"""
Typing Tests — Views
=====================
"""

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.throttling import TestGenerateThrottle, TestSubmitThrottle

from .serializers import TestGenerateSerializer, TestSubmitSerializer
from .services import TestGenerationService
from .validators import AntiCheatValidator


class TestGenerateView(APIView):
    """
    GET /api/v1/tests/generate/ — Generate typing test content
    """

    permission_classes = [permissions.AllowAny]
    throttle_classes = [TestGenerateThrottle]

    def get(self, request):
        serializer = TestGenerateSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = TestGenerationService.generate(
            mode=data["mode"],
            language=data.get("language", "en"),
            duration=data.get("duration", 30),
            word_count=data.get("word_count", 50),
            wordlist_id=data.get("wordlist_id"),
            difficulty=data.get("difficulty"),
            punctuation=data.get("punctuation", False),
            numbers=data.get("numbers", False),
        )

        return Response({
            "success": True,
            "data": result,
        })


class TestSubmitView(APIView):
    """
    POST /api/v1/tests/submit/ — Submit typing test result
    """

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [TestSubmitThrottle]

    def post(self, request):
        serializer = TestSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Run anti-cheat validation
        is_clean, flags = AntiCheatValidator.validate(data)

        # Create result
        from apps.results.models import Result

        result = Result.objects.create(
            user=request.user,
            wpm=data["wpm"],
            raw_wpm=data["raw_wpm"],
            accuracy=data["accuracy"],
            consistency=data["consistency"],
            mode=data["mode"],
            duration=data["duration"],
            language=data.get("language", "en"),
            characters_typed=data["characters_typed"],
            correct_chars=data["correct_chars"],
            incorrect_chars=data["incorrect_chars"],
            extra_chars=data.get("extra_chars", 0),
            missed_chars=data.get("missed_chars", 0),
            keystrokes=data.get("keystrokes", []),
            char_log=data.get("char_log", []),
            wpm_history=data.get("wpm_history", []),
            is_flagged=not is_clean,
            flag_reasons=flags if flags else [],
        )

        # Update user profile stats (async in production, sync for now)
        self._update_user_stats(request.user, result)

        from apps.results.serializers import ResultSerializer

        return Response(
            {
                "success": True,
                "data": ResultSerializer(result).data,
                "is_personal_best": result.is_personal_best,
            },
            status=status.HTTP_201_CREATED,
        )

    def _update_user_stats(self, user, result):
        """Update user profile statistics after a test."""
        profile = user.profile
        profile.total_tests += 1
        profile.total_time_typing += result.duration

        if result.wpm > profile.best_wpm and not result.is_flagged:
            profile.best_wpm = result.wpm

        # Running average
        if profile.total_tests > 1:
            profile.avg_wpm = (
                (profile.avg_wpm * (profile.total_tests - 1) + result.wpm)
                / profile.total_tests
            )
            profile.avg_accuracy = (
                (profile.avg_accuracy * (profile.total_tests - 1) + result.accuracy)
                / profile.total_tests
            )
        else:
            profile.avg_wpm = result.wpm
            profile.avg_accuracy = result.accuracy

        # XP calculation (base 10 + bonus for high WPM/accuracy)
        xp_earned = 10
        if result.wpm > 60:
            xp_earned += int(result.wpm / 10)
        if result.accuracy > 95:
            xp_earned += 5
        profile.xp += xp_earned

        # Level up every 100 XP
        profile.level = (profile.xp // 100) + 1

        profile.save()

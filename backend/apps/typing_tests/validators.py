"""
Typing Tests — Anti-Cheat Validators
======================================
"""

import logging
import statistics

logger = logging.getLogger(__name__)


class AntiCheatValidator:
    """
    Validates typing test submissions for suspicious activity.
    Runs synchronous basic checks on submission.
    """

    # Thresholds
    MAX_WPM = 250  # World record is ~220 WPM
    MIN_ACCURACY_FOR_HIGH_WPM = 90  # High WPM must have decent accuracy
    MIN_KEY_DELAY_MS = 15  # Faster than humanly possible
    MAX_CONSISTENCY = 99.5  # Perfect consistency is suspicious

    @classmethod
    def validate(cls, submission_data):
        """
        Run all anti-cheat checks.

        Args:
            submission_data: dict with wpm, raw_wpm, accuracy, consistency, keystrokes, duration

        Returns:
            tuple(is_valid: bool, flags: list[str])
        """
        flags = []

        # Check unrealistic WPM
        wpm = submission_data.get("wpm", 0)
        if wpm > cls.MAX_WPM:
            flags.append(f"wpm_exceeds_maximum: {wpm} > {cls.MAX_WPM}")

        # High WPM with low accuracy is suspicious
        accuracy = submission_data.get("accuracy", 0)
        if wpm > 150 and accuracy < cls.MIN_ACCURACY_FOR_HIGH_WPM:
            flags.append(f"high_wpm_low_accuracy: wpm={wpm}, accuracy={accuracy}")

        # Check keystroke timing
        keystrokes = submission_data.get("keystrokes", [])
        if keystrokes:
            timing_flags = cls._check_keystroke_timing(keystrokes)
            flags.extend(timing_flags)

        # Check consistency (too-perfect is suspicious)
        consistency = submission_data.get("consistency", 0)
        if consistency > cls.MAX_CONSISTENCY and wpm > 100:
            flags.append(f"suspiciously_consistent: {consistency}%")

        # Check duration vs characters typed
        duration = submission_data.get("duration", 0)
        chars_typed = submission_data.get("characters_typed", 0)
        if duration > 0 and chars_typed > 0:
            chars_per_second = chars_typed / duration
            if chars_per_second > 25:  # ~300 WPM equivalent
                flags.append(f"excessive_chars_per_second: {chars_per_second:.1f}")

        is_valid = len(flags) == 0

        if flags:
            logger.warning(
                "Anti-cheat flags for submission: %s",
                ", ".join(flags),
            )

        return is_valid, flags

    @classmethod
    def _check_keystroke_timing(cls, keystrokes):
        """Analyze keystroke timing patterns for bot-like behavior."""
        flags = []

        if len(keystrokes) < 5:
            return flags

        # Extract inter-key intervals
        timestamps = []
        for ks in keystrokes:
            if isinstance(ks, dict) and "timestamp" in ks:
                timestamps.append(ks["timestamp"])
            elif isinstance(ks, (int, float)):
                timestamps.append(ks)

        if len(timestamps) < 5:
            return flags

        intervals = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
        intervals = [i for i in intervals if i > 0]  # Filter out zero/negative intervals

        if not intervals:
            return flags

        # Check for impossibly fast keystrokes
        min_interval = min(intervals)
        if min_interval < cls.MIN_KEY_DELAY_MS:
            flags.append(f"impossibly_fast_keystroke: {min_interval}ms")

        # Check for bot-like uniform intervals (very low std deviation)
        if len(intervals) > 10:
            std_dev = statistics.stdev(intervals)
            mean_interval = statistics.mean(intervals)
            if mean_interval > 0:
                cv = std_dev / mean_interval  # Coefficient of variation
                if cv < 0.05:  # Less than 5% variation is robotic
                    flags.append(f"robotic_timing_pattern: cv={cv:.4f}")

        return flags

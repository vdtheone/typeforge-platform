"""
Word Lists — Admin Configuration
==================================
"""

from django.contrib import admin

from .models import Language, Quote, WordList


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "flag_emoji", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "code")


@admin.register(WordList)
class WordListAdmin(admin.ModelAdmin):
    list_display = ("name", "language", "difficulty", "word_count", "is_default", "is_public", "times_used")
    list_filter = ("language", "difficulty", "is_default", "is_public")
    search_fields = ("name", "slug")
    readonly_fields = ("word_count", "times_used", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "author", "language", "difficulty", "word_count", "is_active")
    list_filter = ("language", "difficulty", "is_active")
    search_fields = ("text", "author", "source")
    readonly_fields = ("word_count", "char_count")

"""Unit tests for base models and mixins.

Tests focus on mixin behavior and logic without requiring database.
Integration tests will be added separately once basic infrastructure is stable.
"""

from datetime import datetime
from uuid import UUID

import pytest
from freezegun import freeze_time

from app.models.base import (
    MultilingualMixin,
    SoftDeleteMixin,
)


# ============================================================================
# SoftDeleteMixin Tests (Pure Unit Tests - No Database)
# ============================================================================

class MockSoftDeleteModel:
    """Mock model for testing SoftDeleteMixin without database."""

    def __init__(self):
        self.is_deleted = False
        self.deleted_at = None

    # Add mixin methods
    soft_delete = SoftDeleteMixin.soft_delete
    restore = SoftDeleteMixin.restore
    is_active = SoftDeleteMixin.is_active


@pytest.mark.unit
@pytest.mark.models
class TestSoftDeleteMixin:
    """Test SoftDeleteMixin functionality."""

    def test_is_deleted_defaults_to_false(self):
        """Test that is_deleted is False by default."""
        model = MockSoftDeleteModel()

        assert model.is_deleted is False
        assert model.deleted_at is None

    def test_soft_delete_sets_flags(self):
        """Test that soft_delete() sets deletion flags."""
        model = MockSoftDeleteModel()

        with freeze_time("2025-01-01 12:00:00"):
            model.soft_delete()

        assert model.is_deleted is True
        assert model.deleted_at is not None
        assert isinstance(model.deleted_at, datetime)

    def test_restore_clears_flags(self):
        """Test that restore() clears deletion flags."""
        model = MockSoftDeleteModel()
        model.soft_delete()

        model.restore()

        assert model.is_deleted is False
        assert model.deleted_at is None

    def test_is_active_returns_true_for_active_record(self):
        """Test is_active() for non-deleted record."""
        model = MockSoftDeleteModel()

        assert model.is_active() is True

    def test_is_active_returns_false_for_deleted_record(self):
        """Test is_active() for soft-deleted record."""
        model = MockSoftDeleteModel()
        model.soft_delete()

        assert model.is_active() is False

    def test_multiple_delete_restore_cycles(self):
        """Test that delete/restore can be called multiple times."""
        model = MockSoftDeleteModel()

        # Delete
        model.soft_delete()
        assert model.is_deleted is True

        # Restore
        model.restore()
        assert model.is_deleted is False

        # Delete again
        model.soft_delete()
        assert model.is_deleted is True


# ============================================================================
# MultilingualMixin Tests (Pure Unit Tests - No Database)
# ============================================================================

class MockMultilingualModel:
    """Mock model for testing MultilingualMixin without database."""

    def __init__(self):
        self.title_i18n = None
        self.description_i18n = None

    # Add mixin methods and constants
    SUPPORTED_LANGUAGES = MultilingualMixin.SUPPORTED_LANGUAGES
    DEFAULT_LANGUAGE = MultilingualMixin.DEFAULT_LANGUAGE
    RTL_LANGUAGES = MultilingualMixin.RTL_LANGUAGES

    get_translation = MultilingualMixin.get_translation
    set_translation = MultilingualMixin.set_translation
    get_supported_languages = MultilingualMixin.get_supported_languages
    is_rtl_language = staticmethod(MultilingualMixin.is_rtl_language)


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.multilingual
class TestMultilingualMixin:
    """Test MultilingualMixin functionality."""

    def test_supported_languages_constant(self):
        """Test that SUPPORTED_LANGUAGES contains expected languages."""
        assert MultilingualMixin.SUPPORTED_LANGUAGES == ['en', 'fa', 'ar', 'tr']

    def test_default_language_is_english(self):
        """Test that DEFAULT_LANGUAGE is English."""
        assert MultilingualMixin.DEFAULT_LANGUAGE == 'en'

    def test_rtl_languages_constant(self):
        """Test that RTL_LANGUAGES contains Persian and Arabic."""
        assert MultilingualMixin.RTL_LANGUAGES == ['fa', 'ar']

    def test_set_translation_creates_content(self):
        """Test setting translation for a field."""
        model = MockMultilingualModel()

        model.set_translation('title_i18n', 'en', 'Software Engineer')

        assert model.title_i18n == {'en': 'Software Engineer'}

    def test_set_multiple_translations(self):
        """Test setting multiple language translations."""
        model = MockMultilingualModel()

        model.set_translation('title_i18n', 'en', 'Software Engineer')
        model.set_translation('title_i18n', 'fa', 'مهندس نرم‌افزار')
        model.set_translation('title_i18n', 'ar', 'مهندس برمجيات')

        assert model.title_i18n == {
            'en': 'Software Engineer',
            'fa': 'مهندس نرم‌افزار',
            'ar': 'مهندس برمجيات'
        }

    def test_get_translation_returns_correct_language(self):
        """Test retrieving translation in specific language."""
        model = MockMultilingualModel()
        model.set_translation('title_i18n', 'en', 'Software Engineer')
        model.set_translation('title_i18n', 'fa', 'مهندس نرم‌افزار')

        result = model.get_translation('title_i18n', 'fa')

        assert result == 'مهندس نرم‌افزار'

    def test_get_translation_fallback_to_default(self):
        """Test that get_translation falls back to default language."""
        model = MockMultilingualModel()
        model.set_translation('title_i18n', 'en', 'Software Engineer')

        # Request Turkish (not available), should fallback to English
        result = model.get_translation('title_i18n', 'tr', fallback='en')

        assert result == 'Software Engineer'

    def test_get_translation_returns_none_if_not_found(self):
        """Test that get_translation returns None if no translation exists."""
        model = MockMultilingualModel()

        result = model.get_translation('title_i18n', 'en')

        assert result is None

    def test_set_translation_raises_error_for_invalid_field(self):
        """Test that set_translation raises error for non-existent field."""
        model = MockMultilingualModel()

        with pytest.raises(ValueError, match="does not exist"):
            model.set_translation('invalid_field', 'en', 'Test')

    def test_set_translation_raises_error_for_unsupported_language(self):
        """Test that set_translation raises error for unsupported language."""
        model = MockMultilingualModel()

        with pytest.raises(ValueError, match="not supported"):
            model.set_translation('title_i18n', 'de', 'Test')

    def test_set_translation_raises_error_for_non_string_value(self):
        """Test that set_translation raises error for non-string value."""
        model = MockMultilingualModel()

        with pytest.raises(ValueError, match="must be a string"):
            model.set_translation('title_i18n', 'en', 123)

    def test_get_supported_languages_returns_available_languages(self):
        """Test getting list of available languages for a field."""
        model = MockMultilingualModel()
        model.set_translation('title_i18n', 'en', 'Software Engineer')
        model.set_translation('title_i18n', 'fa', 'مهندس نرم‌افزار')

        languages = model.get_supported_languages('title_i18n')

        assert set(languages) == {'en', 'fa'}

    def test_get_supported_languages_empty_for_no_translations(self):
        """Test that get_supported_languages returns empty list."""
        model = MockMultilingualModel()

        languages = model.get_supported_languages('title_i18n')

        assert languages == []

    def test_is_rtl_language_true_for_persian(self):
        """Test that Persian is identified as RTL language."""
        assert MultilingualMixin.is_rtl_language('fa') is True

    def test_is_rtl_language_true_for_arabic(self):
        """Test that Arabic is identified as RTL language."""
        assert MultilingualMixin.is_rtl_language('ar') is True

    def test_is_rtl_language_false_for_english(self):
        """Test that English is not RTL language."""
        assert MultilingualMixin.is_rtl_language('en') is False

    def test_is_rtl_language_false_for_turkish(self):
        """Test that Turkish is not RTL language."""
        assert MultilingualMixin.is_rtl_language('tr') is False

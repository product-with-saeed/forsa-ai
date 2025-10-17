"""
Base models and mixins for Forsa AI.

This module provides abstract base classes and mixins that implement
common functionality for all database models. All concrete models must
inherit from these base classes to ensure consistency and maintainability.

Design Principles:
    - Multilingual support via JSONB columns
    - Soft delete pattern for data retention
    - UUID primary keys for global uniqueness
    - Comprehensive audit trail
    - Type safety with proper annotations

Classes:
    Base: SQLAlchemy declarative base
    TimestampMixin: Created/updated timestamps
    SoftDeleteMixin: Soft delete functionality
    MultilingualMixin: i18n content support
    BaseModel: Abstract base combining all mixins
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Mapped, mapped_column

# SQLAlchemy declarative base
Base = declarative_base()


class TimestampMixin:
    """Mixin providing automatic timestamp management.

    Attributes:
        created_at: UTC timestamp when record was created (immutable)
        updated_at: UTC timestamp when record was last modified (auto-updates)

    Example:
        >>> class User(Base, TimestampMixin):
        ...     pass
        >>> user = User()
        >>> print(user.created_at)  # Auto-populated on insert
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="UTC timestamp of record creation"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="UTC timestamp of last modification"
    )


class SoftDeleteMixin:
    """Mixin implementing soft delete pattern.

    Instead of permanently removing records, they are marked as deleted.
    This enables data recovery and maintains referential integrity.

    Attributes:
        is_deleted: Boolean flag indicating deletion status
        deleted_at: UTC timestamp when record was soft-deleted

    Methods:
        soft_delete(): Mark record as deleted
        restore(): Restore a soft-deleted record
        is_active(): Check if record is not deleted

    Example:
        >>> user = User(email="test@example.com")
        >>> user.soft_delete()
        >>> assert user.is_deleted is True
        >>> user.restore()
        >>> assert user.is_active() is True
    """

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Soft delete flag - True if record is deleted"
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        doc="UTC timestamp when record was soft-deleted"
    )

    def soft_delete(self) -> None:
        """Mark this record as deleted.

        Sets is_deleted=True and records deletion timestamp.
        Does not commit - caller must handle session commit.
        """
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        """Restore a soft-deleted record.

        Clears deletion flag and timestamp.
        Does not commit - caller must handle session commit.
        """
        self.is_deleted = False
        self.deleted_at = None

    def is_active(self) -> bool:
        """Check if record is not deleted.

        Returns:
            True if record is active (not deleted), False otherwise
        """
        return not self.is_deleted


class MultilingualMixin:
    """Mixin providing multilingual content support.

    Stores text content in multiple languages using PostgreSQL JSONB.
    Supports Persian (fa), Arabic (ar), Turkish (tr), and English (en).

    Methods:
        get_translation(field_name, lang, fallback): Get text in specific language
        set_translation(field_name, lang, value): Set text for specific language
        get_supported_languages(field_name): Get available languages for field

    Example:
        >>> job = Job()
        >>> job.set_translation('title', 'en', 'Software Engineer')
        >>> job.set_translation('title', 'fa', 'مهندس نرم‌افزار')
        >>> print(job.get_translation('title', 'fa'))
        'مهندس نرم‌افزار'
        >>> print(job.get_translation('title', 'ar', fallback='en'))
        'Software Engineer'  # Falls back to English if Arabic not available
    """

    # Supported languages for this platform
    SUPPORTED_LANGUAGES = ['en', 'fa', 'ar', 'tr']
    DEFAULT_LANGUAGE = 'en'

    # RTL (Right-to-Left) languages
    RTL_LANGUAGES = ['fa', 'ar']

    def get_translation(
        self,
        field_name: str,
        lang: str,
        fallback: str = 'en'
    ) -> Optional[str]:
        """Get translated content for a specific field and language.

        Args:
            field_name: Name of the i18n field (e.g., 'title_i18n')
            lang: ISO 639-1 language code (en, fa, ar, tr)
            fallback: Language to use if requested lang not available

        Returns:
            Translated string or None if not found

        Raises:
            ValueError: If field_name doesn't exist or isn't a JSONB field

        Example:
            >>> job.get_translation('title_i18n', 'fa', fallback='en')
            'مهندس نرم‌افزار'
        """
        if not hasattr(self, field_name):
            raise ValueError(f"Field '{field_name}' does not exist on {self.__class__.__name__}")

        content: Optional[Dict[str, str]] = getattr(self, field_name)

        if not content:
            return None

        # Try requested language first
        if lang in content:
            return content[lang]

        # Fall back to fallback language
        if fallback in content:
            return content[fallback]

        # Return any available language as last resort
        return next(iter(content.values())) if content else None

    def set_translation(
        self,
        field_name: str,
        lang: str,
        value: str
    ) -> None:
        """Set translated content for a specific field and language.

        Args:
            field_name: Name of the i18n field (e.g., 'title_i18n')
            lang: ISO 639-1 language code (en, fa, ar, tr)
            value: Translated text content

        Raises:
            ValueError: If field doesn't exist, lang unsupported, or value invalid

        Example:
            >>> job.set_translation('title_i18n', 'fa', 'مهندس نرم‌افزار')
        """
        if not hasattr(self, field_name):
            raise ValueError(f"Field '{field_name}' does not exist on {self.__class__.__name__}")

        if lang not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Language '{lang}' not supported. Use: {', '.join(self.SUPPORTED_LANGUAGES)}"
            )

        if not isinstance(value, str):
            raise ValueError("Translation value must be a string")

        current_content: Optional[Dict[str, str]] = getattr(self, field_name)

        if current_content is None:
            current_content = {}

        current_content[lang] = value
        setattr(self, field_name, current_content)

    def get_supported_languages(self, field_name: str) -> list[str]:
        """Get list of languages available for a specific field.

        Args:
            field_name: Name of the i18n field

        Returns:
            List of ISO 639-1 language codes that have translations

        Example:
            >>> job.get_supported_languages('title_i18n')
            ['en', 'fa', 'ar']
        """
        if not hasattr(self, field_name):
            raise ValueError(f"Field '{field_name}' does not exist")

        content: Optional[Dict[str, str]] = getattr(self, field_name)
        return list(content.keys()) if content else []

    @staticmethod
    def is_rtl_language(lang: str) -> bool:
        """Check if a language requires RTL (Right-to-Left) layout.

        Args:
            lang: ISO 639-1 language code

        Returns:
            True if language is RTL (Persian, Arabic)
        """
        return lang in MultilingualMixin.RTL_LANGUAGES


class BaseModel(Base, TimestampMixin, SoftDeleteMixin, MultilingualMixin):
    """Abstract base model for all domain entities.

    Combines all mixins to provide:
        - UUID primary keys
        - Automatic timestamps
        - Soft delete capability
        - Multilingual content support

    All concrete models (User, Job, Company, etc.) must inherit from this class.

    Attributes:
        id: UUID primary key
        created_at: Creation timestamp (from TimestampMixin)
        updated_at: Last update timestamp (from TimestampMixin)
        is_deleted: Soft delete flag (from SoftDeleteMixin)
        deleted_at: Deletion timestamp (from SoftDeleteMixin)

    Note:
        This is an abstract class - it won't create a table.
        Concrete models must define __tablename__ attribute.

    Example:
        >>> class User(BaseModel):
        ...     __tablename__ = 'users'
        ...     email = Column(String, unique=True, nullable=False)
    """

    __abstract__ = True  # Don't create table for base class

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
        doc="UUID primary key - globally unique identifier"
    )

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name.

        Converts CamelCase class name to snake_case table name.
        Can be overridden in concrete models.

        Returns:
            snake_case table name

        Example:
            UserProfile -> user_profile
            JobApplication -> job_application
        """
        import re
        name = cls.__name__
        # Convert CamelCase to snake_case
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    def __repr__(self) -> str:
        """String representation for debugging.

        Returns:
            String showing class name and ID
        """
        return f"<{self.__class__.__name__}(id={self.id})>"

    def to_dict(self, include_deleted: bool = False) -> Dict[str, Any]:
        """Convert model to dictionary representation.

        Args:
            include_deleted: Whether to include deleted records

        Returns:
            Dictionary with all model fields

        Note:
            Useful for API serialization. Consider using Pydantic schemas instead.
        """
        if not include_deleted and self.is_deleted:
            return {}

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

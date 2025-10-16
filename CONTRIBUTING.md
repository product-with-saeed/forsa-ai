# Contributing to Forsa AI

Thank you for your interest in contributing to Forsa AI! This document provides guidelines and standards for contributing to this world-class, production-grade open-source project.

## 🌟 Our Standards

Forsa AI is built to **world-class standards**. We expect:

- **Production-ready code** - Not prototypes or "TODO: refactor later"
- **Clean OOP design** - SOLID principles, proper abstractions
- **Comprehensive documentation** - Every class, function, and decision explained
- **Type safety** - Complete type hints throughout
- **International-first** - i18n/l10n considerations in every feature
- **Test coverage** - Unit and integration tests for all code
- **Forward compatibility** - Design for scale and evolution

## 🎯 Ways to Contribute

### 1. Code Contributions
- 🐛 Fix bugs
- ✨ Implement new features
- 🔧 Improve existing functionality
- ⚡ Performance optimizations
- 🧪 Add tests

### 2. Documentation
- 📝 Improve README, guides, tutorials
- 🏗️ Document architecture decisions
- 💡 Create examples and use cases
- 🌐 Translate documentation

### 3. Internationalization (i18n)
- 🌍 Translate UI text (Persian, Arabic, Turkish, English)
- 🔤 Add RTL support enhancements
- 🗺️ Regional job market insights
- 📊 Locale-specific formatting

### 4. Web Scraping
- 🕷️ Create new job site scrapers
- 🔄 Maintain existing scrapers
- 🛡️ Handle anti-bot measures
- 📋 Regional job platform expertise

### 5. AI/ML
- 🤖 Improve LLM prompts
- 🎯 Enhance semantic matching
- 📈 Optimize embeddings
- 🧠 Train custom models

### 6. Community
- 💬 Answer questions in Discussions
- 🐛 Triage issues
- 👥 Help onboard new contributors
- 📢 Spread the word

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **Docker & Docker Compose**
- **Git**
- **Code editor** (VS Code recommended)

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork:**
```bash
   git clone https://github.com/YOUR_USERNAME/forsa-ai.git
   cd forsa-ai
```

3. **Add upstream remote:**
```bash
   git remote add upstream https://github.com/product-with-saeed/forsa-ai.git
```

4. **Create a virtual environment:**
```bash
   python3.12 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

5. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

6. **Install development tools:**
```bash
   pip install black flake8 mypy pytest pytest-asyncio pytest-cov
```

7. **Copy environment file:**
```bash
   cp .env.example .env
   # Edit .env and add your API keys
```

8. **Start Docker services:**
```bash
   docker-compose up -d postgres redis
```

9. **Run migrations:**
```bash
   alembic upgrade head
```

10. **Verify setup:**
```bash
    pytest
    uvicorn app.main:app --reload
    # Visit http://localhost:8000/docs
```

## 📋 Development Workflow

### 1. Find or Create an Issue

- Browse [existing issues](https://github.com/product-with-saeed/forsa-ai/issues)
- Look for `good first issue` or `help wanted` labels
- Or create a new issue to propose your contribution

### 2. Create a Feature Branch
```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a new branch
git checkout -b feature/your-feature-name
# Or: git checkout -b fix/bug-description
# Or: git checkout -b docs/documentation-improvement
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Adding tests
- `i18n/` - Internationalization

### 3. Write Your Code

Follow our coding standards (see below).

### 4. Test Your Changes
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# Run linting
black . --check
flake8 app tests
mypy app
```

### 5. Commit Your Changes

**Commit message format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting (no code change)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance

**Example:**
```bash
git add .
git commit -m "feat: add Persian language support to job search

- Implement Persian text normalization
- Add RTL layout support
- Update database schema for multilingual content
- Add unit tests for Persian search

Closes #123"
```

### 6. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 7. Create Pull Request

- Go to GitHub and create a Pull Request from your fork
- Fill out the PR template completely
- Link related issues
- Request review from maintainers

## 💻 Coding Standards

### Python Code Style

**We use Black formatter with 120 character line length:**
```bash
# Format code
black . --line-length 120

# Check without changing
black . --check --line-length 120
```

**Flake8 configuration (.flake8):**
```ini
[flake8]
max-line-length = 120
extend-ignore = E203, W503
exclude = .git,__pycache__,.venv,build,dist
```

### Type Hints

**MANDATORY - All functions must have complete type hints:**
```python
# ✅ GOOD
from typing import Optional, List
from pydantic import BaseModel

def search_jobs(
    query: str,
    location: Optional[str] = None,
    max_results: int = 10
) -> List[JobResult]:
    """Search for jobs matching the query.

    Args:
        query: Search query string (supports multilingual)
        location: Optional location filter
        max_results: Maximum number of results to return

    Returns:
        List of matching job results

    Raises:
        ValueError: If query is empty or invalid
    """
    pass

# ❌ BAD - No type hints
def search_jobs(query, location=None, max_results=10):
    pass
```

### Docstrings

**Use Google-style docstrings for all public classes and functions:**
```python
class JobScraper:
    """Base class for job board scrapers.

    This abstract base class defines the interface for all job scrapers.
    Implementations must handle multilingual content and RTL languages.

    Attributes:
        source_name: Name of the job board being scraped
        supported_languages: List of ISO 639-1 language codes supported
        rate_limit: Requests per minute allowed

    Example:
        >>> scraper = LinkedInScraper()
        >>> jobs = await scraper.scrape(query="Python Developer", lang="en")
    """

    def __init__(self, source_name: str, rate_limit: int = 60):
        """Initialize the scraper.

        Args:
            source_name: Name identifier for this job source
            rate_limit: Maximum requests per minute (default: 60)
        """
        pass
```

### Class Design

**Follow OOP principles and design patterns:**
```python
# ✅ GOOD - Clean abstraction with dependency injection
from abc import ABC, abstractmethod
from typing import Protocol

class JobRepository(Protocol):
    """Protocol for job data access."""
    async def save(self, job: Job) -> Job:
        ...

    async def find_by_id(self, job_id: str) -> Optional[Job]:
        ...

class JobService:
    """Business logic for job operations.

    This service encapsulates all job-related business rules and
    orchestrates operations between repositories and external services.
    """

    def __init__(
        self,
        job_repo: JobRepository,
        ai_service: AIService,
        logger: Logger
    ):
        self.job_repo = job_repo
        self.ai_service = ai_service
        self.logger = logger

    async def match_jobs_to_user(
        self,
        user: User,
        max_results: int = 20
    ) -> List[JobMatch]:
        """Find best matching jobs for user using AI.

        This method uses semantic search with embeddings to find
        jobs that match the user's profile, skills, and preferences.
        Supports multilingual matching.

        Args:
            user: User profile to match against
            max_results: Maximum number of matches to return

        Returns:
            List of JobMatch objects sorted by relevance score
        """
        pass

# ❌ BAD - God class with tight coupling
class JobManager:
    def do_everything(self):
        # Direct database access
        # Direct API calls
        # Business logic
        # Presentation logic
        pass
```

### Error Handling

**Use specific exceptions and proper error messages:**
```python
# ✅ GOOD
from app.core.exceptions import JobNotFoundError, InvalidLanguageError

class JobService:
    async def get_job(self, job_id: str, lang: str) -> Job:
        """Get job by ID with localized content.

        Args:
            job_id: Unique job identifier
            lang: ISO 639-1 language code (en, fa, ar, tr)

        Returns:
            Job object with content in requested language

        Raises:
            JobNotFoundError: If job_id doesn't exist
            InvalidLanguageError: If language not supported
        """
        if lang not in ["en", "fa", "ar", "tr"]:
            raise InvalidLanguageError(
                f"Language '{lang}' not supported. Use: en, fa, ar, tr"
            )

        job = await self.job_repo.find_by_id(job_id)
        if not job:
            raise JobNotFoundError(f"Job with ID {job_id} not found")

        return job

# ❌ BAD - Generic exceptions, no validation
async def get_job(job_id, lang):
    try:
        job = db.get(job_id)
        return job
    except:
        return None
```

### Testing

**Write comprehensive tests for all code:**
```python
# tests/services/test_job_service.py
import pytest
from app.services.job_service import JobService
from app.core.exceptions import JobNotFoundError, InvalidLanguageError

@pytest.fixture
def job_service(mock_job_repo, mock_ai_service):
    """Fixture providing JobService with mocked dependencies."""
    return JobService(
        job_repo=mock_job_repo,
        ai_service=mock_ai_service,
        logger=mock_logger
    )

@pytest.mark.asyncio
async def test_get_job_success(job_service, sample_job):
    """Test successful job retrieval with valid language."""
    result = await job_service.get_job(
        job_id="123",
        lang="fa"
    )

    assert result.id == "123"
    assert result.language == "fa"

@pytest.mark.asyncio
async def test_get_job_invalid_language(job_service):
    """Test that invalid language raises appropriate error."""
    with pytest.raises(InvalidLanguageError) as exc_info:
        await job_service.get_job(job_id="123", lang="invalid")

    assert "not supported" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_job_not_found(job_service, mock_job_repo):
    """Test that missing job raises appropriate error."""
    mock_job_repo.find_by_id.return_value = None

    with pytest.raises(JobNotFoundError):
        await job_service.get_job(job_id="nonexistent", lang="en")
```

### Internationalization (i18n)

**Always design for multilingual support:**
```python
# ✅ GOOD - Multilingual from the start
from typing import Dict
from pydantic import BaseModel, Field

class JobTitle(BaseModel):
    """Multilingual job title.

    All user-facing text must support multiple languages.
    """
    en: str = Field(..., description="English title")
    fa: Optional[str] = Field(None, description="Persian title (فارسی)")
    ar: Optional[str] = Field(None, description="Arabic title (العربية)")
    tr: Optional[str] = Field(None, description="Turkish title (Türkçe)")

    def get(self, lang: str, fallback: str = "en") -> str:
        """Get title in specified language with fallback.

        Args:
            lang: ISO 639-1 language code
            fallback: Fallback language if requested not available

        Returns:
            Title string in requested language
        """
        return getattr(self, lang, None) or getattr(self, fallback)

class Job(BaseModel):
    id: str
    title: JobTitle
    description: Dict[str, str] = Field(
        ...,
        description="Job description in multiple languages"
    )

    @property
    def is_rtl(self) -> bool:
        """Check if job content requires RTL layout."""
        return self.primary_language in ["fa", "ar"]

# ❌ BAD - English-only design
class Job:
    title: str
    description: str
```

## 🔍 Code Review Process

### What We Look For

**Your PR will be reviewed for:**

1. **Code Quality**
   - Follows coding standards
   - Clean OOP design
   - Proper error handling
   - No code smells

2. **Documentation**
   - Complete docstrings
   - Type hints everywhere
   - Inline comments for complex logic
   - Updated README if needed

3. **Testing**
   - Unit tests for new code
   - Integration tests where appropriate
   - All tests passing
   - Good coverage (aim for >80%)

4. **Internationalization**
   - Multilingual support considered
   - RTL compatibility checked
   - Proper character encoding

5. **Performance**
   - No obvious bottlenecks
   - Async/await used correctly
   - Database queries optimized

### Review Timeline

- **Initial review:** Within 2-3 days
- **Follow-up reviews:** Within 1-2 days after updates
- **Merge:** After approval from 2 maintainers

### Addressing Feedback
```bash
# Make requested changes
git add .
git commit -m "refactor: address review feedback

- Improve error handling in job scraper
- Add missing type hints
- Enhance docstrings"

# Push to same branch
git push origin feature/your-feature-name
```

## 📝 Documentation Standards

### Code Documentation

**Every module should have a header:**
```python
"""Job scraping services.

This module contains all job board scraper implementations.
Each scraper must handle multilingual content and respect
rate limits.

Classes:
    BaseScraper: Abstract base class for all scrapers
    LinkedInScraper: LinkedIn job scraping implementation
    BaytScraper: Bayt.com scraping implementation

Example:
    >>> scraper = LinkedInScraper()
    >>> jobs = await scraper.scrape(query="Python", location="Tehran")
"""
```

### Architecture Decisions

**Document important decisions in docs/adr/:**
```markdown
# ADR-001: Use PostgreSQL for Full-Text Search

## Status
Accepted

## Context
We need multilingual full-text search for Persian, Arabic, Turkish, English.

## Decision
Use PostgreSQL with custom text search configurations for each language.

## Consequences
- Simpler architecture (no separate search engine)
- Native support for our languages
- Easier deployment and maintenance
```

## 🐛 Bug Reports

**Use the issue template and provide:**

- Clear title describing the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Docker version)
- Relevant logs or error messages
- Screenshots if applicable

## 💡 Feature Requests

**Before proposing a feature:**

1. Check if it already exists or is planned
2. Search existing issues and discussions
3. Consider if it aligns with project goals

**In your proposal, include:**

- **Problem:** What problem does this solve?
- **Solution:** How would it work?
- **Alternatives:** What other approaches did you consider?
- **Impact:** Who benefits and how?
- **i18n:** How does this work across languages?

## ❓ Questions

**For questions:**

- Check [Discussions](https://github.com/product-with-saeed/forsa-ai/discussions)
- Search existing issues
- Ask in the appropriate Discussion category
- Be specific and provide context

## 🏆 Recognition

**Contributors are recognized in:**

- README.md Contributors section
- Release notes
- Project documentation
- Annual contributor highlights

## 📜 Legal

By contributing, you agree that:

- Your contributions will be licensed under AGPL-3.0
- You have the right to submit the contribution
- You grant us a perpetual, worldwide license to your contribution

## 📬 Contact

- **GitHub Issues:** Technical discussions
- **Discussions:** General questions and community
- **Email:** product.with.saeed@gmail.com for private matters

---

**Thank you for contributing to Forsa AI! Together, we're creating opportunities for millions across the MENA region. 🌟**

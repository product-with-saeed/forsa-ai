# Forsa AI (فرصة) - AI-Powered Job Search Platform for MENA

<div align="center">

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Forsa** (فرصة) means "Opportunity" in Arabic - helping MENA job seekers find economic opportunities through AI-powered job aggregation and career assistance.

[Features](#features) • [Architecture](#architecture) • [Quick Start](#quick-start) • [Contributing](#contributing) • [Roadmap](#roadmap)

</div>

---

## 🌍 Vision

Forsa AI addresses the fragmented job market across the Middle East, North Africa, and Turkey by:

- **Aggregating opportunities** from multiple platforms (LinkedIn, Bayt, IranTalent, and more)
- **AI-powered matching** using embeddings and semantic search
- **Multilingual support** - First-class support for Persian (فارسی), Arabic (العربية), Turkish (Türkçe), and English
- **Career assistance** - AI-powered resume analysis, cover letter generation, interview prep
- **RTL-first design** - Built for right-to-left languages from the ground up

This is not just another job board - it's an intelligent career companion designed specifically for MENA professionals.

---

## ✨ Features

### Core Platform
- 🔍 **Job Aggregation Engine** - Scrapy-based distributed scraping with deduplication
- 🤖 **AI Career Assistant** - LLM-powered resume analysis and cover letter generation
- 🎯 **Smart Matching** - Semantic job matching using vector embeddings
- 🌐 **Multilingual** - Native support for Persian, Arabic, Turkish, English
- 📊 **User Dashboard** - Track applications, save jobs, analyze skill gaps
- 🔔 **Real-time Notifications** - WebSocket-based instant updates

### Technical Highlights
- **Production-grade architecture** - FastAPI + PostgreSQL + Redis + Celery
- **AI/ML Integration** - LangChain/LlamaIndex for LLM orchestration
- **Modern async Python** - Fully async/await codebase
- **Type safety** - Comprehensive type hints with Pydantic v2
- **International-first** - i18n/l10n built into data models from day one
- **Developer-friendly** - Complete Docker setup, auto-generated API docs

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Future)                        │
│              React + RTL Support + i18n                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    FastAPI REST API                          │
│  • Authentication & Authorization                            │
│  • Job Search & Filtering (Multilingual)                     │
│  • AI Career Assistant Endpoints                             │
│  • Real-time WebSocket Connections                           │
└─────────┬──────────────────────────┬────────────────────────┘
          │                          │
┌─────────▼──────────┐    ┌──────────▼─────────────────────────┐
│   PostgreSQL       │    │      Redis + Celery                 │
│  • Job Data        │    │  • Background Job Scraping          │
│  • User Profiles   │    │  • Task Queue Management            │
│  • Applications    │    │  • Caching Layer                    │
│  • Full-text Search│    │  • Rate Limiting                    │
└────────────────────┘    └─────────┬──────────────────────────┘
                                    │
                          ┌─────────▼──────────────────┐
                          │   AI/ML Services           │
                          │  • LLM Integration         │
                          │  • Vector Embeddings       │
                          │  • Semantic Search         │
                          └────────────────────────────┘
```

**Technology Stack:**
- **Backend:** Python 3.12+, FastAPI, SQLAlchemy 2.0, Pydantic v2
- **Database:** PostgreSQL 16 with full-text search extensions
- **Caching:** Redis 7
- **Task Queue:** Celery + Flower (monitoring)
- **Web Scraping:** Scrapy, Selenium, BeautifulSoup
- **AI/ML:** LangChain, OpenAI/Anthropic APIs, Sentence Transformers
- **Infrastructure:** Docker, Docker Compose, GitHub Actions

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed
- **Python 3.12+** (for local development)
- **Git**

### Installation

```bash
# Clone the repository
git clone https://github.com/product-with-saeed/forsa-ai.git
cd forsa-ai

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys (OpenAI/Anthropic)
nano .env

# Build and start services
docker-compose up --build

# API will be available at:
# http://localhost:8000
# http://localhost:8000/docs (Interactive API documentation)
```

### Local Development Setup

```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","environment":"development","version":"0.1.0"}
```

---

## 🗺️ Roadmap

### Phase 1: Foundation (Months 1-3) - Current Phase
- [x] Project setup and Docker configuration
- [x] FastAPI application structure
- [x] Database schema design
- [ ] Job scraping engine (Scrapy spiders for LinkedIn, Bayt, IranTalent)
- [ ] LLM integration and AI career assistant
- [ ] User authentication and basic dashboard
- [ ] Initial deployment

### Phase 2: Community & Scale (Months 4-6)
- [ ] Contributor onboarding and documentation
- [ ] Advanced search with filters (multilingual)
- [ ] Real-time notifications via WebSockets
- [ ] Mobile-responsive frontend
- [ ] Performance optimization
- [ ] 1000+ active users milestone

### Phase 3: Monetization & Growth (Months 7-12)
- [ ] Premium features (advanced AI assistance)
- [ ] Enterprise partnerships
- [ ] Job posting platform for employers
- [ ] Regional expansion
- [ ] Mobile app development

---

## 🤝 Contributing

We welcome contributors from around the world, especially those familiar with MENA job markets and languages!

**Areas where we need help:**
- 🌐 **Translation & Localization** - Native speakers of Persian, Arabic, Turkish
- 🕷️ **Web Scraping** - Expertise with regional job platforms
- 🤖 **AI/ML** - LLM integration, embeddings, semantic search
- 🎨 **Frontend** - React developers with RTL experience
- 📝 **Documentation** - Technical writing, tutorials
- 🧪 **Testing** - QA, test automation

### How to Contribute

1. **Read [CONTRIBUTING.md](CONTRIBUTING.md)** for detailed guidelines
2. **Check [Issues](https://github.com/product-with-saeed/forsa-ai/issues)** for tasks labeled `good first issue`
3. **Fork the repository** and create a feature branch
4. **Follow our coding standards:**
   - Black formatting (line length: 120)
   - Type hints everywhere
   - Comprehensive docstrings
   - Tests for new features
5. **Submit a Pull Request** with clear description

### Development Standards

This is a **world-class, production-grade project**. We maintain high standards:

- ✅ **Clean OOP design** - SOLID principles, design patterns
- ✅ **Type safety** - Complete type hints, Pydantic models
- ✅ **Documentation** - Docstrings, inline comments, architectural decisions
- ✅ **Testing** - Unit tests, integration tests (pytest)
- ✅ **International-first** - i18n considerations in all features
- ✅ **Code review** - All changes reviewed before merge

---

## 📖 Documentation

- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design and technical decisions
- **[API Documentation](http://localhost:8000/docs)** - Interactive Swagger UI (when running)
- **[Database Schema](docs/DATABASE.md)** - Data models and relationships
- **[Internationalization Guide](docs/I18N.md)** - Adding new languages
- **[Scraping Guide](docs/SCRAPING.md)** - Adding new job sources

---

## 🔒 Security & Privacy

- All user data encrypted at rest
- GDPR-compliant data handling
- No selling of user data - ever
- Secure authentication with JWT
- Regular security audits

**Found a security vulnerability?** Please email product.with.saeed@gmail.com instead of opening a public issue.

---

## 📊 Project Status

**Current Phase:** Month 1 - Foundation Setup
**Version:** 0.1.0 (Alpha)
**Last Updated:** October 2025

### Recent Achievements
- ✅ Complete Docker development environment
- ✅ FastAPI backend with auto-generated docs
- ✅ PostgreSQL + Redis infrastructure
- ✅ Project structure and standards defined

### Active Focus
- 🔨 Database schema implementation
- 🔨 Job scraping engine development
- 🔨 LLM integration for AI features

---

## 📜 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

**What this means:**
- ✅ You can use, modify, and distribute this software
- ✅ If you run a modified version as a service, you must release your source code
- ✅ Protects against proprietary derivatives
- ✅ Perfect for open-source SaaS projects

See [LICENSE](LICENSE) file for details.

**Commercial licensing available** for enterprises requiring proprietary modifications. Contact: product.with.saeed@gmail.com

---

## 🌟 Acknowledgments

- Built with love for the MENA region 🇮🇷 🇹🇷 🇸🇦 🇪🇬 and beyond
- Inspired by the need for better job opportunities across borders
- Thank you to all contributors and supporters

---

## 📬 Contact & Community

- **GitHub Issues:** [Report bugs or request features](https://github.com/product-with-saeed/forsa-ai/issues)
- **Discussions:** [Join community discussions](https://github.com/product-with-saeed/forsa-ai/discussions)
- **Email:** product.with.saeed@gmail.com
- **LinkedIn:** [linkedin.com/in/product-with-saeed](https://www.linkedin.com/in/product-with-saeed/)

---

<div align="center">

**⭐ Star this repository if you believe in connecting MENA talent with global opportunities! ⭐**

Made with ❤️ by developers who care about economic opportunity

</div>

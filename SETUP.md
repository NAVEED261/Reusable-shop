# Developer Setup Guide

**Men's Boutique E-Commerce Platform**
**Get productive in <4 hours**

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Development Setup](#local-development-setup)
3. [Running Services](#running-services)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)
7. [Project Structure](#project-structure)

---

## System Requirements

### Software
- **Node.js**: 18.17+ (for frontend)
- **Python**: 3.11+ (for backend)
- **Docker**: Latest (for containerized services)
- **Docker Compose**: Latest (for orchestrating services)
- **Git**: Latest
- **PostgreSQL**: 14+ (or use Docker)
- **Redis**: (optional, for caching)

### Hardware
- **Minimum**: 8GB RAM, 2 CPU cores, 20GB disk
- **Recommended**: 16GB RAM, 4 CPU cores, 50GB disk

### Accounts
- **Stripe**: https://stripe.com (test and live keys)
- **OpenAI**: https://platform.openai.com (API key)
- **Neon**: https://neon.tech (PostgreSQL hosting)
- **Vercel**: https://vercel.com (frontend hosting)
- **GitHub**: https://github.com (code repository)

---

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/NAVEED261/Reusable-shop.git
cd Reusable-shop
```

### Step 2: Set Up Environment Variables

**Backend** (`.env.backend`):
```bash
# Copy example file
cp learnflow-app/.env.backend.example learnflow-app/.env.backend

# Edit with your keys
nano learnflow-app/.env.backend
```

**Required variables**:
```
DATABASE_URL=postgresql://user:password@localhost:5432/reusable_shop_dev
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
QDRANT_URL=http://localhost:6333
JWT_SECRET=your-random-secret-key
WHATSAPP_NUMBER=+923331234567
SENTRY_DSN=(optional)
```

**Frontend** (`.env.local`):
```bash
# In learnflow-app/app/frontend/
touch .env.local
```

**Required variables**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_WHATSAPP_NUMBER=+923331234567
```

### Step 3: Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r learnflow-app/app/backend/requirements.txt
```

### Step 4: Set Up Node.js

```bash
# Install Node dependencies
cd learnflow-app/app/frontend
npm install

# Go back to root
cd ../../../
```

### Step 5: Start Database

**Option A: Using Docker (Recommended)**
```bash
# Start PostgreSQL in Docker
docker run -d \
  --name postgres_dev \
  -e POSTGRES_USER=dev \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=reusable_shop_dev \
  -p 5432:5432 \
  postgres:14-alpine
```

**Option B: Using Docker Compose**
```bash
cd learnflow-app
docker-compose up -d postgres qdrant
```

### Step 6: Run Database Migrations

```bash
cd learnflow-app/app/backend
alembic upgrade head

# Seed sample data
python ../../scripts/seed_products.py
```

### Step 7: Generate Embeddings (RAG)

```bash
# From project root
python learnflow-app/scripts/generate_embeddings.py \
  --db-url $DATABASE_URL \
  --qdrant-url http://localhost:6333 \
  --openai-key $OPENAI_API_KEY
```

---

## Running Services

### Option A: Docker Compose (Recommended for Production-like)

```bash
cd learnflow-app
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379, optional)
- Qdrant (port 6333)
- Product Service (port 8001)
- Order Service (port 8002)
- Chat Service (port 8003)
- Payment Service (port 8004)
- Frontend (port 3000)

### Option B: Manual (Recommended for Development)

**Terminal 1: Backend Services**
```bash
cd learnflow-app/app/backend

# Product Service
uvicorn product_service.main:app --reload --port 8001 &

# Order Service
uvicorn order_service.main:app --reload --port 8002 &

# Chat Service
uvicorn chat_service.main:app --reload --port 8003 &

# Payment Service
uvicorn payment_service.main:app --reload --port 8004 &
```

**Terminal 2: Frontend**
```bash
cd learnflow-app/app/frontend
npm run dev
# Opens at http://localhost:3000
```

**Terminal 3: Qdrant (if needed)**
```bash
docker run -d \
  -p 6333:6333 \
  -p 6334:6334 \
  qdrant/qdrant:latest
```

### Verify Services Are Running

```bash
# Health checks
curl http://localhost:8001/api/health  # Product Service
curl http://localhost:8002/api/health  # Order Service
curl http://localhost:8003/api/health  # Chat Service
curl http://localhost:8004/api/health  # Payment Service
curl http://localhost:3000             # Frontend
```

---

## Testing

### Run All Tests

```bash
# Backend tests
cd learnflow-app/app/backend
pytest tests/ -v --cov=app --cov-report=html

# Frontend tests
cd learnflow-app/app/frontend
npm test
npm run test:e2e  # Playwright E2E tests
```

### Run Specific Test

```bash
# Single test file
pytest tests/unit/test_products.py -v

# Single test function
pytest tests/unit/test_products.py::test_product_filtering -v

# With coverage
pytest tests/ --cov=app --cov-report=term-missing
```

### Coverage Reports

```bash
# Backend coverage HTML report
# Opens in learnflow-app/app/backend/htmlcov/index.html

# Frontend coverage
npm test -- --coverage --watch=false
```

---

## Deployment

### Frontend to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy to Vercel
cd learnflow-app/app/frontend
vercel --prod

# Preview deployments
git checkout -b feature-branch
git push origin feature-branch
# Vercel automatically creates preview URL
```

### Backend to Railway/Render

```bash
# Method 1: Via GitHub (Recommended)
# 1. Push to main branch
git add .
git commit -m "Deploy backend"
git push origin main

# 2. Railway/Render automatically detects and deploys

# Method 2: Via CLI
# Railway
railway up --push

# Render
render deploy --env production
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Database Connection Error

```bash
# Verify PostgreSQL is running
psql -U dev -d reusable_shop_dev -c "SELECT 1"

# Check connection string
echo $DATABASE_URL

# Reset database
# WARNING: This deletes all data!
dropdb -U dev reusable_shop_dev
createdb -U dev reusable_shop_dev
alembic upgrade head
```

### OpenAI API Rate Limit

```bash
# Wait and retry
# Add rate limiting in code:
import time
time.sleep(60)  # Wait 60 seconds

# Or use exponential backoff
# See: learnflow-app/app/backend/chat_service/rag_client.py
```

### Docker Compose Issues

```bash
# Clean start (remove containers/volumes)
docker-compose down -v
docker-compose up -d

# View logs
docker-compose logs -f service_name

# Rebuild image
docker-compose build --no-cache service_name
```

### Stripe Test Mode Issues

```bash
# Use correct test keys (start with pk_test_ or sk_test_)
# Don't use live keys in development!

# Test cards:
# Success: 4242 4242 4242 4242
# Decline: 4000 0000 0000 0002
# 3D Secure: 4000 0000 0000 0341

# Find keys at: https://dashboard.stripe.com/test/apikeys
```

### Node/Python Version Issues

```bash
# Check Node version
node --version  # Should be 18.17+

# Check Python version
python3 --version  # Should be 3.11+

# Update Node (via nvm)
nvm install 18.17.0
nvm use 18.17.0

# Update Python (via pyenv)
pyenv install 3.11.0
pyenv local 3.11.0
```

---

## Project Structure

```
Reusable-shop/
├── learnflow-app/
│   ├── app/
│   │   ├── frontend/              # Next.js React app
│   │   │   ├── app/               # Next.js pages/routes
│   │   │   ├── components/        # React components
│   │   │   ├── public/            # Static assets
│   │   │   ├── package.json
│   │   │   └── tsconfig.json
│   │   │
│   │   └── backend/               # FastAPI services
│   │       ├── product_service/   # Product catalog
│   │       ├── order_service/     # Orders & checkout
│   │       ├── chat_service/      # AI chat & RAG
│   │       ├── payment_service/   # Stripe integration
│   │       ├── notification_service/  # Emails/SMS
│   │       ├── admin_service/     # Analytics
│   │       ├── requirements.txt
│   │       ├── main.py
│   │       └── alembic/           # Database migrations
│   │
│   ├── database/
│   │   ├── schema.sql
│   │   └── seeds/
│   │
│   ├── scripts/
│   │   ├── generate_embeddings.py # RAG embeddings
│   │   ├── seed_products.py       # Sample data
│   │   └── backup_database.sh
│   │
│   ├── tests/
│   │   ├── unit/                  # Unit tests
│   │   ├── integration/           # Integration tests
│   │   └── e2e/                   # E2E tests
│   │
│   ├── docker-compose.yml         # Service orchestration
│   ├── Dockerfile                 # Docker image
│   └── .env.backend.example
│
├── .claude/                        # Claude Code configuration
│   ├── agents/                    # AI agents
│   └── skills/                    # Reusable skills
│
├── specs/
│   └── phase5-testing/            # Phase 5 spec
│
├── history/
│   ├── prompts/                   # Prompt history records
│   └── adr/                       # Architecture decisions
│
├── CLAUDE.md                       # Implementation plan
├── TASKS.md                        # Task tracking
├── DEPLOYMENT.md                   # Deployment runbook
├── SETUP.md                        # This file
├── README.md                       # Project overview
└── .gitignore
```

---

## Common Commands

### Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Run tests
pytest tests/ -v

# Format code
black .  # Python
prettier --write .  # JavaScript

# Lint
flake8 .  # Python
eslint .  # JavaScript
```

### Database

```bash
# Connect to database
psql -U dev -d reusable_shop_dev

# Run migrations
alembic upgrade head
alembic downgrade -1  # Rollback

# Seed data
python scripts/seed_products.py
```

### Git

```bash
# Create feature branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "Add feature"

# Push to GitHub
git push origin feature/my-feature

# Create pull request
# Go to GitHub and create PR

# Merge after review
git checkout main
git pull origin main
git merge feature/my-feature
git push origin main
```

### API Testing

```bash
# Get all products
curl http://localhost:8001/api/v1/products

# Get single product
curl http://localhost:8001/api/v1/products/1

# Create order
curl -X POST http://localhost:8002/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product_id": 1, "quantity": 2}]}'

# Chat with AI
curl -X POST http://localhost:8003/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "formal wedding suit"}'
```

---

## Performance Tips

### Backend

1. **Database Optimization**
   - Add indexes on frequently queried columns
   - Use query explain to identify slow queries
   - Connection pooling (default 20, adjust in .env)

2. **Caching**
   - Enable Redis for session storage
   - Cache product catalog (TTL: 1 hour)
   - Cache RAG embeddings (TTL: 24 hours)

3. **Async Operations**
   - Use FastAPI's async/await
   - Queue email notifications (Celery)
   - Background tasks for embeddings

### Frontend

1. **Bundle Optimization**
   - Code splitting on routes
   - Dynamic imports for heavy components
   - Tree shaking (remove unused code)

2. **Image Optimization**
   - Use Next.js Image component
   - WebP format with JPEG fallback
   - Lazy loading for below-fold images

3. **Caching Strategy**
   - SWR for API data
   - Service Worker for offline support
   - Browser cache: max-age=3600

---

## Getting Help

### Documentation
- **Project Plan**: `CLAUDE.md`
- **Deployment**: `DEPLOYMENT.md`
- **API Docs**: http://localhost:8001/docs (Swagger)
- **Database Schema**: `learnflow-app/database/schema.sql`

### Support Channels
- **GitHub Issues**: https://github.com/NAVEED261/Reusable-shop/issues
- **Team Chat**: (specify your team's Slack/Discord)
- **Code Review**: Ask senior developer for code review

### External Resources
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Next.js Docs**: https://nextjs.org/docs
- **Stripe Docs**: https://stripe.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs

---

## Onboarding Checklist

- [ ] Clone repository
- [ ] Set up `.env.backend` and `.env.local`
- [ ] Create virtual environment (Python)
- [ ] Install Python dependencies
- [ ] Install Node dependencies
- [ ] Start PostgreSQL (Docker)
- [ ] Run database migrations
- [ ] Generate embeddings
- [ ] Start backend services
- [ ] Start frontend (npm run dev)
- [ ] Verify health checks (all return 200)
- [ ] Run tests (all pass)
- [ ] Browse to http://localhost:3000
- [ ] Create test product
- [ ] Add to cart
- [ ] Test checkout (use test card)
- [ ] Read CLAUDE.md (understand phases)
- [ ] Read TASKS.md (see current work)
- [ ] Ask questions in team chat!

---

## Next Steps

Once setup is complete:

1. **Review Code**: Read `learnflow-app/app/frontend/app/page.tsx` and `learnflow-app/app/backend/product_service/app/routes.py`
2. **Understand Architecture**: Review `CLAUDE.md` implementation plan
3. **Run Tests**: `pytest tests/ -v && npm test`
4. **Check Status**: See `TASKS.md` for Phase 5 (testing) tasks
5. **Start Contributing**: Pick a task from `TASKS.md` and get started!

---

**Welcome to the team! 🚀**

Questions? Open an issue on GitHub or ask in team chat.

Last Updated: 2026-02-08


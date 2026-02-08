# Phase 6: Production Deployment Runbook

**Project**: Men's Boutique E-Commerce Platform
**Status**: Ready for deployment after Phase 5 completion
**Last Updated**: 2026-02-08

---

## Deployment Overview

This runbook covers all steps to deploy the Men's Boutique platform to production, including frontend, backend services, databases, and observability.

**Timeline**: ~8-12 hours
**Risk Level**: Medium (database migrations, payment integration)
**Rollback Time**: ~30 minutes

---

## Pre-Deployment Checklist

### Phase 5 Completion
- [ ] 95%+ test pass rate confirmed
- [ ] Backend coverage: 70%+
- [ ] Frontend coverage: 60%+
- [ ] All Lighthouse scores ≥90
- [ ] Zero critical security vulnerabilities

### Infrastructure Requirements
- [ ] Domain registered
- [ ] SSL certificate procured
- [ ] Database provider account (Neon, Supabase)
- [ ] Backend platform account (Railway, Render, K8s)
- [ ] Vercel account linked to GitHub
- [ ] Stripe account (live mode keys)
- [ ] SendGrid account (email service)
- [ ] Sentry account (error tracking)

### Team Readiness
- [ ] Deployment lead identified
- [ ] On-call rotation scheduled
- [ ] Incident response plan reviewed
- [ ] Rollback procedure tested
- [ ] Communication plan prepared (Slack, email)

---

## Step 1: Deployment Platform Selection

**Decision Required**: Choose backend deployment platform

### Option A: Railway.app (RECOMMENDED)
**Pros**:
- ✅ Simplest setup (connect GitHub repo)
- ✅ Automatic deployments on git push
- ✅ Built-in logging and monitoring
- ✅ PostgreSQL addon available
- ✅ Qdrant deployment support

**Cons**:
- ❌ Less control over infrastructure
- ❌ Vendor lock-in
- ❌ Limited customization

**Time to Deploy**: 2-3 hours

**Link**: https://railway.app

### Option B: Render.com
**Pros**:
- ✅ Free tier available
- ✅ Simple deployment process
- ✅ Good documentation
- ✅ Auto-deploys from GitHub

**Cons**:
- ❌ Cold starts on free tier
- ❌ Limited monitoring

**Time to Deploy**: 2-3 hours

**Link**: https://render.com

### Option C: Kubernetes (Production Grade)
**Pros**:
- ✅ Full control over infrastructure
- ✅ Horizontal scaling
- ✅ Cost optimization
- ✅ Multi-region capable

**Cons**:
- ❌ Complex setup
- ❌ Requires DevOps expertise
- ❌ Higher infrastructure cost

**Time to Deploy**: 6-8 hours

**Link**: https://kubernetes.io

### **RECOMMENDED**: Railway.app
- Fastest deployment
- Perfect for Phase 6 timeline
- Sufficient for initial launch
- Can migrate to K8s later if needed

---

## Step 2: Database Setup (Neon PostgreSQL)

### 2.1 Create Neon Database
```bash
1. Go to https://neon.tech
2. Sign up / Login
3. Create new project "reusable-shop-prod"
4. Select region: closest to users
5. Tier: Paid (production tier)
6. Copy connection string
```

### 2.2 Configure Environment Variables
```bash
# Backend .env file (keep secret, don't commit)
DATABASE_URL="postgresql://user:password@region.neon.tech/reusable_shop_prod"
DATABASE_POOL_SIZE=20
DATABASE_POOL_TIMEOUT=30
```

### 2.3 Run Database Migrations
```bash
# From local machine
export DATABASE_URL="postgresql://..."
cd learnflow-app/app/backend

# Run Alembic migrations
alembic upgrade head

# Verify schema
psql $DATABASE_URL -c "\dt"
```

### 2.4 Seed Production Data
```bash
# Run seed script
python scripts/seed_products.py --env production

# Verify data
psql $DATABASE_URL -c "SELECT COUNT(*) FROM products;"
# Expected: 40+
```

### 2.5 Configure Backups
```bash
# Neon automatically backs up daily
# Verify in Neon console:
# Settings → Backups → Daily backups enabled
```

---

## Step 3: Qdrant Vector Database Setup

### 3.1 Deploy Qdrant (Docker/Railway)
```bash
# Option 1: Via Railway
# 1. Create new Railway service
# 2. Select Docker from marketplace
# 3. Docker image: qdrant/qdrant:latest
# 4. Expose port 6333
# 5. Set memory limit: 2GB

# Option 2: Self-hosted (K8s)
# See Kubernetes deployment guide
```

### 3.2 Configure Collection
```bash
# Create collection via API
curl -X PUT http://qdrant-host:6333/collections/products \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 1536,
      "distance": "Cosine"
    },
    "optimizers_config": {
      "default_segment_number": 2
    }
  }'
```

### 3.3 Generate & Upload Embeddings
```bash
# From local machine
python scripts/generate_embeddings.py \
  --db-url $DATABASE_URL \
  --qdrant-url http://qdrant-host:6333 \
  --openai-key $OPENAI_API_KEY

# This will:
# - Fetch all 40+ products from database
# - Generate embeddings via OpenAI
# - Upload to Qdrant collection
# Time: ~2-3 minutes
```

### 3.4 Verify Embeddings
```bash
# Test similarity search
curl -X POST http://qdrant-host:6333/collections/products/points/search \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, ...],
    "limit": 5
  }'
```

---

## Step 4: Frontend Deployment (Vercel)

### 4.1 Connect GitHub Repository
```bash
1. Go to vercel.com
2. Sign up / Login
3. Import project from GitHub
4. Select repository: https://github.com/NAVEED261/Reusable-shop
5. Configure build settings:
   - Framework: Next.js
   - Build command: npm run build
   - Output directory: .next
   - Install command: npm install
```

### 4.2 Configure Environment Variables
```bash
# In Vercel dashboard → Settings → Environment Variables

NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_XXXXXX
NEXT_PUBLIC_WHATSAPP_NUMBER=+923331234567
```

### 4.3 Configure Custom Domain
```bash
# In Vercel dashboard → Domains
# Add domain: yourdomain.com
# Update DNS records to Vercel nameservers
# Wait for DNS propagation (24-48 hours)
```

### 4.4 Enable Preview Deployments
```bash
# Settings → Git → Automatic deployments
# ✅ Preview deployments for all branches
# ✅ Production deployments only from main
```

### 4.5 Deploy
```bash
# Push to main branch
git push origin main

# Vercel automatically deploys
# Monitor: vercel.com dashboard

# Verify deployment
curl https://yourdomain.com/api/health
# Should return 200 OK
```

---

## Step 5: Backend Services Deployment (Railway)

### 5.1 Create Railway Project
```bash
1. Go to railway.app
2. Create new project
3. Connect GitHub repository
4. Configure services:
   - Service 1: Product Service
   - Service 2: Order Service
   - Service 3: Chat Service
   - Service 4: Payment Service
   - Service 5: Notification Service
```

### 5.2 Configure Each Service
```bash
# For each service:
# 1. Create Dockerfile (if not exists)
# 2. Configure environment variables:
#    - DATABASE_URL
#    - OPENAI_API_KEY
#    - STRIPE_SECRET_KEY
#    - QDRANT_URL
#    - SERVICE_PORT
# 3. Set resources:
#    - Memory: 512MB minimum
#    - CPU: 0.25 minimum
# 4. Configure health check:
#    - Path: /api/health
#    - Interval: 30s
#    - Timeout: 10s
```

### 5.3 Deploy Services
```bash
# Push to main branch with docker-compose.yml
# Railway automatically detects and builds

# Monitor deployment
# Railway dashboard → Services → Logs

# Verify each service is running
curl https://api.yourdomain.com/api/v1/products
curl https://api.yourdomain.com/api/v1/orders
```

### 5.4 Configure Service-to-Service Communication
```bash
# In Railway dashboard, services can communicate via:
# http://product-service:8000/api/...
# http://order-service:8001/api/...

# Update API_URLS in each service's environment
```

---

## Step 6: Stripe Webhook Configuration

### 6.1 Register Webhook Endpoint
```bash
1. Go to https://dashboard.stripe.com (live mode)
2. Settings → Webhooks
3. Add endpoint: https://api.yourdomain.com/api/webhooks/stripe
4. Events to listen:
   ✅ payment_intent.succeeded
   ✅ payment_intent.payment_failed
   ✅ charge.refunded
5. Copy webhook signing secret
6. Add to environment: STRIPE_WEBHOOK_SECRET=whsec_...
```

### 6.2 Test Webhook
```bash
# Stripe provides webhook testing UI
# Alternatively, test with curl:
curl -X POST https://api.yourdomain.com/api/webhooks/stripe \
  -H "Stripe-Signature: {{signature}}" \
  -d '{...event...}'
```

### 6.3 Test Payment Flow
```bash
# Use Stripe test mode temporarily for verification
# Then switch to live mode

# Test with test card: 4242 4242 4242 4242
# Expected flow:
# 1. Create payment intent → client_secret
# 2. Frontend submits card via Stripe Elements
# 3. Webhook fires → Order created → Email sent
# 4. User sees confirmation page
```

---

## Step 7: Monitoring & Alerting Setup

### 7.1 Centralized Logging (Sentry)
```bash
1. Go to sentry.io
2. Create new project "reusable-shop-prod"
3. Select platform: Python, JavaScript
4. Add Sentry DSN to all services:
   - SENTRY_DSN=https://...@sentry.io/...
5. Configure release tracking
6. Set up error alerts
```

### 7.2 Metrics & Dashboards
```bash
# For Railway: Built-in metrics available
# For other platforms: Integrate Prometheus/Grafana

# Key metrics to monitor:
# - API latency (p50, p95, p99)
# - Error rate (%)
# - Request count (per service)
# - Database connections
# - Memory usage
# - CPU usage
```

### 7.3 Configure Alerting
```bash
# Alert channels:
# 1. Slack (#production-alerts)
# 2. Email (ops@company.com)
# 3. PagerDuty (for P1 incidents)

# Alert rules:
# - Error rate > 1% → P1 (immediate)
# - Latency p95 > 500ms → P2 (15 min)
# - Service down → P1 (immediate)
# - Payment webhook failures → P1 (immediate)
```

### 7.4 Set Up Monitoring Dashboards
```bash
# Create dashboards for:
# 1. System Health
#    - Service status
#    - Uptime percentage
#    - Error rate
# 2. Business Metrics
#    - Transactions processed
#    - Revenue
#    - Cart abandonment
# 3. Performance
#    - API latency
#    - Page load time
#    - Database query time
```

---

## Step 8: Security Hardening

### 8.1 SSL/TLS Configuration
```bash
# Verify HTTPS for all endpoints
curl https://yourdomain.com
# Should have valid certificate

# Test SSL rating
# Go to https://www.ssllabs.com/ssltest/
# Should achieve A+ rating
```

### 8.2 Security Headers
```bash
# Configure in each service's middleware:

# HSTS (HTTP Strict-Transport-Security)
Strict-Transport-Security: max-age=31536000; includeSubDomains

# CSP (Content-Security-Policy)
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' stripe.com

# X-Frame-Options
X-Frame-Options: DENY

# X-Content-Type-Options
X-Content-Type-Options: nosniff
```

### 8.3 Dependency Scanning
```bash
# Run security scan
pip audit  # Python dependencies
npm audit  # JavaScript dependencies

# Fix critical vulnerabilities
pip install --upgrade vulnerable-package
npm update vulnerable-package

# Both should report 0 critical vulnerabilities
```

### 8.4 DDoS Protection
```bash
# For maximum protection, add Cloudflare
# 1. Go to cloudflare.com
# 2. Add domain
# 3. Update DNS nameservers
# 4. Enable DDoS protection
# 5. Configure rate limiting
```

---

## Step 9: Blue-Green Deployment Testing

### 9.1 Set Up Blue Environment (Current Prod)
```bash
# Blue = currently running production
# All users go to blue
```

### 9.2 Set Up Green Environment
```bash
# Green = new version being tested
# Deploy all services to green
# Test endpoints in isolation
```

### 9.3 Automated Smoke Tests
```bash
# Before switching traffic to green:
# Run smoke tests:
# ✅ Homepage loads
# ✅ Product page loads
# ✅ Add to cart works
# ✅ Checkout form submits
# ✅ API endpoints return 200
# ✅ Database connectivity OK

# If any fail → keep blue, investigate green
# If all pass → switch traffic to green
```

### 9.4 Traffic Switch
```bash
# Update load balancer to route to green
# Monitor metrics for 5 minutes
# Expected:
# - No 5xx errors
# - Latency unchanged
# - Error rate <0.5%

# If issues arise:
# Switch back to blue immediately (30s)
```

### 9.5 Rollback Procedure
```bash
# If green deployment fails:
# 1. Switch traffic back to blue (via load balancer)
# 2. Investigate issue in green
# 3. Deploy fix
# 4. Re-test in isolated environment
# 5. Try again with updated green
```

---

## Step 10: Production Validation

### 10.1 Health Checks
```bash
# Verify all services are running:

# Frontend
curl https://yourdomain.com/
# Should return homepage

# Product Service
curl https://api.yourdomain.com/api/v1/products
# Should return product list

# Order Service
curl https://api.yourdomain.com/api/v1/orders
# Should return 200 (require auth)

# Chat Service
curl https://api.yourdomain.com/api/v1/chat/health
# Should return OK

# Payment Service
curl https://api.yourdomain.com/api/v1/payments/health
# Should return OK
```

### 10.2 Critical User Journey Testing
```bash
# Manually test complete flow:
# 1. Browse to https://yourdomain.com
# 2. Search for "cotton shirt"
# 3. Click product
# 4. Add to cart
# 5. Go to checkout
# 6. Enter test address
# 7. Enter test card: 4242 4242 4242 4242
# 8. Submit payment
# 9. Verify order confirmation
# 10. Check email for confirmation
# 11. Verify order in admin dashboard
```

### 10.3 WhatsApp & Chat Testing
```bash
# Test WhatsApp integration
# 1. Open product page
# 2. Click WhatsApp button
# 3. Verify message pre-filled with product name

# Test Chat
# 1. Open chat widget
# 2. Ask "formal wedding suit"
# 3. Verify recommendations returned with product links
```

### 10.4 Performance Validation
```bash
# Run Lighthouse on production
# https://yourdomain.com

# Expected scores:
# Performance: 85-95 (may be lower in production due to real load)
# Accessibility: 95+
# Best Practices: 95+
# SEO: 90+

# Run API load test
# 100 concurrent users, 5 minute duration
# Expected p95 latency: <200ms
# Expected error rate: <0.5%
```

---

## Step 11: Team Training & Handoff

### 11.1 Create Runbooks
```bash
# Document operational procedures:
# - How to scale services
# - How to handle incidents
# - How to investigate errors
# - How to roll back
# - How to view logs
```

### 11.2 Schedule On-Call Rotation
```bash
# Define on-call team
# Week 1: Person A
# Week 2: Person B
# Escalation path:
# Primary → Secondary (after 15 min) → Tech Lead (after 30 min)
```

### 11.3 Alert Configuration Training
```bash
# Train team on:
# - How to view dashboards
# - How to acknowledge alerts
# - How to investigate errors
# - How to document incidents
```

### 11.4 Incident Response Drills
```bash
# Run tabletop exercises:
# "What if X service goes down?"
# Verify rollback procedure works
```

---

## Step 12: Post-Deployment Optimization

### 12.1 Performance Monitoring
```bash
# Track metrics for 1 week:
# - API latency p95
# - Error rate
# - Payment success rate
# - User experience metrics

# Identify slow endpoints
# Optimize queries
# Add caching where needed
```

### 12.2 Cost Optimization
```bash
# Monitor infrastructure costs:
# - Database storage/compute
# - API requests (OpenAI, Stripe)
# - Bandwidth usage
# - Service compute time

# Optimize:
# - Right-size instances
# - Compress data
# - Cache aggressively
# - Batch requests
```

### 12.3 Documentation Updates
```bash
# Create/update:
# - Architecture diagram (with prod URLs)
# - API documentation (with live endpoints)
# - Troubleshooting guide
# - Performance tuning guide
```

---

## Deployment Checklist

### Pre-Deployment (Phase 5 Complete)
- [ ] All tests passing (95%+)
- [ ] Security scan passed (0 critical vulns)
- [ ] Code reviewed
- [ ] Secrets removed from code
- [ ] Git history clean

### Database
- [ ] Neon PostgreSQL created
- [ ] Migrations run successfully
- [ ] Product data seeded (40+)
- [ ] Backups configured
- [ ] Database tested

### Qdrant
- [ ] Qdrant instance deployed
- [ ] Collection created
- [ ] Embeddings generated
- [ ] Similarity search tested

### Frontend
- [ ] Vercel project created
- [ ] GitHub connected
- [ ] Environment variables set
- [ ] Build succeeds
- [ ] Domain configured
- [ ] SSL certificate valid

### Backend Services
- [ ] Railway/Render account created
- [ ] All services deployed
- [ ] Environment variables set
- [ ] Health checks passing
- [ ] Logs visible

### Stripe
- [ ] Live API keys obtained
- [ ] Webhook endpoint registered
- [ ] Webhook signed correctly
- [ ] Test payment successful

### Monitoring
- [ ] Sentry configured
- [ ] Dashboards created
- [ ] Alerts configured
- [ ] On-call rotation ready

### Security
- [ ] SSL/TLS verified (A+)
- [ ] Security headers set
- [ ] DDoS protection enabled
- [ ] No secrets in logs

### Testing
- [ ] Smoke tests passed
- [ ] User journey tested
- [ ] Performance targets met
- [ ] Rollback tested

### Go-Live
- [ ] Team briefed
- [ ] Incident response plan reviewed
- [ ] 24/7 support ready
- [ ] Customer communication prepared

---

## Rollback Procedures

### If Frontend Fails
```bash
# 1. Revert to previous commit
git revert HEAD

# 2. Push to main
git push origin main

# 3. Vercel automatically redeploys
# 4. Verify homepage loads
```

### If Backend Service Fails
```bash
# 1. Option A: Revert code
git revert HEAD
git push origin main

# 2. Option B: Scale to previous version
# Railway dashboard → Service → Previous deployment

# 3. Verify health checks passing
curl https://api.yourdomain.com/api/health

# 4. Monitor metrics for 5 minutes
```

### If Database Fails
```bash
# 1. Restore from latest backup
# Neon dashboard → Backups → Restore

# 2. Verify data integrity
SELECT COUNT(*) FROM products;

# 3. Re-seed if necessary
python scripts/seed_products.py

# 4. Verify service connectivity
```

---

## Success Criteria

- [ ] Frontend live on custom domain
- [ ] All backend services healthy
- [ ] Database functional with data
- [ ] Stripe payments working
- [ ] Logs visible in Sentry
- [ ] Monitoring dashboards active
- [ ] Team trained and ready
- [ ] Incident response plan active
- [ ] All smoke tests passing
- [ ] User journey tested end-to-end

---

## Support & Escalation

### Issues During Deployment
- **Database issues**: Contact Neon support
- **Vercel deployment**: Check build logs, open GitHub issue
- **Railway deployment**: Check service logs, check environment variables
- **Stripe integration**: Contact Stripe support, check webhook logs

### Post-Deployment Support
- **Production issues**: Page ops@company.com and on-call
- **Performance issues**: Check dashboards, scale services if needed
- **Security issues**: Immediately page security lead
- **Data issues**: Restore from backup, investigate root cause

---

**Prepared**: 2026-02-08
**Next Review**: 1 week post-deployment


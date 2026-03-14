# 🚀 DigitalOcean Deployment Guide - Fatima Zehra Boutique

## 🎯 QUICK START - Deploy Backend in 15 Minutes

**Frontend Status**: ✅ **LIVE** - https://frontend-eta-wine-65.vercel.app

**Next Step**: Deploy 4 backend services to DigitalOcean App Platform

---

## 📋 Prerequisites

1. **DigitalOcean Account**: https://cloud.digitalocean.com
   - Create account if you don't have one
   - Add payment method

2. **GitHub Access**:
   - Repository: https://github.com/NAVEED261/Reusable-shop
   - Should have push access

3. **Environment Secrets Ready**:
   - `DATABASE_URL`: `postgresql://neondb_owner:npg_RiFw31LNbBeX@ep-withered-tooth-ahbaotjq-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require`
   - `OPENAI_API_KEY`: `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`
   - `JWT_SECRET`: `bfcdc8ade27118c29423b523292545cd124721ed5a1ea38ea2f3c8ce0b84f73a`
   - Stripe keys (if needed)

---

## 🔧 Deployment Method 1: DigitalOcean App Platform (Recommended)

### Step 1: Create User Service

1. **Open DigitalOcean**: https://cloud.digitalocean.com/apps/new

2. **Connect GitHub Repository**:
   - Click "GitHub" under "Choose your source"
   - Authorize DigitalOcean with GitHub
   - Select repository: `NAVEED261/Reusable-shop`
   - Branch: `main`

3. **Configure Service**:
   - **Name**: `user-service`
   - **Root Directory**: `learnflow-app/app/backend/user-service`
   - **Source Type**: Dockerfile
   - **HTTP Port**: 8000

4. **Set Environment Variables**:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_RiFw31LNbBeX@ep-withered-tooth-ahbaotjq-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   JWT_SECRET=bfcdc8ade27118c29423b523292545cd124721ed5a1ea38ea2f3c8ce0b84f73a
   JWT_ALGORITHM=HS256
   CORS_ORIGINS=https://frontend-eta-wine-65.vercel.app,http://localhost:3000
   ENVIRONMENT=production
   ```

5. **Deploy**:
   - Click "Create Resources"
   - Wait 2-3 minutes for deployment
   - Get URL from "Live App" (e.g., `https://user-service-abc123.ondigitalocean.app`)

### Step 2-4: Repeat for Other Services

**Product Service**:
- Root Directory: `learnflow-app/app/backend/product-service`
- Env vars: DATABASE_URL, CORS_ORIGINS
- Result URL: `https://product-service-abc123.ondigitalocean.app`

**Order Service**:
- Root Directory: `learnflow-app/app/backend/order-service`
- Env vars: DATABASE_URL, CORS_ORIGINS, STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET
- Result URL: `https://order-service-abc123.ondigitalocean.app`

**Chat Service**:
- Root Directory: `learnflow-app/app/backend/chat-service`
- Env vars: DATABASE_URL, CORS_ORIGINS, OPENAI_API_KEY, QDRANT_HOST, QDRANT_PORT
- Result URL: `https://chat-service-abc123.ondigitalocean.app`

---

## 📝 Step 3: Update Frontend Environment Variables

After all backend services are deployed, update Vercel:

1. Go to: https://vercel.com/naveeds-projects-04d1df6d/settings/environment-variables

2. Update variables with actual DigitalOcean URLs:
   ```
   NEXT_PUBLIC_USER_SERVICE_URL=https://user-service-abc123.ondigitalocean.app/api
   NEXT_PUBLIC_PRODUCT_SERVICE_URL=https://product-service-abc123.ondigitalocean.app/api
   NEXT_PUBLIC_ORDER_SERVICE_URL=https://order-service-abc123.ondigitalocean.app/api
   NEXT_PUBLIC_CHAT_SERVICE_URL=https://chat-service-abc123.ondigitalocean.app/api
   ```

3. **Redeploy Frontend**:
   - Go to Vercel dashboard
   - Click "Deployments"
   - Click "..." on latest deployment
   - Click "Redeploy"

---

## ✅ Verification Checklist

### Backend Health Checks

```bash
# Test each service health endpoint
curl https://user-service-abc123.ondigitalocean.app/health
curl https://product-service-abc123.ondigitalocean.app/health
curl https://order-service-abc123.ondigitalocean.app/health
curl https://chat-service-abc123.ondigitalocean.app/health

# All should return: {"status":"ok"}
```

### Product API Test

```bash
curl https://product-service-abc123.ondigitalocean.app/api/products | jq '.[] | {id, name, price}' | head -20
```

### Full Stack Test

1. Go to **https://frontend-eta-wine-65.vercel.app**
2. Click on any product
3. Click "Add to Cart"
4. Go to Cart
5. Try checkout (test card: 4242 4242 4242 4242)
6. Click chat widget and ask: "Show me fancy suits under Rs 10000"

---

## 🔐 Post-Deployment Configuration

### 1. Stripe Webhooks

1. Go to https://dashboard.stripe.com → **Webhooks**
2. Click "Add an endpoint"
3. **Endpoint URL**: `https://order-service-abc123.ondigitalocean.app/api/payments/webhook`
4. **Events**: Select `payment_intent.succeeded`, `payment_intent.payment_failed`
5. Copy the signing secret
6. Update DigitalOcean env var: `STRIPE_WEBHOOK_SECRET=whsec_...`

### 2. CORS Configuration

Verify CORS is configured in each service to allow Vercel domain:
- All services should have `CORS_ORIGINS=https://frontend-eta-wine-65.vercel.app`

### 3. Qdrant Vector Database Setup

For Chat RAG to work:

**Option A: Qdrant Cloud (Easiest)**
1. Go to https://cloud.qdrant.io
2. Create account and cluster
3. Get URL and API key
4. Update Chat Service env vars:
   ```
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-api-key
   ```

**Option B: DigitalOcean Kubernetes (Advanced)**
1. Create Kubernetes cluster
2. Deploy Qdrant using Helm
3. Expose service and get URL

**Option C: Self-Hosted (Simple)**
```bash
# SSH into a DigitalOcean droplet
docker run -d -p 6333:6333 qdrant/qdrant

# Update Chat Service:
QDRANT_URL=http://droplet-ip:6333
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────┐
│   Frontend (Vercel)                  │
│   https://frontend-eta-wine-65.     │
│   vercel.app                         │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
┌───────▼────────┐ ┌─────────────────┐
│ Backend (DO)   │ │ Database (Neon) │
├────────────────┤ └─────────────────┘
│ User Service   │
│ Product Service│      ┌──────────────┐
│ Order Service  │──────│ Qdrant Cloud │
│ Chat Service   │      │ (Vector DB)  │
└────────────────┘      └──────────────┘
```

---

## 🚨 Troubleshooting

### Service Fails to Build

**Problem**: Build fails on DigitalOcean
```
Error: Could not find requirements.txt
```

**Solution**:
- Verify Root Directory is correct
- Check Dockerfile exists in that directory
- Ensure you're pointing to correct branch (main)

### CORS Errors in Browser

**Problem**: Frontend can't reach backend
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution**:
- Update `CORS_ORIGINS` in each service to include Vercel URL
- Commit changes to GitHub
- DigitalOcean will auto-redeploy

### Database Connection Failed

**Problem**: Backend can't connect to database
```
Database connection failed: could not connect to server
```

**Solution**:
- Verify DATABASE_URL is correct
- Check Neon database is accessible
- Ensure whitelist includes DigitalOcean IP (usually not needed with `?sslmode=require`)

---

## 💰 Cost Estimate

| Service | Cost/Month |
|---------|-----------|
| Frontend (Vercel) | Free |
| 4x Backend (DigitalOcean) | $6-12 |
| Database (Neon) | Free (up to 1GB) |
| Qdrant Cloud | Free (up to 1GB) |
| **Total** | **$6-12/month** |

---

## 📞 Support

### Quick Links
- GitHub Repo: https://github.com/NAVEED261/Reusable-shop
- DigitalOcean Docs: https://docs.digitalocean.com/products/app-platform/
- Vercel Docs: https://vercel.com/docs

### Environment Details
- Frontend: Next.js 16 (static export)
- Backend: FastAPI (Python 3.10+)
- Database: PostgreSQL 15 (Neon)
- Vector DB: Qdrant (1536-dimensional embeddings)

---

## ✨ Expected Final Result

After completing all steps, you should have:

**Frontend**: ✅ https://frontend-eta-wine-65.vercel.app
- Browse products
- Add to cart
- User authentication
- Chat with AI
- WhatsApp integration

**Backend**: ✅ Four services on DigitalOcean
- User authentication & JWT
- Product catalog (40 items)
- Shopping cart & Stripe checkout
- AI chat with RAG + product recommendations

**Database**: ✅ Neon PostgreSQL
- All tables created
- 40 products seeded
- Chat history stored
- Order records tracked

**Complete Full-Stack E-Commerce Platform**: ✅

---

**Next Action**: Follow the 4 deployment steps above and update this document with your actual DigitalOcean app URLs.

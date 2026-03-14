#!/bin/bash
# Deployment Script - Automates Vercel and Database Setup
# Usage: bash scripts/deploy.sh

set -e  # Exit on error

echo "🚀 Fatima Zehra Boutique - Deployment Script"
echo "=============================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v git &> /dev/null || { echo "❌ Git not found"; exit 1; }
command -v python3 &> /dev/null || { echo "❌ Python3 not found"; exit 1; }
echo "✅ Git and Python3 found"
echo ""

# Step 1: Git setup
echo "📦 Step 1: Git Configuration"
echo "----------------------------"
read -p "Have you set up GitHub auth? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please setup GitHub SSH or HTTPS authentication first:"
    echo "https://docs.github.com/en/get-started/getting-started-with-git"
    exit 1
fi

# Step 2: Database setup
echo ""
echo "🗄️  Step 2: Database Setup"
echo "------------------------"
read -p "Enter your Neon PostgreSQL connection string: " DATABASE_URL

if [ -z "$DATABASE_URL" ]; then
    echo "❌ Database URL is required"
    exit 1
fi

echo "Testing database connection..."
python3 -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null && echo "✅ Database connection successful" || {
    echo "❌ Failed to connect to database"
    exit 1
}

# Step 3: Seed database
echo ""
echo "🌱 Step 3: Seeding Products"
echo "---------------------------"
export DATABASE_URL="$DATABASE_URL"
python3 scripts/seed_products.py

# Step 4: Git commit
echo ""
echo "📝 Step 4: Git Commit"
echo "--------------------"
git add -A
git commit -m "feat: Complete full-stack deployment with 3D logo, database seeding, and APIs"
git push origin master
echo "✅ Pushed to GitHub"

# Step 5: Vercel setup
echo ""
echo "🌐 Step 5: Vercel Deployment"
echo "----------------------------"
echo ""
echo "Next steps:"
echo "1. Open https://vercel.com/new"
echo "2. Import: https://github.com/NAVEED261/Reusable-shop"
echo "3. Configure project:"
echo "   - Framework: Next.js"
echo "   - Build: cd learnflow-app/app/frontend && npm run build"
echo "   - Output: learnflow-app/app/frontend/.next"
echo ""
echo "4. Add environment variables:"
echo "   DATABASE_URL=$DATABASE_URL"
echo "   NEXT_PUBLIC_API_URL=https://your-vercel-app.vercel.app"
echo "   OPENAI_API_KEY=sk-xxx"
echo "   JWT_SECRET=your-secret"
echo ""
echo "5. Click Deploy and wait 5-10 minutes"
echo ""

read -p "Have you deployed to Vercel? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your Vercel production URL: " VERCEL_URL

    if [ -z "$VERCEL_URL" ]; then
        echo "❌ Vercel URL is required"
        exit 1
    fi

    echo ""
    echo "✅ Testing deployment..."

    # Test endpoints
    echo ""
    echo "Testing API endpoints..."

    curl -s "$VERCEL_URL" > /dev/null && echo "✅ Homepage responsive" || echo "⚠️  Homepage check failed"
    curl -s "$VERCEL_URL/api/products" > /dev/null && echo "✅ Products API working" || echo "⚠️  Products API check failed"

    echo ""
    echo "🎉 Deployment Summary"
    echo "====================
    echo "Frontend: $VERCEL_URL"
    echo "Products: $VERCEL_URL/api/products"
    echo "Chat: $VERCEL_URL/api/chat"
    echo ""
    echo "✨ Verify these in browser:"
    echo "1. 3D animated logo in navbar"
    echo "2. About page with hero image"
    echo "3. Chat widget responds to messages"
    echo "4. Products load from database"
    echo ""
else
    echo "Please complete Vercel deployment and run this script again."
fi

echo ""
echo "📚 Full documentation: cat DEPLOYMENT_GUIDE.md"
echo "🚀 Deployment complete!"

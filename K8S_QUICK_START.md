# Kubernetes Deployment - Quick Start Guide

## 🚀 Deploy in 5 Minutes

### Step 1: Build Images
```bash
cd learnflow-app

docker build -t boutique-user-service:latest ./app/backend/user-service
docker build -t boutique-product-service:latest ./app/backend/product-service
docker build -t boutique-order-service:latest ./app/backend/order-service
docker build -t boutique-chat-service:latest ./app/backend/chat-service
docker build -t boutique-frontend:latest ./app/frontend
```

### Step 2: Update Secrets
Edit `learnflow-app/k8s/config/07-secrets.yaml` and replace:
- `OPENAI_API_KEY` → Your OpenAI key
- `STRIPE_SECRET_KEY` → Your Stripe secret
- `STRIPE_WEBHOOK_SECRET` → Your Stripe webhook secret

### Step 3: Deploy
```bash
# Single command to deploy everything
kubectl apply -k learnflow-app/k8s/

# Watch deployment
kubectl get pods -n boutique-shop -w
```

### Step 4: Verify
```bash
# Run verification script
chmod +x learnflow-app/k8s/verify-deployment.sh
./learnflow-app/k8s/verify-deployment.sh

# Expected: All checks pass ✓
```

### Step 5: Access
```bash
# Get node IP
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')

# Open in browser
http://${NODE_IP}:30080
```

Or port-forward for local testing:
```bash
kubectl port-forward -n boutique-shop svc/nginx-service 8080:80
# Then: http://localhost:8080
```

---

## 📋 What Gets Deployed

| Component | Type | Replicas | Port |
|-----------|------|----------|------|
| PostgreSQL | StatefulSet | 1 | 5432 |
| Qdrant | StatefulSet | 1 | 6333 |
| User Service | Deployment | 2 | 8000 |
| Product Service | Deployment | 2 | 8000 |
| Order Service | Deployment | 2 | 8000 |
| Chat Service | Deployment | 2 | 8000 |
| Frontend | Deployment | 2 | 3000 |
| NGINX Gateway | Deployment | 2 | 80 (NodePort 30080) |

**Total**: 1 namespace, 5 roles, 2 statefulsets, 6 deployments, 8 services

---

## 🔧 Common Commands

### View Resources
```bash
# All resources in namespace
kubectl get all -n boutique-shop

# Specific resource type
kubectl get pods -n boutique-shop
kubectl get deployments -n boutique-shop
kubectl get services -n boutique-shop
```

### View Logs
```bash
# Single deployment
kubectl logs -n boutique-shop deploy/user-service

# Follow logs (live)
kubectl logs -f -n boutique-shop deploy/user-service

# Specific pod
kubectl logs -n boutique-shop user-service-abc123-xyz
```

### Scale Services
```bash
# Scale to 3 replicas
kubectl scale deployment user-service --replicas=3 -n boutique-shop
```

### Debug Pod
```bash
# Connect to pod
kubectl exec -it -n boutique-shop <pod-name> -- /bin/sh

# Check pod details
kubectl describe pod -n boutique-shop <pod-name>
```

### Update Configuration
```bash
# Update ConfigMap
kubectl patch configmap boutique-config -n boutique-shop --type merge \
  -p '{"data":{"LOG_LEVEL":"debug"}}'

# Update image
kubectl set image deployment/user-service \
  user-service=boutique-user-service:v2 \
  -n boutique-shop
```

---

## ✅ Verification Checklist

Quick verification without script:
```bash
# Namespace exists and is active
kubectl get ns boutique-shop

# All pods running
kubectl get pods -n boutique-shop
# Expected: All pods = Running (0 errors)

# Services have endpoints
kubectl get endpoints -n boutique-shop
# Expected: All services listed with IP:port

# NGINX accessible
curl http://<NODE_IP>:30080/health
# Expected: OK

# Database works
kubectl exec -n boutique-shop postgres-0 -- pg_isready -U postgres
# Expected: "accepting connections"
```

---

## 🚨 Troubleshooting

### Pod stuck in CrashLoopBackOff
```bash
# Check logs
kubectl logs -n boutique-shop <pod-name> --previous

# Check events
kubectl describe pod -n boutique-shop <pod-name>
```

### Cannot access application
```bash
# Check NGINX service
kubectl get svc -n boutique-shop nginx-service

# Check if NGINX pod is running
kubectl get pod -n boutique-shop -l app=nginx

# Port-forward if NodePort not accessible
kubectl port-forward -n boutique-shop svc/nginx-service 8080:80
```

### Database not ready
```bash
# Check postgres pod logs
kubectl logs -n boutique-shop postgres-0

# Check if PVC is bound
kubectl get pvc -n boutique-shop
```

### Service connectivity issues
```bash
# Test DNS from within cluster
kubectl exec -it -n boutique-shop <pod-name> -- \
  nslookup postgres-service

# Test service port
kubectl exec -it -n boutique-shop <pod-name> -- \
  curl http://postgres-service:5432
```

---

## 📚 Full Documentation

For detailed information, see:
- **`learnflow-app/k8s/README.md`** - Complete deployment guide
- **`KUBERNETES_DEPLOYMENT.md`** - Phase-by-phase instructions
- **`KUBERNETES_IMPLEMENTATION_SUMMARY.md`** - Technical overview
- **`learnflow-app/k8s/verify-deployment.sh`** - Automated verification script

---

## 🔑 Key Files

```
learnflow-app/k8s/
├── 00-namespace.yaml              # Start here
├── rbac/                          # 5 RBAC files
├── config/                        # ConfigMap + Secrets
├── storage/                       # PersistentVolumeClaims
├── workloads/                     # 8 service files
├── kustomization.yaml             # Deployment orchestration
├── README.md                      # Full guide
└── verify-deployment.sh           # Verification script
```

---

## 🎯 Next Steps After Deployment

1. **Initialize Database**
   ```bash
   kubectl exec postgres-0 -- psql -U postgres < migrations.sql
   ```

2. **Seed Data**
   ```bash
   kubectl exec postgres-0 -- psql -U postgres boutique_shop < sample_products.sql
   ```

3. **Generate Embeddings** (for RAG)
   ```bash
   kubectl exec -it chat-service-0 -- python scripts/generate_embeddings.py
   ```

4. **Monitor Health**
   ```bash
   kubectl get pods -n boutique-shop -w
   kubectl top pods -n boutique-shop
   ```

5. **View Logs**
   ```bash
   kubectl logs -n boutique-shop -l app.kubernetes.io/name=boutique-shop --tail=50
   ```

---

## 📊 Expected Resource Usage

- **CPU**: ~1.1 cores (requests)
- **Memory**: ~1.66 GB (requests)
- **Storage**: 8 GB total (5GB postgres + 3GB qdrant)
- **Network**: <100 Mbps (typical)

---

## 🔒 Security Notes

- ✅ RBAC enforced (dev team can't access secrets)
- ✅ Non-root containers (security context set)
- ✅ Secrets base64-encoded (not plaintext)
- ✅ Network security headers enabled
- ✅ No privilege escalation allowed

---

## 📞 Need Help?

1. Run verification script: `./learnflow-app/k8s/verify-deployment.sh`
2. Check logs: `kubectl logs -n boutique-shop <pod>`
3. View events: `kubectl get events -n boutique-shop -w`
4. Read full guide: `learnflow-app/k8s/README.md`

---

## 🚀 One-Line Deployment

For experienced users (after building images and updating secrets):
```bash
kubectl apply -k learnflow-app/k8s/ && sleep 5 && ./learnflow-app/k8s/verify-deployment.sh
```

---

**Status**: ✅ Ready to Deploy

**Version**: 1.0.0 | Created: 2026-03-14

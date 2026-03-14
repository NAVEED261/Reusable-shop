# Kubernetes Production Deployment Guide

## 📌 Complete Implementation Summary

This guide provides step-by-step instructions for deploying the Men's Boutique E-Commerce Platform to Kubernetes with full RBAC, persistent storage, and production-grade configurations.

---

## 🎯 What Was Created

### 20 Kubernetes Manifest Files (Complete Stack)

#### **1. Namespace (1 file)**
- `k8s/00-namespace.yaml` — `boutique-shop` namespace with production labels

#### **2. RBAC (5 files)**
- `k8s/rbac/01-serviceaccount.yaml` — Service account + long-lived token
- `k8s/rbac/02-role.yaml` — App role (configmaps, secrets, pods, services)
- `k8s/rbac/03-rolebinding.yaml` — Bind app role to service account
- `k8s/rbac/04-devuser-role.yaml` — Dev team read-only role
- `k8s/rbac/05-devuser-rolebinding.yaml` — Bind dev role to dev-user

#### **3. Configuration (2 files)**
- `k8s/config/06-configmap.yaml` — Non-sensitive env vars
- `k8s/config/07-secrets.yaml` — Sensitive secrets (base64-encoded) + placeholders

#### **4. Storage (2 files)**
- `k8s/storage/08-postgres-pvc.yaml` — PostgreSQL 5Gi persistent volume
- `k8s/storage/09-qdrant-pvc.yaml` — Qdrant 3Gi persistent volume

#### **5. Stateful Services (2 files)**
- `k8s/workloads/10-postgres-statefulset.yaml` — PostgreSQL + ClusterIP Service
- `k8s/workloads/11-qdrant-statefulset.yaml` — Qdrant vector DB + Service

#### **6. Microservices (4 files)**
- `k8s/workloads/12-user-service.yaml` — User auth service (2 replicas)
- `k8s/workloads/13-product-service.yaml` — Product catalog (2 replicas)
- `k8s/workloads/14-order-service.yaml` — Orders + Stripe (2 replicas)
- `k8s/workloads/15-chat-service.yaml` — Chat + RAG system (2 replicas)

#### **7. Frontend & Gateway (2 files)**
- `k8s/workloads/16-frontend.yaml` — Next.js frontend (2 replicas)
- `k8s/workloads/17-nginx.yaml` — API gateway + NodePort (2 replicas)

#### **8. Orchestration (1 file)**
- `k8s/kustomization.yaml` — Kustomize deployment configuration (ordered apply)

#### **9. Documentation (1 file)**
- `k8s/README.md` — Complete deployment guide

---

## 🚀 Deployment Instructions

### Phase 1: Prerequisites (15 mins)

#### 1.1 Verify Kubernetes Cluster

```bash
# Check cluster version (1.24+ required)
kubectl version --short

# Check node status
kubectl get nodes

# Expected output: At least 1 node in Ready state
```

#### 1.2 Build Docker Images

```bash
cd learnflow-app

# Build all 5 custom images
docker build -t boutique-user-service:latest ./app/backend/user-service
docker build -t boutique-product-service:latest ./app/backend/product-service
docker build -t boutique-order-service:latest ./app/backend/order-service
docker build -t boutique-chat-service:latest ./app/backend/chat-service
docker build -t boutique-frontend:latest ./app/frontend

# Verify images
docker images | grep boutique
```

#### 1.3 Load Images (Minikube Only)

If using Minikube, load images:

```bash
minikube image load boutique-user-service:latest
minikube image load boutique-product-service:latest
minikube image load boutique-order-service:latest
minikube image load boutique-chat-service:latest
minikube image load boutique-frontend:latest

# Verify
minikube image ls | grep boutique
```

### Phase 2: Prepare Secrets (10 mins)

#### 2.1 Update `k8s/config/07-secrets.yaml`

Edit the file and replace these placeholder values:

```yaml
stringData:
  OPENAI_API_KEY: "sk-YOUR-OPENAI-KEY-HERE"  # Get from OpenAI dashboard
  STRIPE_SECRET_KEY: "sk_live_YOUR-KEY-HERE"  # Get from Stripe dashboard
  STRIPE_WEBHOOK_SECRET: "whsec_YOUR-SECRET-HERE"  # Get from Stripe webhooks
```

**Where to get keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **Stripe Secret**: https://dashboard.stripe.com/apikeys
- **Stripe Webhook**: https://dashboard.stripe.com/webhooks

#### 2.2 (Optional) Pre-create Secret

```bash
# Instead of updating YAML, create secret directly
kubectl create secret generic boutique-secrets -n boutique-shop \
  --from-literal=OPENAI_API_KEY="sk_xxx" \
  --from-literal=STRIPE_SECRET_KEY="sk_live_xxx" \
  --from-literal=STRIPE_WEBHOOK_SECRET="whsec_xxx" \
  --from-literal=POSTGRES_PASSWORD="postgres" \
  --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres-service:5432/boutique_shop" \
  --from-literal=JWT_SECRET="$(openssl rand -hex 32)" \
  --dry-run=client -o yaml | kubectl apply -f -
```

### Phase 3: Deploy to Kubernetes (5 mins)

#### 3.1 Deploy All Resources

```bash
# Single command: Deploy all manifests in order
kubectl apply -k learnflow-app/k8s/

# Expected output:
# namespace/boutique-shop created
# serviceaccount/boutique-sa created
# role.rbac.authorization.k8s.io/boutique-app-role created
# ... (many more resources)
```

#### 3.2 Watch Deployment Progress

```bash
# Terminal 1: Watch pod creation
kubectl get pods -n boutique-shop -w

# Terminal 2: Watch events
kubectl get events -n boutique-shop -w --sort-by='.lastTimestamp'

# Terminal 3: Monitor resources
kubectl top pods -n boutique-shop -w
```

### Phase 4: Verification (10-15 mins)

#### 4.1 Verify All Resources Created

```bash
# Check namespace
kubectl get ns boutique-shop
# Expected: STATUS = Active

# Check RBAC
kubectl get sa,role,rolebinding -n boutique-shop
# Expected: 1 ServiceAccount, 2 Roles, 2 RoleBindings

# Check storage
kubectl get pvc -n boutique-shop
# Expected: Both PVCs = Bound

# Check stateful services
kubectl get statefulsets -n boutique-shop
# Expected: postgres, qdrant = 1/1 Ready

# Check microservices
kubectl get deployments -n boutique-shop
# Expected: All = 2/2 Ready

# Check services
kubectl get services -n boutique-shop
# Expected: 8 services listed
```

#### 4.2 Detailed Verification Checklist

```bash
# ✅ Namespace active
kubectl get ns boutique-shop

# ✅ RBAC configured
kubectl get role,rolebinding -n boutique-shop

# ✅ ConfigMap created
kubectl get configmap boutique-config -n boutique-shop -o yaml | head -20

# ✅ Secrets created
kubectl get secret boutique-secrets -n boutique-shop

# ✅ PVCs bound
kubectl get pvc -n boutique-shop

# ✅ PostgreSQL running
kubectl get statefulset postgres -n boutique-shop
kubectl logs -n boutique-shop postgres-0 | tail -10

# ✅ Qdrant running
kubectl get statefulset qdrant -n boutique-shop
kubectl logs -n boutique-shop qdrant-0 | tail -10

# ✅ Services ready
kubectl get svc -n boutique-shop

# ✅ All pods running
kubectl get pods -n boutique-shop
# Expected: All pods = Running (no CrashLoopBackOff)

# ✅ Endpoints configured
kubectl get endpoints -n boutique-shop
```

#### 4.3 Verify Health Checks

```bash
# Test PostgreSQL health
kubectl exec -n boutique-shop postgres-0 -- pg_isready -U postgres
# Expected: "accepting connections"

# Test Qdrant health
kubectl exec -n boutique-shop qdrant-0 -- curl -s http://localhost:6333/health | jq .
# Expected: JSON with status

# Test service connectivity
POD=$(kubectl get pods -n boutique-shop -l app=user-service -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n boutique-shop $POD -- curl -s http://postgres-service:5432
# Expected: TCP connection works (or connection refused message, not timeout)
```

### Phase 5: Access the Application (5 mins)

#### 5.1 Get Node Information

```bash
# Find node IP
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')

# If ExternalIP is empty, use InternalIP
if [ -z "$NODE_IP" ]; then
  NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
fi

echo "Node IP: $NODE_IP"
echo "Application URL: http://$NODE_IP:30080"
```

#### 5.2 Test Application

```bash
# Test NGINX gateway health
curl http://$NODE_IP:30080/health
# Expected: OK

# Test API user service
curl http://$NODE_IP:30080/api/users/health
# Expected: 200 OK or service response

# Test product service
curl http://$NODE_IP:30080/api/products/health
# Expected: 200 OK or service response
```

#### 5.3 Port Forward (Alternative for Local Testing)

```bash
# Forward local port to NGINX service
kubectl port-forward -n boutique-shop svc/nginx-service 8080:80

# In another terminal, access application
open http://localhost:8080
# or
curl http://localhost:8080/health
```

---

## 📋 Verification Checklist

### Namespace & RBAC
- [ ] `kubectl get ns boutique-shop` → Active
- [ ] `kubectl get sa -n boutique-shop boutique-sa` → Exists
- [ ] `kubectl get secret boutique-sa-token -n boutique-shop` → Contains token
- [ ] `kubectl get role -n boutique-shop` → 2 roles exist
- [ ] `kubectl get rolebinding -n boutique-shop` → 2 rolebindings exist

### Configuration & Secrets
- [ ] `kubectl get configmap -n boutique-shop` → boutique-config exists
- [ ] `kubectl get secret -n boutique-shop` → boutique-secrets exists
- [ ] `kubectl get configmap boutique-config -n boutique-shop -o yaml` → All values present
- [ ] `kubectl get secret boutique-secrets -n boutique-shop -o yaml` → All keys present

### Storage
- [ ] `kubectl get pvc postgres-pvc -n boutique-shop` → Bound
- [ ] `kubectl get pvc qdrant-pvc -n boutique-shop` → Bound
- [ ] `kubectl get pv` → 2 PVs in use (if dynamic provisioning)

### Stateful Services
- [ ] `kubectl get statefulset postgres -n boutique-shop` → 1/1 Ready
- [ ] `kubectl get statefulset qdrant -n boutique-shop` → 1/1 Ready
- [ ] `kubectl get pod postgres-0 -n boutique-shop` → Running
- [ ] `kubectl get pod qdrant-0 -n boutique-shop` → Running

### Microservices
- [ ] `kubectl get deployment user-service -n boutique-shop` → 2/2 Ready
- [ ] `kubectl get deployment product-service -n boutique-shop` → 2/2 Ready
- [ ] `kubectl get deployment order-service -n boutique-shop` → 2/2 Ready
- [ ] `kubectl get deployment chat-service -n boutique-shop` → 2/2 Ready
- [ ] `kubectl get deployment frontend -n boutique-shop` → 2/2 Ready
- [ ] `kubectl get deployment nginx -n boutique-shop` → 2/2 Ready

### Services & Networking
- [ ] `kubectl get svc -n boutique-shop` → All 8 services listed
- [ ] `kubectl get svc nginx-service -n boutique-shop` → NodePort 30080
- [ ] `kubectl get endpoints -n boutique-shop` → All endpoints populated

### Application Functionality
- [ ] `curl http://$NODE_IP:30080/health` → OK
- [ ] Frontend loads at `http://$NODE_IP:30080`
- [ ] Can navigate product pages
- [ ] Chat service responds
- [ ] Database operations work

---

## 🔧 Common Operations

### View Logs

```bash
# Entire deployment
kubectl logs -n boutique-shop deploy/user-service

# Specific pod
kubectl logs -n boutique-shop user-service-abc123-xyz

# Follow logs (live)
kubectl logs -f -n boutique-shop deploy/user-service

# Previous logs (if crashed)
kubectl logs -n boutique-shop pod/user-service-xyz --previous

# All logs in namespace
kubectl logs -n boutique-shop --all-containers=true -l app.kubernetes.io/name=boutique-shop
```

### Scale Deployments

```bash
# Scale to 3 replicas
kubectl scale deployment user-service --replicas=3 -n boutique-shop

# View current replicas
kubectl get deployment user-service -n boutique-shop
```

### Update Configuration

```bash
# Update non-sensitive config
kubectl patch configmap boutique-config -n boutique-shop --type merge \
  -p '{"data":{"LOG_LEVEL":"debug"}}'

# Update secrets
kubectl patch secret boutique-secrets -n boutique-shop --type merge \
  -p '{"stringData":{"OPENAI_API_KEY":"sk-new-key"}}'

# Force pod restart (to pick up config changes)
kubectl rollout restart deployment/user-service -n boutique-shop
```

### Rolling Updates

```bash
# Update image
kubectl set image deployment/user-service \
  user-service=boutique-user-service:v2 \
  -n boutique-shop

# Check rollout status
kubectl rollout status deployment/user-service -n boutique-shop -w

# Undo rollout
kubectl rollout undo deployment/user-service -n boutique-shop
```

### Debug Pod Issues

```bash
# Describe pod (show events)
kubectl describe pod -n boutique-shop <pod-name>

# SSH into pod
kubectl exec -it -n boutique-shop <pod-name> -- /bin/sh

# Test connectivity
kubectl exec -it -n boutique-shop <pod-name> -- nslookup postgres-service
kubectl exec -it -n boutique-shop <pod-name> -- curl http://postgres-service:5432
```

---

## 🚨 Troubleshooting

### Pods stuck in CrashLoopBackOff

```bash
# Check logs
kubectl logs -n boutique-shop <pod-name> --previous

# Common causes:
# 1. Missing environment variable → Check ConfigMap/Secret
# 2. Database not ready → Check postgres-0 logs
# 3. Image not found → Check imagePullPolicy and image name
# 4. Port conflict → Check if service is running on expected port
```

### PVC not binding

```bash
# Check PVC status
kubectl describe pvc -n boutique-shop postgres-pvc

# Common causes:
# 1. No available PV → Check storage class
# 2. AccessMode mismatch → Must be ReadWriteOnce
# 3. Storage class missing → Create or use 'standard' class
```

### Service not accessible

```bash
# Check service endpoints
kubectl get endpoints -n boutique-shop nginx-service

# If empty, pods are not ready
# Check pod status and logs

# Test DNS resolution
kubectl exec -it -n boutique-shop <pod-name> -- nslookup nginx-service
```

### Database connection errors

```bash
# Verify postgres is running
kubectl exec -n boutique-shop postgres-0 -- pg_isready -U postgres

# Check database exists
kubectl exec -n boutique-shop postgres-0 -- psql -U postgres -l

# Connect to database
kubectl exec -it -n boutique-shop postgres-0 -- psql -U postgres boutique_shop
```

---

## 📊 Resource Requirements

### Recommended Cluster Size

| Cluster Type | Min Nodes | Min Total | Recommended |
|--------------|-----------|-----------|-------------|
| Development | 1 | 2 CPU, 4GB RAM | 2 CPU, 4GB RAM |
| Staging | 2 | 4 CPU, 8GB RAM | 4 CPU, 8GB RAM |
| Production | 3 | 8 CPU, 16GB RAM | 16 CPU, 32GB RAM |

### Pod Resource Allocation

| Service | Requests | Limits |
|---------|----------|--------|
| PostgreSQL | 256m/250m | 512m/500m |
| Qdrant | 512m/250m | 1Gi/500m |
| Microservices (each) | 128m/100m | 512m/500m |
| Frontend | 128m/100m | 256m/300m |
| NGINX | 64m/50m | 128m/200m |
| **Total** | **~3.5 CPU / 2.8 GB** | **~5.5 CPU / 5.5 GB** |

---

## 🔒 Security Best Practices

### Implemented
- ✅ RBAC enforced (no secrets for dev team)
- ✅ Security context (non-root, read-only filesystems)
- ✅ Service account isolation
- ✅ Secret management (base64 encoded)
- ✅ Network security headers in NGINX

### Additional Recommendations
- [ ] Enable Pod Security Policy
- [ ] Use private container registry
- [ ] Implement Network Policy
- [ ] Enable audit logging
- [ ] Use external secret management (HashiCorp Vault, AWS Secrets Manager)
- [ ] Enable TLS/HTTPS with cert-manager
- [ ] Implement image scanning for vulnerabilities
- [ ] Set resource limits to prevent DoS

---

## 📚 Next Steps

1. **Access the Application**
   - Get node IP: `kubectl get nodes -o wide`
   - Open browser: `http://<NODE_IP>:30080`

2. **Initialize Database**
   - Run migrations: `kubectl exec postgres-0 -- psql -U postgres < migrations.sql`
   - Seed data: `kubectl exec postgres-0 -- psql -U postgres boutique_shop < sample_products.sql`

3. **Generate Embeddings** (for RAG system)
   - `kubectl exec -it chat-service-0 -- python scripts/generate_embeddings.py`

4. **Monitor & Scale**
   - Set up Prometheus for metrics
   - Configure HPA for auto-scaling
   - Enable log aggregation (ELK, Loki)

5. **Production Hardening**
   - Set up Ingress with TLS
   - Configure backup strategy
   - Implement disaster recovery
   - Enable monitoring and alerting

---

## 📞 Support

- **Logs**: `kubectl logs -n boutique-shop <resource>`
- **Events**: `kubectl get events -n boutique-shop -w`
- **Describe**: `kubectl describe <resource-type> -n boutique-shop <name>`
- **Docs**: See `learnflow-app/k8s/README.md`

---

**Version**: 1.0.0
**Created**: 2026-03-14
**Last Updated**: 2026-03-14

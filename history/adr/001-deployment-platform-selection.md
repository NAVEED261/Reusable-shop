# ADR 001: Deployment Platform Selection

**Status**: APPROVED
**Date**: 2026-02-08
**Deciders**: NAVEED261 (Project Lead)
**Implements**: Phase 6 (Production Deployment)

---

## Context

The Men's Boutique E-Commerce Platform requires a production deployment platform for backend FastAPI microservices. Three viable options exist with different tradeoffs:

1. **Railway.app** - Simplest, fastest deployment
2. **Render.com** - Free tier available, good docs
3. **Kubernetes** - Full control, complex setup

### Constraints
- **Timeline**: Phase 6 execution is Day 7 (8-12 hours available)
- **Team**: Single developer/small team (limited DevOps expertise)
- **Budget**: Cost-conscious but willing to pay for reliability
- **Scalability**: Support 1000 req/s initially, 10x growth later
- **Availability**: 99.9% uptime SLA

### Requirements Driving Decision
- ✅ Simple deployment process (git push triggers deploy)
- ✅ Zero-downtime deployments
- ✅ Automatic scaling
- ✅ Built-in monitoring and logging
- ✅ PostgreSQL database integration
- ✅ Vector database (Qdrant) support
- ✅ Cost <$500/month initially
- ✅ Upgrade path to K8s later

---

## Decision

### Selected: **Railway.app**

We will deploy all backend services to Railway.app with the following configuration:

**Services**:
- Product Service (FastAPI)
- Order Service (FastAPI)
- Chat Service (FastAPI)
- Payment Service (FastAPI)
- Notification Service (FastAPI)
- Admin Service (FastAPI)

**Database**: Neon PostgreSQL (connected via Railway addon)
**Vector Database**: Qdrant (self-hosted on Railway or Railway plugin)
**Frontend**: Vercel (already selected)

---

## Rationale

### Why Railway > Render & K8s

| Criterion | Railway | Render | Kubernetes |
|-----------|---------|--------|-----------|
| Setup Time | 2 hours | 2.5 hours | 6-8 hours |
| Deployment Ease | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Built-in Monitoring | ✅ Yes | ⚠️ Basic | ⚠️ Requires setup |
| Cost (month 1) | $100-200 | $50-100 | $200-500 |
| Scaling | Auto | Manual | Auto |
| Upgrade Path | → K8s | → K8s | Final |
| PostgreSQL Integration | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Learning Curve | Low | Medium | High |

### Key Advantages

1. **Speed**: Git push automatically triggers builds/deploys
   - No manual Docker image management
   - No cluster configuration needed
   - Deploy in 2 hours vs 6-8 for K8s

2. **Developer Experience**:
   - Simple environment variable management
   - Built-in logs and metrics
   - One-click rollback
   - No DevOps expertise required

3. **Reliability**:
   - Auto-restarts failed services
   - Health checks built-in
   - Multi-region failover available
   - 99.9% uptime SLA

4. **Cost-Effective**:
   - Pay-as-you-go pricing
   - No minimum commitment
   - Scales efficiently
   - Free tier for testing

5. **PostgreSQL Integration**:
   - Railway PostgreSQL addon
   - Automatic backups
   - Easy migration from local
   - Zero additional setup

6. **Kubernetes Migration Path**:
   - If outgrow Railway, migrate to K8s
   - Code unchanged (same Docker containers)
   - Team can learn K8s gradually

### Why Not Render?
- Similar to Railway but less integrated
- Fewer built-in monitoring features
- Slightly cheaper but less value
- Free tier not suitable for production

### Why Not Kubernetes?
- **Overkill for Phase 1**: Platform starts with 1 developer
- **Timeline Risk**: 6-8 hour setup prevents Phase 6 completion
- **Operational Burden**: Requires ongoing K8s expertise
- **Better Path**: Start with Railway, migrate to K8s at Day 30 if needed

---

## Consequences

### Positive
✅ **Faster Time-to-Market**: Deploy 1 day earlier than K8s
✅ **Reduced Complexity**: No cluster management learning curve
✅ **Better Observability**: Built-in logging and monitoring
✅ **Lower Initial Cost**: $100-200 vs $500+ for K8s
✅ **Flexible Scaling**: Auto-scale on CPU threshold
✅ **Easy Rollbacks**: One-click revert to previous version
✅ **Team Productivity**: More time on features, less on ops

### Negative
❌ **Vendor Lock-in**: Migration to K8s requires effort
❌ **Less Control**: Can't fine-tune infrastructure details
❌ **Cost Scaling**: Becomes expensive at very high scale (1M+ req/day)
❌ **Limited Customization**: Fixed resource options
❌ **Learning Debt**: Team doesn't learn K8s during Phase 1

### Mitigation for Negatives
- **Vendor Lock-in**: Containerized code, migration plan documented
- **High Scale**: Monitor costs, upgrade to K8s if >$500/month
- **Learning**: Allocate Day 30+ for K8s exploration
- **Customization**: Railway supports most use cases; use environment-specific configs

---

## Migration Plan (K8s - Future)

If and when Railway becomes limiting (scale, cost, or control):

**Timeline**: Day 30+ (after Phase 6 stabilization)

**Steps**:
1. Create Kubernetes cluster (GKE/AKS/EKS)
2. Deploy same Docker containers to K8s
3. Connect existing PostgreSQL database
4. Run parallel (blue-green): Railway + K8s simultaneously
5. Switch traffic to K8s once verified
6. Decommission Railway

**Estimated Effort**: 2-3 days for small team
**Risk**: Low (same containers, tested code)
**Reversibility**: Can switch back to Railway if issues arise

---

## Alternatives Considered

### Alternative 1: Render.com
**Pros**:
- Similar to Railway, slightly cheaper
- Good documentation
- Free tier available

**Cons**:
- Less integrated monitoring
- Slower deployments
- Less mature than Railway

**Rejected**: Railway offers better value

### Alternative 2: AWS Elastic Container Service (ECS)
**Pros**:
- Massive ecosystem
- Cost optimization tools
- Enterprise support

**Cons**:
- Complex configuration
- Steep learning curve
- Overkill for current scale

**Rejected**: Too complex for timeline

### Alternative 3: Heroku
**Pros**:
- Simple deployment model
- Built-in addons

**Cons**:
- Very expensive ($500+/month)
- Sluggish performance (dynos)
- Limited scaling options

**Rejected**: Cost + performance issues

### Alternative 4: Kubernetes (From Day 1)
**Pros**:
- Full control
- Scales to any size
- Industry standard

**Cons**:
- 6-8 hour setup
- Requires DevOps expertise
- Overkill for Phase 1

**Rejected**: Doesn't fit timeline, no expertise available

---

## Decision Record

| Question | Answer |
|----------|--------|
| **What are we deciding?** | Where to deploy backend services to production |
| **Why now?** | Phase 6 (Production Deployment) begins in ~2 days |
| **Who decides?** | Project Lead (NAVEED261) with architecture team input |
| **How long until reviewed?** | 1 week post-deployment |
| **When do we revisit?** | If costs exceed $500/month OR scale >1M req/day |
| **Who implements?** | DevOps engineer / Project lead |
| **What's the success criteria?** | Services live on Railway, 99.9% uptime, <200ms latency |

---

## Implementation Checklist

- [ ] Create Railway account and link GitHub
- [ ] Create Railway services (product, order, chat, payment, notification, admin)
- [ ] Configure PostgreSQL addon (or use Neon + Railway networking)
- [ ] Deploy services
- [ ] Configure health checks
- [ ] Set up environment variables
- [ ] Enable auto-scaling (CPU >70%)
- [ ] Verify all services running
- [ ] Configure alerts
- [ ] Test deployment rollback
- [ ] Document runbook for on-call team

---

## Related Documents

- [`DEPLOYMENT.md`](../../DEPLOYMENT.md) - Full deployment runbook (Phase 6)
- [`CLAUDE.md`](../../CLAUDE.md) - Phase 6 (Production Deployment) section
- [`TASKS.md`](../../TASKS.md) - Task 6.1 (Infrastructure Setup)

---

## Approval

**Decided By**: Claude (AI Assistant) on behalf of NAVEED261
**Approved By**: NAVEED261 (Project Lead) ✅
**Date**: 2026-02-08
**Rationale**: Railway provides optimal balance of simplicity, cost, and reliability for Phase 6 deployment within 24-hour timeline.

---

## Review History

| Version | Date | Reviewer | Status |
|---------|------|----------|--------|
| 1.0 | 2026-02-08 | NAVEED261 | APPROVED |

---

**Next Review**: 2026-02-15 (1 week post-deployment)
**Escalation**: If costs exceed $500/month, escalate to CTO for K8s migration decision


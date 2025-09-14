# realworld-devops-homelab

Local-first DevOps homelab designed to simulate production-like environments on a single Ubuntu laptop using **k3d**.  
The goal: practice modern DevOps & SRE workflows (GitOps, Helm, observability, DevSecOps, chaos) with minimal cost.

---

## Project architecture

```text
realworld-devops-homelab/
├─ apps/
│  ├─ frontend/
│  ├─ orders-api/
│  ├─ payments-api/
│  ├─ catalog-api/
│  ├─ ai-worker/
│  └─ shared/
├─ deploy/
│  ├─ compose/
│  │  ├─ docker-compose.dev.yml
│  │  └─ docker-compose.prod.yml
│  ├─ k8s/
│  │  ├─ base/
│  │  ├─ overlays/
│  │  │  ├─ dev/
│  │  │  └─ prod/
│  │  ├─ argo/
│  │  └─ rollouts/
│  └─ charts/
├─ ci-cd/
│  └─ github-actions/
├─ observability/
│  ├─ prometheus/
│  ├─ grafana/
│  ├─ loki-promtail/
│  ├─ tracing/
│  └─ alerts/
├─ mq/
│  ├─ rabbitmq/
│  └─ redpanda/
├─ security/
│  ├─ trivy/
│  ├─ syft/
│  ├─ cosign/
│  ├─ opa-gatekeeper/
│  └─ vault/
├─ infra/
│  └─ terraform/
├─ chaos/
│  └─ litmus/
├─ registry/
│  ├─ k3d-registry.yaml
│  └─ harbor/
├─ docs/
│  ├─ diagrams/
│  ├─ runbook.md
│  ├─ architecture.md
│  ├─ showcase.md
│  └─ security.md
├─ .github/workflows/
├─ README.md
└─ LICENSE
...

## ASCII architecture - Local only (dev + prod)

             ┌────────────────────────────────────────┐
             │    Local Ubuntu Laptop (Dev + Prod)    │
             │     k3d clusters + local registry      │
             └────────────────────────────────────────┘
                             │
      ┌─────────────────────────────────────────────────────────┐
      │   ┌──────────────┐    ┌──────────────┐                  │
      │   │ Frontend     │    │ Orders-API   │                  │
      │   └──────────────┘    └──────────────┘                  │
      │   ┌──────────────┐    ┌──────────────┐                  │
      │   │ Payments-API │    │ Catalog-API  │                  │
      │   └──────────────┘    └──────────────┘                  │
      │   ┌──────────────┐                                      │
      │   │ AI Worker    │ <── RabbitMQ OR Redpanda             │
      │   └──────────────┘                                      │
      │                                                         │
      │   Ingress: Traefik | GitOps: ArgoCD | Obs: Grafana stack│
      │   Security: Trivy, Syft, Cosign, Gatekeeper, Vault      │
      │   Chaos: Litmus (pod-delete, latency tests)             │
      └─────────────────────────────────────────────────────────┘


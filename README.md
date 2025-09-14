# realworld-devops-homelab

Local-first DevOps homelab designed to simulate production-like environments on a single Ubuntu laptop using **k3d**.  
The goal: practice modern DevOps & SRE workflows (GitOps, Helm, observability, DevSecOps, chaos) with minimal cost.

## Project architecture

```text
realworld-devops-homelab/
├─ apps/ # Application services
│  ├─ frontend/ # React/Vue UI
│  ├─ orders-api/ # Handles orders
│  ├─ payments-api/ # Handles payments (FastAPI/Flask)
│  ├─ catalog-api/ # Catalog service
│  ├─ ai-worker/ # Worker (rules engine or ML inference)
│  └─ shared/ # Shared libs, contracts, OpenAPI schemas
├─ deploy/
│  ├─ compose/ # Local bring-up for dev/prod
│  │  ├─ docker-compose.dev.yml
│  │  └─ docker-compose.prod.yml
│  ├─ k8s/
│  │  ├─ base/ # Common manifests (namespace, RBAC, CRDs)
│  │  ├─ overlays/
│  │  │  ├─ dev/ # Local dev (k3d cluster)
│  │  │  └─ prod/ # Local prod (separate k3d cluster)
│  │  ├─ argo/ # ArgoCD App-of-Apps definitions
│  │  └─ rollouts/ # Argo Rollouts configs (canary, blue/green)
│  └─ charts/ # Helm charts for apps & infra
│     ├─ frontend/
│     ├─ orders-api/
│     ├─ payments-api/
│     ├─ catalog-api/
│     ├─ ai-worker/
│     ├─ traefik/ # Helm chart for Traefik ingress
│     ├─ rabbitmq/ # Legacy MQ (queue-based)
│     ├─ redpanda/ # Kafka-compatible broker
│     ├─ prometheus/ # Monitoring
│     ├─ grafana/ # Dashboards
│     ├─ loki/ # Logs
│     └─ otel-collector/ # Distributed tracing
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


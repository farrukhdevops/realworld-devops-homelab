# realworld-devops-homelab

Local-first DevOps homelab designed to simulate production-like environments on a single Ubuntu laptop using **k3d**.  
The goal: practice modern DevOps & SRE workflows (GitOps, Helm, observability, DevSecOps, chaos) with minimal cost.

---

## Project architecture


realworld-devops-homelab/
├─ apps/ # Application services
│ ├─ frontend/ # React/Vue UI
│ ├─ orders-api/ # Handles orders
│ ├─ payments-api/ # Handles payments (FastAPI/Flask)
│ ├─ catalog-api/ # Catalog service
│ ├─ ai-worker/ # Worker (rules engine or ML inference)
│ └─ shared/ # Shared libs, contracts, OpenAPI schemas
│
├─ deploy/
│ ├─ compose/ # Local bring-up for dev/prod
│ │ ├─ docker-compose.dev.yml
│ │ └─ docker-compose.prod.yml
│ ├─ k8s/
│ │ ├─ base/ # Common manifests (namespace, RBAC, CRDs)
│ │ ├─ overlays/
│ │ │ ├─ dev/ # Local dev (k3d cluster)
│ │ │ └─ prod/ # Local prod (separate k3d cluster)
│ │ ├─ argo/ # ArgoCD App-of-Apps definitions
│ │ └─ rollouts/ # Argo Rollouts configs (canary, blue/green)
│ └─ charts/ # Helm charts for apps & infra
│ ├─ frontend/
│ ├─ orders-api/
│ ├─ payments-api/
│ ├─ catalog-api/
│ ├─ ai-worker/
│ ├─ traefik/ # Helm chart for Traefik ingress
│ ├─ rabbitmq/ # Legacy MQ (queue-based)
│ ├─ redpanda/ # Kafka-compatible broker
│ ├─ prometheus/ # Monitoring
│ ├─ grafana/ # Dashboards
│ ├─ loki/ # Logs
│ └─ otel-collector/ # Distributed tracing
│
├─ ci-cd/
│ ├─ github-actions/ # GitHub Actions workflows
│ │ ├─ build.yml
│ │ ├─ test.yml # Unit/integration tests
│ │ ├─ security.yml # Trivy, Syft, Cosign
│ │ └─ deploy.yml # Deploy to k3d dev/prod via ArgoCD sync
│ └─ scripts/ # Helper scripts (tagging, version bump, push)
│
├─ observability/
│ ├─ prometheus/ # Metrics config + alert rules
│ ├─ grafana/ # Dashboards + provisioning
│ ├─ loki-promtail/ # Log aggregation configs
│ ├─ tracing/ # OTEL collector configs (Jaeger/Tempo)
│ └─ alerts/ # Alertmanager configs + runbooks
│
├─ mq/
│ ├─ rabbitmq/ # Legacy task queue
│ └─ redpanda/ # Kafka-compatible event streaming
│
├─ security/
│ ├─ trivy/ # Container scanning configs
│ ├─ syft/ # SBOM generation
│ ├─ cosign/ # Image signing & verification
│ ├─ opa-gatekeeper/ # Policy enforcement
│ └─ vault/ # Local Vault for secrets
│
├─ infra/
│ └─ terraform/ # OPTIONAL IaC Showcase
│ ├─ dev-cluster.tf # Dev k3d cluster + registry
│ ├─ prod-cluster.tf # Prod k3d cluster + registry
│ └─ helm-releases.tf # Bootstrap Traefik/ArgoCD via Helm provider
│
├─ chaos/
│ └─ litmus/ # Chaos experiments (pod delete, network delay)
│
├─ registry/
│ ├─ k3d-registry.yaml # Local dev/prod registry config
│ └─ harbor/ # Optional Harbor setup
│
├─ docs/
│ ├─ diagrams/ # Local architecture diagrams
│ ├─ runbook.md # Incident response + chaos recovery steps
│ ├─ architecture.md # High-level design
│ ├─ showcase.md # Demo checklist (Dev → GitOps → Prod)
│ └─ security.md # Threat model + DevSecOps practices
│
├─ .github/workflows/ # Meta checks (linting, SAST, SBOM, etc.)
├─ README.md
└─ LICENSE

---

## ASCII architecture - Local only (dev + prod)



---

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


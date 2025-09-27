# IZA OS System Map

Complete system architecture and dependency mapping for the IZA OS ecosystem.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    IZA OS Ecosystem                        │
├─────────────────────────────────────────────────────────────┤
│  Core Orchestration Layer                                  │
│  ├── Warp Workflows (main.yaml, subflows/)                │
│  ├── MCP Server Hub (server.py, auth/, schemas/)          │
│  └── Command Interface (warp/commands/)                   │
├─────────────────────────────────────────────────────────────┤
│  AI Agents Layer                                           │
│  ├── Claude Agents (agent_manager.py, wrappers/)          │
│  ├── Local LLM (Ollama, AnythingLLM)                       │
│  ├── Fellou Agents (autonomous workflows)                 │
│  ├── Omnara Agents (deployment orchestration)             │
│  └── Klavis Agents (contextual AI)                        │
├─────────────────────────────────────────────────────────────┤
│  Knowledge Management Layer                               │
│  ├── Notes Integration (obsidian/, apple_notes/, jupyter/)│
│  ├── RAG Pipeline (indexer.py, retriever.py)             │
│  └── Vector Databases (ChromaDB, Weaviate, Pinecone)      │
├─────────────────────────────────────────────────────────────┤
│  Security & API Layer                                      │
│  ├── Authentication (jwt_manager.py, api_keys.json)       │
│  ├── Infrastructure (docker-compose.yaml, terraform/, k8s/)│
│  └── Monitoring (Prometheus, Grafana)                     │
├─────────────────────────────────────────────────────────────┤
│  Research & Documentation Layer                            │
│  ├── Master Research (master_research.pdf)                │
│  ├── Monetization Strategies (monetization_strategies.md) │
│  ├── System Map (system_map.md)                           │
│  └── Prompts (cursor_prompts.md, vercept_job.yaml)        │
├─────────────────────────────────────────────────────────────┤
│  Experimentation Layer                                     │
│  ├── Neuro Pipeline (eeg_pipeline.py)                     │
│  ├── Quantum Mirror (quantum_mirror/)                     │
│  └── Sandbox (rapid tests, experimental ideas)             │
└─────────────────────────────────────────────────────────────┘
```

## Project Dependencies

### 1. Core Orchestration
**Dependencies:**
- Python 3.11+
- FastAPI
- JWT libraries
- Redis client
- PostgreSQL client

**Dependents:**
- All AI Agents
- Knowledge Management
- Security & API
- Dashboard

### 2. AI Agents
**Dependencies:**
- Core Orchestration (MCP Server)
- Claude API
- Ollama/Local LLM
- Vercept API
- Redis (for agent state)

**Dependents:**
- Dashboard (for monitoring)
- Knowledge Management (for context)

### 3. Knowledge Management
**Dependencies:**
- ChromaDB/Vector databases
- OpenAI API (for embeddings)
- File system watchers
- PostgreSQL (for metadata)

**Dependents:**
- AI Agents (for context)
- Dashboard (for visualization)

### 4. Security & API
**Dependencies:**
- Docker & Docker Compose
- Kubernetes (optional)
- Terraform (for cloud deployment)
- Prometheus & Grafana

**Dependents:**
- All other layers

### 5. Research & Documentation
**Dependencies:**
- Markdown processors
- PDF generators
- Documentation tools

**Dependents:**
- Development team
- AI agents (for context)

### 6. Neuro/Quantum Sandbox
**Dependencies:**
- OpenBCI hardware
- MNE-Python
- Qiskit
- Experimental libraries

**Dependents:**
- Research projects
- Future AI enhancements

## Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Notes     │───▶│   RAG       │───▶│   Agents    │
│ (Obsidian,  │    │  Indexer    │    │  (Claude,   │
│ Apple, etc) │    │             │    │  Local LLM) │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  File       │    │  Vector     │    │   MCP       │
│  Watchers   │    │  Database   │    │  Server     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Real-time  │    │  Similarity │    │  Task       │
│  Sync       │    │  Search     │    │  Routing    │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Service Ports

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Caching and sessions |
| MinIO | 9000/9001 | Object storage |
| Neo4j | 7474/7687 | Graph database |
| ChromaDB | 8000 | Vector database |
| MCP Server | 8080 | Central API hub |
| Ollama | 11434 | Local LLM server |
| AnythingLLM | 3001 | LLM interface |
| Botpress | 3000 | Conversational AI |
| Dashboard | 8501 | Streamlit UI |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3001 | Monitoring dashboard |

## Environment Variables

### Core Services
```bash
# Database
DATABASE_URL=postgresql://iza_user:iza_password_2024@postgres:5432/iza_os
REDIS_URL=redis://redis:6379/0

# Vector Database
CHROMA_URL=http://chroma:8000
NEO4J_URL=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=iza_neo4j_2024

# Authentication
JWT_PUBLIC_KEY=your_jwt_public_key
JWT_PRIVATE_KEY=your_jwt_private_key
```

### AI Providers
```bash
# Claude
CLAUDE_API_KEY=sk-ant-...

# OpenAI
OPENAI_API_KEY=sk-...

# Vercept
VERCEPT_API_KEY=your_vercept_key
VERCEPT_BASE_URL=https://api.vercept.com/v1

# Local LLM
OLLAMA_URL=http://ollama:11434
```

### External Services
```bash
# Monitoring
PROMETHEUS_URL=http://prometheus:9090
GRAFANA_URL=http://grafana:3000

# Storage
MINIO_ACCESS_KEY=iza_admin
MINIO_SECRET_KEY=iza_minio_2024
```

## Deployment Strategies

### 1. Local Development
```bash
# Start all services
docker compose -f 4-security-api/infra/docker-compose.yaml up -d

# Build RAG index
python3 3-knowledge-management/rag/indexer.py

# Start agents
python3 2-ai-agents/claude/agent_manager.py spawn research
```

### 2. Staging Environment
```bash
# Deploy with Terraform
cd 4-security-api/infra/terraform
terraform init
terraform plan
terraform apply

# Configure monitoring
kubectl apply -f 4-security-api/infra/k8s/monitoring/
```

### 3. Production Environment
```bash
# Blue-green deployment
./deploy.sh --environment=production --strategy=blue-green

# Health checks
./health-check.sh --environment=production
```

## Monitoring & Observability

### Metrics Collection
- **System Metrics**: CPU, memory, disk usage
- **Application Metrics**: Request rates, response times, error rates
- **Business Metrics**: Agent performance, task completion rates
- **Cost Metrics**: API usage, resource consumption

### Alerting Rules
- **Critical**: Service down, high error rate (>5%)
- **Warning**: High resource usage (>80%), slow response (>5s)
- **Info**: New deployments, configuration changes

### Dashboards
- **System Overview**: Overall health and performance
- **Agent Performance**: Individual agent metrics
- **Knowledge Base**: RAG performance and usage
- **Cost Analysis**: Resource usage and optimization

## Security Considerations

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- API key management and rotation
- Multi-factor authentication (MFA)

### Data Protection
- Encryption at rest and in transit
- Secure credential storage
- Data anonymization and privacy
- Compliance with regulations (GDPR, CCPA)

### Network Security
- VPC and private networks
- Firewall rules and security groups
- DDoS protection
- Intrusion detection and prevention

## Scalability & Performance

### Horizontal Scaling
- Stateless service design
- Load balancing and auto-scaling
- Database sharding and replication
- CDN for static content

### Vertical Scaling
- Resource optimization
- Caching strategies
- Database query optimization
- Memory and CPU tuning

### Performance Optimization
- Connection pooling
- Async processing
- Batch operations
- Caching layers

## Disaster Recovery

### Backup Strategy
- Automated database backups
- Configuration backup
- Code repository backup
- Disaster recovery testing

### High Availability
- Multi-region deployment
- Failover mechanisms
- Data replication
- Service redundancy

## Development Workflow

### Code Management
- Git flow branching strategy
- Automated testing and CI/CD
- Code review process
- Documentation updates

### Environment Management
- Development, staging, production
- Environment-specific configurations
- Secret management
- Infrastructure as Code (IaC)

### Quality Assurance
- Automated testing (unit, integration, e2e)
- Performance testing
- Security scanning
- Code quality checks

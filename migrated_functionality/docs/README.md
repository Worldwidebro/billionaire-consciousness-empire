# DevOps & Deployment

Enterprise-grade DevOps and deployment infrastructure for the IZA OS ecosystem.

## IZA OS Integration

This project provides:
- **Unified CI/CD Pipeline**: GitHub Actions workflows for all IZA OS components
- **Infrastructure as Code**: Terraform configurations for scalable deployment
- **Monitoring & Alerting**: Comprehensive monitoring with Prometheus, Grafana, and custom dashboards
- **Automated Scaling**: Kubernetes-based auto-scaling for production workloads

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                DevOps & Deployment Hub                    │
├─────────────────────────────────────────────────────────────┤
│  CI/CD Pipeline                                            │
│  ├── GitHub Actions Workflows                             │
│  ├── Multi-Environment Deployment                         │
│  ├── Automated Testing                                    │
│  └── Security Scanning                                    │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure as Code                                   │
│  ├── Terraform Configurations                            │
│  ├── Kubernetes Manifests                                │
│  ├── Docker Compose Files                                 │
│  └── Environment Templates                               │
├─────────────────────────────────────────────────────────────┤
│  Monitoring & Alerting                                    │
│  ├── Prometheus Metrics Collection                        │
│  ├── Grafana Dashboards                                   │
│  ├── Custom IZA OS Dashboards                            │
│  └── PagerDuty Integration                               │
├─────────────────────────────────────────────────────────────┤
│  Deployment Orchestration                                 │
│  ├── Blue-Green Deployments                              │
│  ├── Canary Releases                                      │
│  ├── Rollback Procedures                                  │
│  └── Health Checks                                       │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. CI/CD Pipeline (`ci_cd/`)

#### GitHub Actions Workflows
- **Main CI Pipeline**: Automated testing, building, and deployment
- **Security Pipeline**: Security scanning and vulnerability assessment
- **Performance Pipeline**: Performance testing and optimization
- **Release Pipeline**: Automated release management

#### Multi-Environment Support
- **Development**: Local development environment
- **Staging**: Pre-production testing environment
- **Production**: Live production environment
- **Disaster Recovery**: Backup and recovery environment

### 2. Infrastructure as Code (`infra/`)

#### Terraform Configurations
- **AWS Infrastructure**: EC2, RDS, S3, CloudFront
- **DigitalOcean Infrastructure**: Droplets, Managed Databases
- **Kubernetes Clusters**: EKS, GKE, AKS
- **Networking**: VPC, subnets, security groups

#### Kubernetes Manifests
- **Deployments**: Application deployments
- **Services**: Service discovery and load balancing
- **Ingress**: External access and SSL termination
- **ConfigMaps & Secrets**: Configuration management

### 3. Monitoring & Alerting (`monitoring/`)

#### Prometheus Metrics
- **Application Metrics**: Custom business metrics
- **Infrastructure Metrics**: System resource utilization
- **Performance Metrics**: Response times and throughput
- **Business Metrics**: User engagement and revenue

#### Grafana Dashboards
- **System Overview**: High-level system health
- **Application Performance**: Detailed performance metrics
- **Business Intelligence**: Revenue and user metrics
- **IZA OS Specific**: Custom IZA OS ecosystem metrics

## IZA OS Ecosystem Integration

### Unified Deployment Configuration
```yaml
# ci_cd/iza-os-deployment.yaml
name: IZA OS Ecosystem Deployment

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  IZA_OS_VERSION: ${{ github.sha }}
  ECOSYSTEM_VALUE: "$10.2B+"
  
jobs:
  deploy-ecosystem:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout IZA OS Code
        uses: actions/checkout@v4
        with:
          repository: 'Worldwidebro/iza-os-cursor'
          
      - name: Deploy Core Orchestration
        run: |
          kubectl apply -f infra/k8s/core-orchestration/
          kubectl rollout status deployment/mcp-server
          
      - name: Deploy AI Agents
        run: |
          kubectl apply -f infra/k8s/ai-agents/
          kubectl rollout status deployment/claude-agent
          kubectl rollout status deployment/omnara-agent
          
      - name: Deploy Knowledge Management
        run: |
          kubectl apply -f infra/k8s/knowledge-management/
          kubectl rollout status deployment/rag-pipeline
          
      - name: Deploy Security & API
        run: |
          kubectl apply -f infra/k8s/security-api/
          kubectl rollout status deployment/auth-service
          
      - name: Deploy Monitoring
        run: |
          kubectl apply -f infra/k8s/monitoring/
          kubectl rollout status deployment/prometheus
          kubectl rollout status deployment/grafana
          
      - name: Health Check
        run: |
          ./scripts/health-check.sh
          
      - name: Notify Success
        if: success()
        run: |
          curl -X POST "${{ secrets.SLACK_WEBHOOK }}" \
            -H 'Content-type: application/json' \
            --data '{"text":"✅ IZA OS Ecosystem deployed successfully!"}'
```

### Infrastructure Configuration
```hcl
# infra/terraform/iza-os-infrastructure.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

# IZA OS EKS Cluster
resource "aws_eks_cluster" "iza_os_cluster" {
  name     = "iza-os-ecosystem"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = "1.28"

  vpc_config {
    subnet_ids = aws_subnet.iza_os_subnets[*].id
  }

  tags = {
    Name        = "IZA OS Ecosystem"
    Environment = "production"
    Value       = "$10.2B+"
  }
}

# IZA OS Node Groups
resource "aws_eks_node_group" "iza_os_nodes" {
  cluster_name    = aws_eks_cluster.iza_os_cluster.name
  node_group_name = "iza-os-workers"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = aws_subnet.iza_os_subnets[*].id

  scaling_config {
    desired_size = 5
    max_size     = 20
    min_size     = 3
  }

  instance_types = ["t3.large", "t3.xlarge"]

  tags = {
    Name = "IZA OS Workers"
  }
}

# IZA OS RDS Database
resource "aws_db_instance" "iza_os_database" {
  identifier = "iza-os-database"
  engine     = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.large"
  allocated_storage = 100
  storage_type = "gp3"

  db_name  = "iza_os"
  username = "iza_os_admin"
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.iza_os_db.id]
  db_subnet_group_name   = aws_db_subnet_group.iza_os.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window    = "sun:04:00-sun:05:00"

  tags = {
    Name = "IZA OS Database"
  }
}
```

### Monitoring Configuration
```yaml
# monitoring/prometheus-config.yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "iza-os-rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  # IZA OS Core Orchestration
  - job_name: 'iza-os-mcp-server'
    static_configs:
      - targets: ['mcp-server:8080']
    metrics_path: '/metrics'
    
  # IZA OS AI Agents
  - job_name: 'iza-os-claude-agent'
    static_configs:
      - targets: ['claude-agent:8081']
    metrics_path: '/metrics'
    
  - job_name: 'iza-os-omnara-agent'
    static_configs:
      - targets: ['omnara-agent:8082']
    metrics_path: '/metrics'
    
  # IZA OS Knowledge Management
  - job_name: 'iza-os-rag-pipeline'
    static_configs:
      - targets: ['rag-pipeline:8083']
    metrics_path: '/metrics'
    
  # IZA OS Security & API
  - job_name: 'iza-os-auth-service'
    static_configs:
      - targets: ['auth-service:8084']
    metrics_path: '/metrics'
    
  # IZA OS Monitoring
  - job_name: 'iza-os-prometheus'
    static_configs:
      - targets: ['prometheus:9090']
    metrics_path: '/metrics'
```

## Deployment Strategies

### Blue-Green Deployment
```bash
#!/bin/bash
# scripts/blue-green-deployment.sh

# Deploy to green environment
kubectl apply -f infra/k8s/green/
kubectl rollout status deployment/iza-os-green

# Health check green environment
./scripts/health-check.sh --environment=green

if [ $? -eq 0 ]; then
    # Switch traffic to green
    kubectl patch service iza-os-service -p '{"spec":{"selector":{"version":"green"}}}'
    
    # Wait for traffic to switch
    sleep 30
    
    # Verify traffic is on green
    ./scripts/verify-traffic.sh --environment=green
    
    if [ $? -eq 0 ]; then
        # Clean up blue environment
        kubectl delete -f infra/k8s/blue/
        echo "✅ Blue-Green deployment successful"
    else
        # Rollback to blue
        kubectl patch service iza-os-service -p '{"spec":{"selector":{"version":"blue"}}}'
        echo "❌ Blue-Green deployment failed, rolled back"
        exit 1
    fi
else
    echo "❌ Green environment health check failed"
    exit 1
fi
```

### Canary Release
```yaml
# infra/k8s/canary-deployment.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: iza-os-canary
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 10m}
      - setWeight: 20
      - pause: {duration: 10m}
      - setWeight: 50
      - pause: {duration: 10m}
      - setWeight: 100
      analysis:
        templates:
        - templateName: iza-os-analysis
        args:
        - name: service-name
          value: iza-os-service
  selector:
    matchLabels:
      app: iza-os
  template:
    metadata:
      labels:
        app: iza-os
    spec:
      containers:
      - name: iza-os
        image: iza-os/ecosystem:latest
        ports:
        - containerPort: 8080
```

## Monitoring & Alerting

### Custom IZA OS Metrics
```python
# monitoring/iza-os-metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# IZA OS Business Metrics
ecosystem_value = Gauge('iza_os_ecosystem_value', 'IZA OS Ecosystem Value in USD')
active_agents = Gauge('iza_os_active_agents', 'Number of Active AI Agents')
rag_queries = Counter('iza_os_rag_queries_total', 'Total RAG Queries')
mcp_calls = Counter('iza_os_mcp_calls_total', 'Total MCP Calls')
venture_projects = Gauge('iza_os_venture_projects', 'Number of Active Venture Projects')

# IZA OS Performance Metrics
agent_response_time = Histogram('iza_os_agent_response_time_seconds', 'Agent Response Time')
rag_processing_time = Histogram('iza_os_rag_processing_time_seconds', 'RAG Processing Time')
mcp_latency = Histogram('iza_os_mcp_latency_seconds', 'MCP Call Latency')

# IZA OS Quality Metrics
data_quality_score = Gauge('iza_os_data_quality_score', 'Data Quality Score (0-100)')
automation_success_rate = Gauge('iza_os_automation_success_rate', 'Automation Success Rate')
scraping_accuracy = Gauge('iza_os_scraping_accuracy', 'Scraping Accuracy Percentage')

class IZAOSMetrics:
    def __init__(self):
        self.start_time = time.time()
        
    def update_ecosystem_metrics(self, metrics: dict):
        """Update IZA OS ecosystem metrics"""
        ecosystem_value.set(metrics.get('value', 10247500000))
        active_agents.set(metrics.get('active_agents', 0))
        venture_projects.set(metrics.get('venture_projects', 0))
        
    def record_agent_call(self, agent_type: str, response_time: float):
        """Record agent call metrics"""
        agent_response_time.labels(agent_type=agent_type).observe(response_time)
        
    def record_rag_query(self, query_type: str, processing_time: float):
        """Record RAG query metrics"""
        rag_queries.labels(type=query_type).inc()
        rag_processing_time.labels(type=query_type).observe(processing_time)
        
    def record_mcp_call(self, mcp_type: str, latency: float):
        """Record MCP call metrics"""
        mcp_calls.labels(type=mcp_type).inc()
        mcp_latency.labels(type=mcp_type).observe(latency)

# Start metrics server
if __name__ == "__main__":
    start_http_server(8080)
    print("IZA OS Metrics server started on port 8080")
    
    # Keep server running
    while True:
        time.sleep(1)
```

### Alerting Rules
```yaml
# monitoring/iza-os-alerts.yaml
groups:
- name: iza-os-ecosystem
  rules:
  - alert: IZAOSHighErrorRate
    expr: rate(iza_os_errors_total[5m]) > 0.1
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "IZA OS Ecosystem high error rate"
      description: "Error rate is {{ $value }} errors per second"
      
  - alert: IZAOSLowDataQuality
    expr: iza_os_data_quality_score < 90
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "IZA OS Data quality below threshold"
      description: "Data quality score is {{ $value }}%"
      
  - alert: IZAOSAgentSlowResponse
    expr: histogram_quantile(0.95, rate(iza_os_agent_response_time_seconds_bucket[5m])) > 10
    for: 3m
    labels:
      severity: warning
    annotations:
      summary: "IZA OS Agent slow response time"
      description: "95th percentile response time is {{ $value }}s"
      
  - alert: IZAOSMCPServerDown
    expr: up{job="iza-os-mcp-server"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "IZA OS MCP Server is down"
      description: "MCP Server has been down for more than 1 minute"
```

## Security & Compliance

### Security Scanning
```yaml
# ci_cd/security-scan.yaml
name: IZA OS Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        
      - name: Run Trivy Vulnerability Scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
          
      - name: Run Snyk Security Scan
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
          
      - name: Run OWASP ZAP Security Scan
        uses: zaproxy/action-full-scan@v0.4.0
        with:
          target: 'http://localhost:8080'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'
```

### Compliance Configuration
```yaml
# infra/compliance/soc2-config.yaml
compliance:
  soc2:
    enabled: true
    controls:
      - CC6.1: Logical and Physical Access Controls
      - CC6.2: System Access Controls
      - CC6.3: Data Access Controls
      - CC6.4: Network Access Controls
      - CC6.5: User Access Controls
      - CC6.6: Privileged Access Controls
      - CC6.7: Access Control Monitoring
      
  gdpr:
    enabled: true
    data_protection:
      encryption_at_rest: true
      encryption_in_transit: true
      data_retention_policy: "7 years"
      right_to_erasure: true
      data_portability: true
      
  hipaa:
    enabled: false
    # Configure if handling healthcare data
```

## Disaster Recovery

### Backup Strategy
```bash
#!/bin/bash
# scripts/disaster-recovery.sh

# Backup IZA OS Database
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup IZA OS Configurations
tar -czf config_backup_$(date +%Y%m%d_%H%M%S).tar.gz infra/

# Backup IZA OS Data
kubectl exec -it postgres-0 -- pg_dump -U iza_os > data_backup_$(date +%Y%m%d_%H%M%S).sql

# Upload to S3
aws s3 cp backup_$(date +%Y%m%d_%H%M%S).sql s3://iza-os-backups/
aws s3 cp config_backup_$(date +%Y%m%d_%H%M%S).tar.gz s3://iza-os-backups/
aws s3 cp data_backup_$(date +%Y%m%d_%H%M%S).sql s3://iza-os-backups/

# Cleanup old backups (keep 30 days)
find . -name "backup_*.sql" -mtime +30 -delete
find . -name "config_backup_*.tar.gz" -mtime +30 -delete
find . -name "data_backup_*.sql" -mtime +30 -delete
```

### Recovery Procedures
```bash
#!/bin/bash
# scripts/recovery-procedure.sh

# Restore IZA OS Database
psql -h $DB_HOST -U $DB_USER -d $DB_NAME < backup_20241201_120000.sql

# Restore IZA OS Configurations
tar -xzf config_backup_20241201_120000.tar.gz

# Restore IZA OS Data
kubectl exec -it postgres-0 -- psql -U iza_os < data_backup_20241201_120000.sql

# Restart IZA OS Services
kubectl rollout restart deployment/mcp-server
kubectl rollout restart deployment/claude-agent
kubectl rollout restart deployment/omnara-agent
kubectl rollout restart deployment/rag-pipeline
kubectl rollout restart deployment/auth-service

# Verify Recovery
./scripts/health-check.sh
```

## Performance Optimization

### Auto-scaling Configuration
```yaml
# infra/k8s/hpa-config.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: iza-os-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: iza-os-deployment
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: iza_os_active_agents
      target:
        type: AverageValue
        averageValue: "10"
```

### Load Testing
```python
# monitoring/load-test.py
import asyncio
import aiohttp
import time
from prometheus_client import Counter, Histogram, start_http_server

# Load test metrics
requests_total = Counter('load_test_requests_total', 'Total load test requests')
response_time = Histogram('load_test_response_time_seconds', 'Response time')

async def load_test_iza_os():
    """Load test IZA OS ecosystem"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        # Test MCP Server
        for i in range(100):
            task = asyncio.create_task(test_mcp_server(session))
            tasks.append(task)
            
        # Test AI Agents
        for i in range(50):
            task = asyncio.create_task(test_ai_agents(session))
            tasks.append(task)
            
        # Test RAG Pipeline
        for i in range(30):
            task = asyncio.create_task(test_rag_pipeline(session))
            tasks.append(task)
            
        # Wait for all tasks
        await asyncio.gather(*tasks)

async def test_mcp_server(session):
    """Test MCP server performance"""
    start_time = time.time()
    
    try:
        async with session.post('http://mcp-server:8080/api/call', 
                              json={'method': 'test', 'params': {}}) as response:
            if response.status == 200:
                requests_total.labels(service='mcp-server', status='success').inc()
            else:
                requests_total.labels(service='mcp-server', status='error').inc()
    except Exception as e:
        requests_total.labels(service='mcp-server', status='error').inc()
        print(f"MCP Server error: {e}")
    
    response_time.labels(service='mcp-server').observe(time.time() - start_time)

async def test_ai_agents(session):
    """Test AI agents performance"""
    start_time = time.time()
    
    try:
        async with session.post('http://claude-agent:8081/api/chat', 
                              json={'message': 'Test message'}) as response:
            if response.status == 200:
                requests_total.labels(service='ai-agents', status='success').inc()
            else:
                requests_total.labels(service='ai-agents', status='error').inc()
    except Exception as e:
        requests_total.labels(service='ai-agents', status='error').inc()
        print(f"AI Agents error: {e}")
    
    response_time.labels(service='ai-agents').observe(time.time() - start_time)

async def test_rag_pipeline(session):
    """Test RAG pipeline performance"""
    start_time = time.time()
    
    try:
        async with session.post('http://rag-pipeline:8083/api/query', 
                              json={'query': 'Test query'}) as response:
            if response.status == 200:
                requests_total.labels(service='rag-pipeline', status='success').inc()
            else:
                requests_total.labels(service='rag-pipeline', status='error').inc()
    except Exception as e:
        requests_total.labels(service='rag-pipeline', status='error').inc()
        print(f"RAG Pipeline error: {e}")
    
    response_time.labels(service='rag-pipeline').observe(time.time() - start_time)

if __name__ == "__main__":
    # Start metrics server
    start_http_server(8080)
    
    # Run load test
    asyncio.run(load_test_iza_os())
```

## Success Metrics

- **Deployment Success Rate**: >99.9% successful deployments
- **Mean Time to Recovery**: <5 minutes for critical issues
- **Infrastructure Uptime**: >99.99% availability
- **Security Scan Pass Rate**: 100% pass rate for security scans
- **Performance**: <2s response time for 95th percentile
- **Compliance**: 100% compliance with SOC2 and GDPR requirements

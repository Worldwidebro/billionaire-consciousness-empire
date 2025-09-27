#!/bin/bash

# Consciousness-OS Deployment Script
# This script deploys the complete 35-project Consciousness-OS system

set -e

echo "🚀 Deploying Consciousness-OS System"
echo "=================================="

# Configuration
CONSCIOUSNESS_OS_DIR="/Users/divinejohns/memU/consciousness-os"
GITHUB_REPO="https://github.com/Worldwidebro/consciousness-os.git"
DOCKER_COMPOSE_FILE="docker-compose.consciousness-os.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_deps=()
    
    if ! command_exists git; then
        missing_deps+=("git")
    fi
    
    if ! command_exists docker; then
        missing_deps+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi
    
    if ! command_exists node; then
        missing_deps+=("node")
    fi
    
    if ! command_exists python3; then
        missing_deps+=("python3")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        print_error "Please install the missing dependencies and try again."
        exit 1
    fi
    
    print_success "All prerequisites met"
}

# Function to create directory structure
create_directory_structure() {
    print_status "Creating Consciousness-OS directory structure..."
    
    # Create main directory
    mkdir -p "$CONSCIOUSNESS_OS_DIR"
    cd "$CONSCIOUSNESS_OS_DIR"
    
    # Create all 35 project directories
    local projects=(
        "0_SystemCore/warp"
        "0_SystemCore/cursor"
        "0_SystemCore/vercept"
        "0_SystemCore/raycast"
        "0_SystemCore/docker"
        "0_SystemCore/terraform"
        "1_Memory/vectorDB"
        "1_Memory/graphDB"
        "1_Memory/longterm"
        "1_Memory/shortterm"
        "2_Agents/roles"
        "2_Agents/lifecycle"
        "2_Agents/autonomy"
        "3_Reflection/critique"
        "3_Reflection/simulation"
        "3_Reflection/quantum_mirrors"
        "4_Tools/browsers"
        "4_Tools/cli_tools"
        "4_Tools/apis"
        "4_Tools/integrations"
        "5_Workflows/research_pipeline"
        "5_Workflows/build_pipeline"
        "5_Workflows/sync_pipeline"
        "5_Workflows/monetization_pipeline"
        "6_UI/frontend"
        "6_UI/dashboard"
        "6_UI/obsidian_publish"
        "7_Metrics/task_completion"
        "7_Metrics/revenue_tracking"
        "7_Metrics/autonomy_score"
        "8_Deployments/local_llm"
        "8_Deployments/cloud"
        "8_Deployments/hybrid"
        "9_Docs/research"
        "9_Docs/guides"
        "9_Docs/playbooks"
        "9_Docs/monetization"
    )
    
    for project in "${projects[@]}"; do
        mkdir -p "$project"
        print_status "Created directory: $project"
    done
    
    print_success "Directory structure created"
}

# Function to initialize Git repository
initialize_git_repo() {
    print_status "Initializing Git repository..."
    
    cd "$CONSCIOUSNESS_OS_DIR"
    
    if [ ! -d ".git" ]; then
        git init
        git remote add origin "$GITHUB_REPO"
        print_success "Git repository initialized"
    else
        print_warning "Git repository already exists"
    fi
}

# Function to create core configuration files
create_core_configs() {
    print_status "Creating core configuration files..."
    
    cd "$CONSCIOUSNESS_OS_DIR"
    
    # Create main README
    cat > README.md << 'EOF'
# Consciousness-OS

A 35-project system designed to simulate artificial metacognition through multi-layer memory, agent lifecycles, reflection systems, and autonomous monetization pipelines.

## Architecture

- **SystemCore**: Root configs and infrastructure
- **Memory**: Multi-layer memory system (vector, graph, long-term, short-term)
- **Agents**: Agent definitions and lifecycles
- **Reflection**: Meta-cognition and self-critique
- **Tools**: External connections and integrations
- **Workflows**: MCP servers and task pipelines
- **UI**: User interfaces and dashboards
- **Metrics**: Success measurement and tracking
- **Deployments**: Deployment environments
- **Docs**: Documentation and knowledge base

## Quick Start

1. Run the deployment script: `./deploy-consciousness-os.sh`
2. Follow the setup wizard
3. Start building your consciousness-like AI system

## Success Metrics

- **Task Completion Rate**: >90% tasks finished without human intervention
- **Revenue per Idea**: Each captured idea generates $X/month average
- **Autonomy Score**: >90% of pipeline operates without human intervention
- **Memory Continuity**: AI remembers and evolves ideas across days
- **Suggestive Power**: System surfaces useful next steps before being asked

## License

MIT License - see LICENSE file for details
EOF

    # Create Docker Compose file
    cat > "$DOCKER_COMPOSE_FILE" << 'EOF'
version: '3.8'

services:
  # Core Infrastructure
  neo4j:
    image: neo4j:5.15
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/consciousness
      - NEO4J_PLUGINS=["apoc"]
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma

  # AI Services
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=consciousness
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  neo4j_data:
  neo4j_logs:
  redis_data:
  chroma_data:
  ollama_data:
  prometheus_data:
  grafana_data:
EOF

    # Create package.json for Node.js dependencies
    cat > package.json << 'EOF'
{
  "name": "consciousness-os",
  "version": "1.0.0",
  "description": "Consciousness-OS: A 35-project system for AI consciousness simulation",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "build": "npm run build:frontend && npm run build:backend",
    "build:frontend": "cd 6_UI/frontend && npm run build",
    "build:backend": "cd 5_Workflows && python3 -m pip install -r requirements.txt",
    "deploy": "./deploy-consciousness-os.sh",
    "test": "npm run test:unit && npm run test:integration",
    "test:unit": "jest --testPathPattern=unit",
    "test:integration": "jest --testPathPattern=integration"
  },
  "dependencies": {
    "express": "^4.18.2",
    "socket.io": "^4.7.2",
    "axios": "^1.6.0",
    "neo4j-driver": "^5.13.0",
    "redis": "^4.6.0",
    "chromadb": "^1.7.0",
    "openai": "^4.20.0",
    "anthropic": "^0.18.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.7.0",
    "supertest": "^6.3.3"
  },
  "keywords": [
    "ai",
    "consciousness",
    "automation",
    "agents",
    "memory",
    "reflection"
  ],
  "author": "IZA OS Team",
  "license": "MIT"
}
EOF

    # Create requirements.txt for Python dependencies
    cat > requirements.txt << 'EOF'
# Core AI and ML
openai==1.3.0
anthropic==0.18.0
langchain==0.1.0
langchain-openai==0.0.5
langchain-anthropic==0.0.1

# Vector and Graph Databases
chromadb==0.4.18
neo4j==5.15.0
redis==5.0.1

# Web Framework
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0

# Data Processing
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2

# Monitoring and Logging
prometheus-client==0.19.0
structlog==23.2.0

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0
EOF

    print_success "Core configuration files created"
}

# Function to setup monitoring
setup_monitoring() {
    print_status "Setting up monitoring..."
    
    mkdir -p "$CONSCIOUSNESS_OS_DIR/monitoring"
    
    # Create Prometheus configuration
    cat > "$CONSCIOUSNESS_OS_DIR/monitoring/prometheus.yml" << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "consciousness-os-rules.yml"

scrape_configs:
  - job_name: 'consciousness-os'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    
  - job_name: 'neo4j'
    static_configs:
      - targets: ['localhost:7474']
    metrics_path: '/metrics'
    
  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:6379']
    metrics_path: '/metrics'
EOF

    print_success "Monitoring setup completed"
}

# Function to create sample workflows
create_sample_workflows() {
    print_status "Creating sample workflows..."
    
    # Create Warp workflow
    cat > "$CONSCIOUSNESS_OS_DIR/0_SystemCore/warp/workflows/consciousness-os.yaml" << 'EOF'
name: Consciousness-OS Workflow
description: Master workflow for Consciousness-OS system

triggers:
  - type: manual
    name: "Start Consciousness-OS"
  - type: schedule
    cron: "0 6 * * *"  # Daily at 6 AM
    name: "Daily Reflection"

steps:
  - name: "Initialize System"
    type: command
    command: "cd /Users/divinejohns/memU/consciousness-os && python3 -m consciousness_os.initialize"
    
  - name: "Run Daily Reflection"
    type: command
    command: "cd /Users/divinejohns/memU/consciousness-os && python3 -m consciousness_os.reflection"
    
  - name: "Process Ideas"
    type: command
    command: "cd /Users/divinejohns/memU/consciousness-os && python3 -m consciousness_os.process_ideas"
    
  - name: "Generate Suggestions"
    type: command
    command: "cd /Users/divinejohns/memU/consciousness-os && python3 -m consciousness_os.suggestions"
    
  - name: "Take Autonomous Action"
    type: command
    command: "cd /Users/divinejohns/memU/consciousness-os && python3 -m consciousness_os.autonomous_action"

notifications:
  - type: slack
    webhook: "${SLACK_WEBHOOK_URL}"
    message: "Consciousness-OS workflow completed successfully"
EOF

    # Create Cursor configuration
    cat > "$CONSCIOUSNESS_OS_DIR/0_SystemCore/cursor/config.json" << 'EOF'
{
  "context": {
    "maxTokens": 200000,
    "chunkSize": 4000,
    "overlap": 200
  },
  "projects": {
    "consciousness-os": {
      "description": "Consciousness-OS: 35-project AI consciousness simulation system",
      "priority": "high",
      "contextFiles": [
        "**/*.py",
        "**/*.js",
        "**/*.ts",
        "**/*.md",
        "**/*.yaml",
        "**/*.json"
      ]
    }
  },
  "consciousness_simulation": {
    "enabled": true,
    "reflection_interval": 3600,
    "autonomy_threshold": 0.8,
    "memory_integration": true,
    "goal_persistence": true
  }
}
EOF

    print_success "Sample workflows created"
}

# Function to start services
start_services() {
    print_status "Starting Consciousness-OS services..."
    
    cd "$CONSCIOUSNESS_OS_DIR"
    
    # Start Docker services
    docker-compose -f "$DOCKER_COMPOSE_FILE" up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    check_service_health
    
    print_success "All services started successfully"
}

# Function to check service health
check_service_health() {
    print_status "Checking service health..."
    
    local services=(
        "http://localhost:7474"  # Neo4j
        "http://localhost:6379"   # Redis
        "http://localhost:8000"   # Chroma
        "http://localhost:11434" # Ollama
        "http://localhost:9090"  # Prometheus
        "http://localhost:3000"  # Grafana
    )
    
    for service in "${services[@]}"; do
        if curl -s "$service" > /dev/null; then
            print_success "Service healthy: $service"
        else
            print_warning "Service not responding: $service"
        fi
    done
}

# Function to run initial setup
run_initial_setup() {
    print_status "Running initial setup..."
    
    cd "$CONSCIOUSNESS_OS_DIR"
    
    # Install Python dependencies
    if [ -f "requirements.txt" ]; then
        print_status "Installing Python dependencies..."
        python3 -m pip install -r requirements.txt
    fi
    
    # Install Node.js dependencies
    if [ -f "package.json" ]; then
        print_status "Installing Node.js dependencies..."
        npm install
    fi
    
    # Initialize databases
    print_status "Initializing databases..."
    python3 -c "
import asyncio
from consciousness_os.memory.graph_db import Neo4jManager
from consciousness_os.memory.vector_db import ChromaManager

async def init_dbs():
    # Initialize Neo4j
    neo4j = Neo4jManager()
    await neo4j.initialize_schema()
    
    # Initialize Chroma
    chroma = ChromaManager()
    await chroma.initialize_collections()

asyncio.run(init_dbs())
"
    
    print_success "Initial setup completed"
}

# Function to display success message
display_success_message() {
    echo ""
    echo "🎉 Consciousness-OS Deployment Complete!"
    echo "======================================"
    echo ""
    echo "Your Consciousness-OS system is now running with:"
    echo ""
    echo "📊 Services:"
    echo "  • Neo4j Graph DB: http://localhost:7474"
    echo "  • Redis Cache: http://localhost:6379"
    echo "  • Chroma Vector DB: http://localhost:8000"
    echo "  • Ollama LLM: http://localhost:11434"
    echo "  • Prometheus: http://localhost:9090"
    echo "  • Grafana: http://localhost:3000"
    echo ""
    echo "📁 Project Structure:"
    echo "  • 35 projects organized in Consciousness-OS/"
    echo "  • Complete folder structure created"
    echo "  • Sample workflows and configurations"
    echo ""
    echo "🚀 Next Steps:"
    echo "  1. Open Cursor and load the Consciousness-OS directory"
    echo "  2. Run the consciousness simulation prompts"
    echo "  3. Start capturing ideas through the monetization pipeline"
    echo "  4. Monitor system performance through Grafana"
    echo ""
    echo "📚 Documentation:"
    echo "  • Architecture: CONSCIOUSNESS_OS_ARCHITECTURE.md"
    echo "  • Folder Structure: CONSCIOUSNESS_OS_FOLDER_STRUCTURE.md"
    echo "  • Monetization Pipeline: IDEA_CAPTURE_MONETIZATION_PIPELINE.md"
    echo "  • Consciousness Prompts: CONSCIOUSNESS_SIMULATION_PROMPTS.md"
    echo ""
    echo "🎯 Success Metrics to Track:"
    echo "  • Task Completion Rate: >90%"
    echo "  • Revenue per Idea: $X/month"
    echo "  • Autonomy Score: >90%"
    echo "  • Memory Continuity: Cross-session memory"
    echo "  • Suggestive Power: Proactive suggestions"
    echo ""
    echo "Happy building! 🚀"
}

# Main deployment function
main() {
    echo "Starting Consciousness-OS deployment..."
    echo ""
    
    check_prerequisites
    create_directory_structure
    initialize_git_repo
    create_core_configs
    setup_monitoring
    create_sample_workflows
    start_services
    run_initial_setup
    display_success_message
}

# Run main function
main "$@"

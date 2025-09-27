#!/bin/bash

# IZA OS Warp Commands
# Quick CLI macros for common operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# IZA OS root directory
IZA_ROOT="/Users/divinejohns/memU/iza-os-cursor"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Command: Spawn Agent
spawn_agent() {
    local agent_type=${1:-"claude"}
    print_info "Spawning $agent_type agent..."
    
    cd "$IZA_ROOT"
    python3 2-ai-agents/claude/agent_manager.py spawn "$agent_type"
    
    if [ $? -eq 0 ]; then
        print_status "$agent_type agent spawned successfully"
    else
        print_error "Failed to spawn $agent_type agent"
        exit 1
    fi
}

# Command: Deploy MCP Server
deploy_mcp() {
    local mcp_name=${1:-"finance"}
    print_info "Deploying $mcp_name MCP server..."
    
    cd "$IZA_ROOT"
    python3 1-core-orchestration/mcp/server.py deploy "$mcp_name"
    
    if [ $? -eq 0 ]; then
        print_status "$mcp_name MCP server deployed successfully"
    else
        print_error "Failed to deploy $mcp_name MCP server"
        exit 1
    fi
}

# Command: Build RAG Index
build_rag() {
    print_info "Building RAG index..."
    
    cd "$IZA_ROOT"
    python3 3-knowledge-management/rag/indexer.py
    
    if [ $? -eq 0 ]; then
        print_status "RAG index built successfully"
    else
        print_error "Failed to build RAG index"
        exit 1
    fi
}

# Command: System Status
system_status() {
    print_info "IZA OS System Status"
    echo "====================="
    
    cd "$IZA_ROOT"
    
    # Check Docker services
    echo "🐳 Docker Services:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(iza|mcp|agent)" || echo "No IZA OS services running"
    
    echo ""
    echo "🤖 Active Agents:"
    python3 2-ai-agents/claude/agent_manager.py list 2>/dev/null || echo "No agents running"
    
    echo ""
    echo "🔌 MCP Servers:"
    python3 1-core-orchestration/mcp/server.py list 2>/dev/null || echo "No MCP servers running"
    
    echo ""
    echo "📊 System Resources:"
    echo "CPU: $(top -l 1 | grep "CPU usage" | awk '{print $3}')"
    echo "Memory: $(top -l 1 | grep "PhysMem" | awk '{print $2}')"
}

# Command: Start Services
start_services() {
    print_info "Starting IZA OS services..."
    
    cd "$IZA_ROOT"
    docker compose -f 4-security-api/infra/docker-compose.yaml up -d --build
    
    if [ $? -eq 0 ]; then
        print_status "Services started successfully"
        print_info "Dashboard available at: http://localhost:8501"
        print_info "MCP Server available at: http://localhost:8080"
    else
        print_error "Failed to start services"
        exit 1
    fi
}

# Command: Stop Services
stop_services() {
    print_info "Stopping IZA OS services..."
    
    cd "$IZA_ROOT"
    docker compose -f 4-security-api/infra/docker-compose.yaml down
    
    if [ $? -eq 0 ]; then
        print_status "Services stopped successfully"
    else
        print_error "Failed to stop services"
        exit 1
    fi
}

# Command: Clean Workspace
clean_workspace() {
    print_info "Cleaning IZA OS workspace..."
    
    cd "$IZA_ROOT"
    
    # Remove Python cache
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Remove temporary files
    find . -name "*.tmp" -delete 2>/dev/null || true
    find . -name "*.log" -delete 2>/dev/null || true
    
    # Clean Docker
    docker system prune -f
    
    print_status "Workspace cleaned successfully"
}

# Command: Test System
test_system() {
    print_info "Testing IZA OS system..."
    
    cd "$IZA_ROOT"
    
    # Test MCP server
    print_info "Testing MCP server..."
    curl -f http://localhost:8080/health > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_status "MCP server responding"
    else
        print_warning "MCP server not responding"
    fi
    
    # Test RAG system
    print_info "Testing RAG system..."
    python3 3-knowledge-management/rag/retriever.py test 2>/dev/null
    if [ $? -eq 0 ]; then
        print_status "RAG system working"
    else
        print_warning "RAG system not responding"
    fi
    
    # Test agents
    print_info "Testing agents..."
    python3 2-ai-agents/claude/agent_manager.py list > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_status "Agent manager working"
    else
        print_warning "Agent manager not responding"
    fi
    
    print_status "System test completed"
}

# Main command dispatcher
case "$1" in
    "spawn-agent")
        spawn_agent "$2"
        ;;
    "deploy-mcp")
        deploy_mcp "$2"
        ;;
    "build-rag")
        build_rag
        ;;
    "status")
        system_status
        ;;
    "start")
        start_services
        ;;
    "stop")
        stop_services
        ;;
    "clean")
        clean_workspace
        ;;
    "test")
        test_system
        ;;
    *)
        echo "IZA OS Warp Commands"
        echo "==================="
        echo ""
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  spawn-agent [type]    Spawn a new agent (claude, local_llm, fellou)"
        echo "  deploy-mcp [name]      Deploy an MCP server (finance, research)"
        echo "  build-rag             Build the RAG index"
        echo "  status                Show system status"
        echo "  start                 Start all services"
        echo "  stop                  Stop all services"
        echo "  clean                 Clean workspace"
        echo "  test                  Test system components"
        echo ""
        echo "Examples:"
        echo "  $0 spawn-agent claude"
        echo "  $0 deploy-mcp finance"
        echo "  $0 status"
        ;;
esac

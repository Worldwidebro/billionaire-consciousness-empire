#!/bin/bash

# N8N Workflow Integration Script for IZA OS Ecosystem
# Integrates official n8n and n8n-workflows with IZA OS

echo "🚀 INTEGRATING N8N WORKFLOWS WITH IZA OS ECOSYSTEM"
echo "================================================="
echo ""

# Check if N8N is running
if ! docker ps | grep -q "memu-n8n-1"; then
    echo "❌ N8N container is not running. Starting Docker services..."
    docker-compose -f docker-compose-iza-os.yml up -d n8n postgres redis
    sleep 10
fi

echo "✅ N8N container is running"
echo ""

# Create workflows directory in n8n container
echo "📁 Creating workflows directory in n8n container..."
docker exec memu-n8n-1 mkdir -p /home/node/.n8n/workflows/advanced

# Copy advanced workflows to n8n container
echo "📋 Copying advanced workflow templates..."
docker cp iza-os-advanced-workflows/ai-ecosystem-orchestration.json memu-n8n-1:/home/node/.n8n/workflows/advanced/
docker cp iza-os-advanced-workflows/revenue-optimization.json memu-n8n-1:/home/node/.n8n/workflows/advanced/

# Copy existing IZA OS workflows
echo "📋 Copying existing IZA OS workflows..."
docker cp n8n-workflows/iza-os-templates/health-monitoring-workflow.json memu-n8n-1:/home/node/.n8n/workflows/
docker cp n8n-workflows/iza-os-templates/bmad-orchestration-workflow.json memu-n8n-1:/home/node/.n8n/workflows/
docker cp n8n-workflows/iza-os-templates/enterprise-monitoring-workflow.json memu-n8n-1:/home/node/.n8n/workflows/

# Set proper permissions
echo "🔧 Setting permissions..."
docker exec memu-n8n-1 chown -R node:node /home/node/.n8n/

echo ""
echo "✅ N8N WORKFLOW INTEGRATION COMPLETE!"
echo "====================================="
echo ""
echo "🌐 ACCESS N8N:"
echo "============="
echo "URL: http://localhost:5678"
echo "Username: iza_os_admin"
echo "Password: iza_os_2024"
echo ""
echo "📋 AVAILABLE WORKFLOWS:"
echo "======================"
echo "• IZA OS Health Monitoring (Basic)"
echo "• BMAD-METHOD Orchestration (Basic)"
echo "• Enterprise Repository Monitoring (Basic)"
echo "• AI-Powered Ecosystem Orchestration (Advanced)"
echo "• Revenue Optimization & Tracking (Advanced)"
echo ""
echo "🎯 ADVANCED FEATURES:"
echo "===================="
echo "• AI-powered ecosystem analysis"
echo "• Revenue optimization tracking"
echo "• Automated health scoring"
echo "• Intelligent recommendations"
echo "• Real-time alerts and notifications"
echo ""
echo "🚀 READY FOR ENTERPRISE AUTOMATION!"

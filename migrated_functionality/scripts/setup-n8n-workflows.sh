#!/bin/bash

# N8N Workflow Setup Script for IZA OS Ecosystem

echo "🚀 SETTING UP N8N WORKFLOWS FOR IZA OS ECOSYSTEM"
echo "==============================================="
echo ""

# Check if n8n is running
if ! docker ps | grep -q "memu-n8n-1"; then
    echo "❌ N8N container is not running. Starting Docker services..."
    docker-compose -f docker-compose-iza-os.yml up -d n8n postgres redis
    sleep 10
fi

echo "✅ N8N container is running"
echo ""

# Create workflows directory in n8n container
echo "📁 Creating workflows directory in n8n container..."
docker exec memu-n8n-1 mkdir -p /home/node/.n8n/workflows
docker exec memu-n8n-1 mkdir -p /home/node/.n8n/credentials

# Copy workflow templates to n8n container
echo "📋 Copying workflow templates..."
docker cp n8n-workflows/iza-os-templates/health-monitoring-workflow.json memu-n8n-1:/home/node/.n8n/workflows/
docker cp n8n-workflows/iza-os-templates/bmad-orchestration-workflow.json memu-n8n-1:/home/node/.n8n/workflows/
docker cp n8n-workflows/iza-os-templates/enterprise-monitoring-workflow.json memu-n8n-1:/home/node/.n8n/workflows/

# Copy credentials to n8n container
echo "🔐 Copying credentials..."
docker cp n8n-workflows/credentials/iza-os-api-credentials.json memu-n8n-1:/home/node/.n8n/credentials/
docker cp n8n-workflows/credentials/postgresql-credentials.json memu-n8n-1:/home/node/.n8n/credentials/
docker cp n8n-workflows/credentials/redis-credentials.json memu-n8n-1:/home/node/.n8n/credentials/

# Set proper permissions
echo "🔧 Setting permissions..."
docker exec memu-n8n-1 chown -R node:node /home/node/.n8n/

echo ""
echo "✅ N8N WORKFLOW SETUP COMPLETE!"
echo "==============================="
echo ""
echo "🌐 ACCESS N8N:"
echo "============="
echo "URL: http://localhost:5678"
echo "Username: iza_os_admin"
echo "Password: iza_os_2024"
echo ""
echo "📋 AVAILABLE WORKFLOWS:"
echo "======================"
echo "• IZA OS Health Monitoring"
echo "• BMAD-METHOD Orchestration"
echo "• Enterprise Repository Monitoring"
echo ""
echo "🔗 AVAILABLE CREDENTIALS:"
echo "========================"
echo "• IZA OS API"
echo "• PostgreSQL Database"
echo "• Redis Cache"
echo ""
echo "🎯 NEXT STEPS:"
echo "=============="
echo "1. Open http://localhost:5678"
echo "2. Login with iza_os_admin / iza_os_2024"
echo "3. Import workflows from /home/node/.n8n/workflows/"
echo "4. Configure credentials from /home/node/.n8n/credentials/"
echo "5. Activate workflows for automation"
echo ""
echo "🚀 READY FOR PRODUCTION AUTOMATION!"

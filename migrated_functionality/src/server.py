# MCP Server - Central Routing Hub

This is the central MCP (Model Context Protocol) server that routes calls between local LLM, Claude, Vercept, and other APIs.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server Hub                          │
├─────────────────────────────────────────────────────────────┤
│  Request Router                                            │
│  ├── Authentication & Authorization                        │
│  ├── Request Validation & Sanitization                     │
│  ├── Provider Selection & Load Balancing                  │
│  └── Response Formatting & Caching                         │
├─────────────────────────────────────────────────────────────┤
│  Provider Adapters                                         │
│  ├── Claude Adapter (Anthropic API)                        │
│  ├── Local LLM Adapter (Ollama/AnythingLLM)               │
│  ├── Vercept Adapter (Workflow Engine)                     │
│  ├── OpenAI Adapter (GPT Models)                          │
│  └── Custom API Adapters                                   │
├─────────────────────────────────────────────────────────────┤
│  Core Services                                             │
│  ├── Health Monitoring                                     │
│  ├── Metrics Collection                                    │
│  ├── Error Handling & Retry Logic                         │
│  └── Configuration Management                              │
└─────────────────────────────────────────────────────────────┘
```

## API Endpoints

### Core MCP Endpoints
- `POST /mcp/complete` - Text completion request
- `POST /mcp/chat` - Conversational chat request
- `POST /mcp/embed` - Text embedding generation
- `POST /mcp/classify` - Text classification
- `GET /mcp/providers` - List available providers
- `GET /mcp/health` - Health check endpoint

### Agent Integration
- `POST /agents/spawn` - Spawn new agent
- `GET /agents/list` - List active agents
- `POST /agents/{id}/task` - Assign task to agent
- `DELETE /agents/{id}` - Terminate agent

### Workflow Management
- `POST /workflows/execute` - Execute Vercept workflow
- `GET /workflows/status/{id}` - Get workflow status
- `POST /workflows/create` - Create new workflow

## Provider Configuration

```python
PROVIDERS = {
    "claude": {
        "api_key": os.getenv("CLAUDE_API_KEY"),
        "base_url": "https://api.anthropic.com/v1",
        "models": ["claude-3-sonnet", "claude-3-haiku"],
        "rate_limit": 1000,
        "cost_per_token": 0.00015
    },
    "local_llm": {
        "base_url": "http://ollama:11434",
        "models": ["llama2", "codellama", "mistral"],
        "rate_limit": 10000,
        "cost_per_token": 0.0
    },
    "vercept": {
        "api_key": os.getenv("VERCEPT_API_KEY"),
        "base_url": "https://api.vercept.com/v1",
        "workflows": ["content_processing", "agent_orchestration"],
        "rate_limit": 100,
        "cost_per_request": 0.01
    }
}
```

## Request Routing Logic

```python
def route_request(request: MCPRequest) -> MCPResponse:
    """Route request to appropriate provider based on context"""
    
    # 1. Authentication & Authorization
    if not authenticate_request(request):
        return MCPResponse(error="Unauthorized")
    
    # 2. Provider Selection
    provider = select_provider(request)
    
    # 3. Load Balancing
    if provider == "claude" and is_rate_limited("claude"):
        provider = "local_llm"  # Fallback
    
    # 4. Request Processing
    try:
        response = process_with_provider(request, provider)
        cache_response(request, response)
        return response
    except Exception as e:
        # Retry with fallback provider
        return retry_with_fallback(request, e)
```

## Health Monitoring

```python
class HealthMonitor:
    def __init__(self):
        self.metrics = {
            "requests_per_minute": 0,
            "average_response_time": 0,
            "error_rate": 0,
            "provider_status": {}
        }
    
    def check_provider_health(self, provider: str) -> bool:
        """Check if provider is healthy and responsive"""
        try:
            response = requests.get(f"{PROVIDERS[provider]['base_url']}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_system_metrics(self) -> dict:
        """Get comprehensive system metrics"""
        return {
            "uptime": time.time() - self.start_time,
            "total_requests": self.total_requests,
            "active_agents": len(self.active_agents),
            "provider_health": {p: self.check_provider_health(p) for p in PROVIDERS},
            "cache_hit_rate": self.cache_hits / max(self.total_requests, 1)
        }
```

## Error Handling & Retry Logic

```python
class RetryHandler:
    def __init__(self):
        self.max_retries = 3
        self.backoff_factor = 2
    
    def execute_with_retry(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry"""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                
                wait_time = self.backoff_factor ** attempt
                time.sleep(wait_time)
                
                # Try fallback provider on final retry
                if attempt == self.max_retries - 2:
                    kwargs['provider'] = self.get_fallback_provider(kwargs.get('provider'))
```

## Usage Examples

### Basic Completion Request
```python
import requests

response = requests.post("http://localhost:8080/mcp/complete", json={
    "prompt": "Explain IZA OS architecture",
    "provider": "claude",
    "max_tokens": 500,
    "temperature": 0.7
})

result = response.json()
print(result["text"])
```

### Agent Spawning
```python
response = requests.post("http://localhost:8080/agents/spawn", json={
    "agent_type": "claude",
    "name": "research_agent_001",
    "config": {
        "model": "claude-3-sonnet",
        "max_tokens": 1000,
        "temperature": 0.5
    }
})

agent_id = response.json()["agent_id"]
```

### Workflow Execution
```python
response = requests.post("http://localhost:8080/workflows/execute", json={
    "workflow_id": "content_processing",
    "input": {
        "content": "Sample content to process",
        "analysis_type": "sentiment"
    }
})

workflow_id = response.json()["workflow_id"]
```

## Security Features

- **JWT Authentication**: Secure API access
- **Rate Limiting**: Prevent abuse and overuse
- **Input Validation**: Sanitize all inputs
- **Audit Logging**: Track all requests and responses
- **API Key Rotation**: Automatic key management
- **CORS Protection**: Secure cross-origin requests

## Performance Optimizations

- **Response Caching**: Cache frequent requests
- **Connection Pooling**: Reuse HTTP connections
- **Async Processing**: Non-blocking request handling
- **Load Balancing**: Distribute load across providers
- **Circuit Breaker**: Prevent cascade failures
- **Metrics Collection**: Monitor performance and costs

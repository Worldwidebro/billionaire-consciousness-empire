# Claude Agent Integration

Claude MCP wrappers and Vercept calls for IZA OS agent orchestration.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Agent Hub                         │
├─────────────────────────────────────────────────────────────┤
│  Agent Manager                                             │
│  ├── Agent Lifecycle Management                            │
│  ├── Task Distribution & Load Balancing                    │
│  ├── Health Monitoring & Auto-Recovery                     │
│  └── Performance Metrics Collection                        │
├─────────────────────────────────────────────────────────────┤
│  Claude MCP Wrappers                                       │
│  ├── Text Completion Wrapper                               │
│  ├── Conversational Chat Wrapper                           │
│  ├── Code Generation Wrapper                               │
│  └── Analysis & Reasoning Wrapper                         │
├─────────────────────────────────────────────────────────────┤
│  Vercept Integration                                       │
│  ├── Workflow Execution Engine                             │
│  ├── Job Template Management                              │
│  ├── Result Processing & Validation                       │
│  └── Error Handling & Retry Logic                         │
├─────────────────────────────────────────────────────────────┤
│  Agent Types                                               │
│  ├── Research Agent (Knowledge & Analysis)                │
│  ├── Finance Agent (Portfolio & Risk Analysis)            │
│  ├── Marketing Agent (Content & Campaign Management)       │
│  └── Legal Agent (Compliance & Contract Analysis)         │
└─────────────────────────────────────────────────────────────┘
```

## Agent Manager

```python
class ClaudeAgentManager:
    def __init__(self):
        self.agents = {}
        self.task_queue = asyncio.Queue()
        self.health_monitor = HealthMonitor()
        self.vercept_client = VerceptClient()
    
    async def spawn_agent(self, agent_type: str, config: dict) -> str:
        """Spawn a new Claude agent"""
        agent_id = f"{agent_type}_{uuid.uuid4().hex[:8]}"
        
        agent = ClaudeAgent(
            agent_id=agent_id,
            agent_type=agent_type,
            config=config,
            vercept_client=self.vercept_client
        )
        
        # Initialize agent
        await agent.initialize()
        
        # Start agent loop
        asyncio.create_task(agent.run())
        
        # Register agent
        self.agents[agent_id] = agent
        
        return agent_id
    
    async def assign_task(self, agent_id: str, task: dict):
        """Assign task to specific agent"""
        if agent_id not in self.agents:
            raise AgentNotFoundError(f"Agent {agent_id} not found")
        
        agent = self.agents[agent_id]
        await agent.add_task(task)
    
    async def get_agent_status(self, agent_id: str) -> dict:
        """Get agent status and metrics"""
        if agent_id not in self.agents:
            raise AgentNotFoundError(f"Agent {agent_id} not found")
        
        agent = self.agents[agent_id]
        return {
            "agent_id": agent_id,
            "status": agent.status,
            "tasks_completed": agent.tasks_completed,
            "current_task": agent.current_task,
            "performance_metrics": agent.get_metrics(),
            "last_heartbeat": agent.last_heartbeat
        }
```

## Claude Agent Base Class

```python
class ClaudeAgent:
    def __init__(self, agent_id: str, agent_type: str, config: dict, vercept_client):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config
        self.vercept_client = vercept_client
        self.status = "initializing"
        self.tasks_completed = 0
        self.current_task = None
        self.last_heartbeat = time.time()
        
        # Initialize Claude client
        self.claude_client = anthropic.Anthropic(
            api_key=config.get("claude_api_key", os.getenv("CLAUDE_API_KEY"))
        )
        
        # Agent-specific configuration
        self.model = config.get("model", "claude-3-sonnet-20240229")
        self.max_tokens = config.get("max_tokens", 1000)
        self.temperature = config.get("temperature", 0.7)
    
    async def initialize(self):
        """Initialize agent with system prompt and capabilities"""
        system_prompt = self.get_system_prompt()
        
        # Test Claude connection
        try:
            response = await self.claude_client.messages.create(
                model=self.model,
                max_tokens=100,
                temperature=0.1,
                system=system_prompt,
                messages=[{"role": "user", "content": "Initialize agent"}]
            )
            
            self.status = "ready"
            logger.info(f"Agent {self.agent_id} initialized successfully")
            
        except Exception as e:
            self.status = "error"
            logger.error(f"Failed to initialize agent {self.agent_id}: {e}")
            raise
    
    def get_system_prompt(self) -> str:
        """Get system prompt based on agent type"""
        prompts = {
            "research": """
            You are a Research Agent for IZA OS. Your capabilities include:
            - Knowledge retrieval and analysis
            - Document processing and summarization
            - Research task automation
            - Content generation and optimization
            
            Always provide accurate, well-researched responses with proper citations.
            """,
            
            "finance": """
            You are a Finance Agent for IZA OS. Your capabilities include:
            - Portfolio analysis and optimization
            - Risk assessment and management
            - Investment recommendations
            - Financial modeling and valuation
            
            Always provide accurate financial analysis with proper risk disclosures.
            """,
            
            "marketing": """
            You are a Marketing Agent for IZA OS. Your capabilities include:
            - Campaign strategy and execution
            - Content creation and optimization
            - Market analysis and segmentation
            - Brand management and positioning
            
            Always create compelling, targeted content that drives engagement.
            """,
            
            "legal": """
            You are a Legal Agent for IZA OS. Your capabilities include:
            - Contract analysis and review
            - Compliance checking and monitoring
            - Regulatory research and updates
            - Risk assessment and mitigation
            
            Always provide accurate legal analysis with proper disclaimers.
            """
        }
        
        return prompts.get(self.agent_type, prompts["research"])
    
    async def run(self):
        """Main agent loop"""
        self.status = "running"
        
        while self.status == "running":
            try:
                # Process tasks
                await self.process_tasks()
                
                # Update heartbeat
                self.last_heartbeat = time.time()
                
                # Sleep briefly
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Agent {self.agent_id} error: {e}")
                self.status = "error"
                break
    
    async def process_tasks(self):
        """Process pending tasks"""
        if not self.task_queue.empty():
            task = await self.task_queue.get()
            self.current_task = task
            
            try:
                result = await self.execute_task(task)
                await self.handle_task_result(task, result)
                
            except Exception as e:
                logger.error(f"Task execution failed: {e}")
                await self.handle_task_error(task, e)
            
            finally:
                self.current_task = None
                self.tasks_completed += 1
    
    async def execute_task(self, task: dict) -> dict:
        """Execute task using Claude and Vercept"""
        task_type = task.get("type")
        
        if task_type == "claude_completion":
            return await self.execute_claude_completion(task)
        elif task_type == "vercept_workflow":
            return await self.execute_vercept_workflow(task)
        elif task_type == "analysis":
            return await self.execute_analysis(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def execute_claude_completion(self, task: dict) -> dict:
        """Execute Claude completion task"""
        prompt = task.get("prompt")
        context = task.get("context", "")
        
        # Build full prompt with context
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        response = await self.claude_client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": full_prompt}]
        )
        
        return {
            "type": "claude_completion",
            "result": response.content[0].text,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            "timestamp": time.time()
        }
    
    async def execute_vercept_workflow(self, task: dict) -> dict:
        """Execute Vercept workflow task"""
        workflow_id = task.get("workflow_id")
        input_data = task.get("input", {})
        
        # Execute workflow via Vercept client
        result = await self.vercept_client.execute_workflow(
            workflow_id=workflow_id,
            input_data=input_data
        )
        
        return {
            "type": "vercept_workflow",
            "workflow_id": workflow_id,
            "result": result,
            "timestamp": time.time()
        }
```

## Vercept Integration

```python
class VerceptClient:
    def __init__(self):
        self.api_key = os.getenv("VERCEPT_API_KEY")
        self.base_url = os.getenv("VERCEPT_BASE_URL", "https://api.vercept.com/v1")
        self.session = aiohttp.ClientSession()
    
    async def execute_workflow(self, workflow_id: str, input_data: dict) -> dict:
        """Execute Vercept workflow"""
        url = f"{self.base_url}/workflows/{workflow_id}/execute"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with self.session.post(url, json=input_data, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise VerceptError(f"Workflow execution failed: {error_text}")
    
    async def get_workflow_status(self, execution_id: str) -> dict:
        """Get workflow execution status"""
        url = f"{self.base_url}/executions/{execution_id}/status"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise VerceptError(f"Status check failed: {error_text}")
    
    async def create_workflow(self, workflow_config: dict) -> str:
        """Create new Vercept workflow"""
        url = f"{self.base_url}/workflows"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with self.session.post(url, json=workflow_config, headers=headers) as response:
            if response.status == 201:
                result = await response.json()
                return result["workflow_id"]
            else:
                error_text = await response.text()
                raise VerceptError(f"Workflow creation failed: {error_text}")
```

## Agent Types Implementation

### Research Agent
```python
class ResearchAgent(ClaudeAgent):
    def __init__(self, agent_id: str, config: dict, vercept_client):
        super().__init__(agent_id, "research", config, vercept_client)
        self.knowledge_base = KnowledgeBase()
    
    async def execute_research_task(self, task: dict) -> dict:
        """Execute research-specific task"""
        query = task.get("query")
        sources = task.get("sources", [])
        
        # Search knowledge base
        relevant_docs = await self.knowledge_base.search(query, limit=5)
        
        # Build context from sources
        context = "\n".join([doc.content for doc in relevant_docs])
        
        # Generate research response
        prompt = f"""
        Research Query: {query}
        
        Context from Knowledge Base:
        {context}
        
        Please provide a comprehensive research response based on the available information.
        Include citations and suggest additional research directions.
        """
        
        return await self.execute_claude_completion({
            "prompt": prompt,
            "context": context
        })
```

### Finance Agent
```python
class FinanceAgent(ClaudeAgent):
    def __init__(self, agent_id: str, config: dict, vercept_client):
        super().__init__(agent_id, "finance", config, vercept_client)
        self.market_data = MarketDataClient()
    
    async def execute_finance_task(self, task: dict) -> dict:
        """Execute finance-specific task"""
        task_type = task.get("task_type")
        
        if task_type == "portfolio_analysis":
            return await self.analyze_portfolio(task)
        elif task_type == "risk_assessment":
            return await self.assess_risk(task)
        elif task_type == "investment_recommendation":
            return await self.generate_recommendation(task)
        else:
            raise ValueError(f"Unknown finance task type: {task_type}")
    
    async def analyze_portfolio(self, task: dict) -> dict:
        """Analyze investment portfolio"""
        portfolio_data = task.get("portfolio_data")
        
        # Get market data
        market_data = await self.market_data.get_portfolio_data(portfolio_data)
        
        # Build analysis prompt
        prompt = f"""
        Analyze the following investment portfolio:
        
        Portfolio Data:
        {json.dumps(portfolio_data, indent=2)}
        
        Market Data:
        {json.dumps(market_data, indent=2)}
        
        Provide:
        1. Performance analysis
        2. Risk assessment
        3. Diversification analysis
        4. Recommendations for optimization
        """
        
        return await self.execute_claude_completion({
            "prompt": prompt,
            "context": json.dumps(market_data)
        })
```

## Usage Examples

### Spawn Research Agent
```python
# Initialize agent manager
agent_manager = ClaudeAgentManager()

# Spawn research agent
agent_id = await agent_manager.spawn_agent("research", {
    "model": "claude-3-sonnet-20240229",
    "max_tokens": 2000,
    "temperature": 0.3
})

# Assign research task
await agent_manager.assign_task(agent_id, {
    "type": "claude_completion",
    "prompt": "Analyze the latest trends in AI agent orchestration",
    "context": "Focus on enterprise applications and scalability"
})
```

### Execute Vercept Workflow
```python
# Assign Vercept workflow task
await agent_manager.assign_task(agent_id, {
    "type": "vercept_workflow",
    "workflow_id": "content_processing",
    "input": {
        "content": "Sample content to process",
        "analysis_type": "sentiment"
    }
})
```

### Monitor Agent Status
```python
# Get agent status
status = await agent_manager.get_agent_status(agent_id)
print(f"Agent Status: {status['status']}")
print(f"Tasks Completed: {status['tasks_completed']}")
print(f"Performance Metrics: {status['performance_metrics']}")
```

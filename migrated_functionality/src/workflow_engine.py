#!/usr/bin/env python3
"""
Workflow Engine for IZA OS Orchestration System
Coordinates task execution through agents and swarms
"""

import asyncio
import uuid
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import logging
from .agent_registry import AgentRegistry
from .task_queue import TaskQueue, Task, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowPhase(Enum):
    """Workflow execution phases"""
    INITIALIZATION = "initialization"
    AGENT_SELECTION = "agent_selection"
    TASK_EXECUTION = "task_execution"
    RESULT_PROCESSING = "result_processing"
    COMPLETION = "completion"

class Workflow:
    """Workflow representation"""
    
    def __init__(self, workflow_type: str, payload: Dict[str, Any], priority: TaskPriority = TaskPriority.NORMAL):
        self.id = str(uuid.uuid4())
        self.workflow_type = workflow_type
        self.payload = payload
        self.priority = priority
        self.status = WorkflowStatus.PENDING
        self.current_phase = WorkflowPhase.INITIALIZATION
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.assigned_agents: List[str] = []
        self.tasks: List[str] = []  # Task IDs
        self.results: Dict[str, Any] = {}
        self.error: Optional[str] = None
        self.timeout_seconds: int = 1800  # 30 minutes default
        self.metadata: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary"""
        return {
            'id': self.id,
            'workflow_type': self.workflow_type,
            'payload': self.payload,
            'priority': self.priority.value,
            'status': self.status.value,
            'current_phase': self.current_phase.value,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'assigned_agents': self.assigned_agents,
            'tasks': self.tasks,
            'results': self.results,
            'error': self.error,
            'timeout_seconds': self.timeout_seconds,
            'metadata': self.metadata
        }

class WorkflowEngine:
    """Workflow execution engine"""
    
    def __init__(self, 
                 agent_registry: AgentRegistry, 
                 task_queue: TaskQueue,
                 memory_manager=None,
                 mcp_gateway=None,
                 decision_engine=None,
                 n8n_adapter=None):
        self.agent_registry = agent_registry
        self.task_queue = task_queue
        self.memory_manager = memory_manager
        self.mcp_gateway = mcp_gateway
        self.decision_engine = decision_engine
        self.n8n_adapter = n8n_adapter
        self.workflows: Dict[str, Workflow] = {}
        self.running_workflows: Dict[str, asyncio.Task] = {}
        self._shutdown = False
        
    async def start_workflow(self, workflow: Workflow) -> str:
        """Start workflow execution"""
        if self._shutdown:
            raise RuntimeError("Workflow engine is shutting down")
        
        self.workflows[workflow.id] = workflow
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        
        # Start workflow execution asynchronously
        execution_task = asyncio.create_task(self._execute_workflow(workflow))
        self.running_workflows[workflow.id] = execution_task
        
        logger.info(f"Started workflow {workflow.id} of type {workflow.workflow_type}")
        return workflow.id
    
    async def _execute_workflow(self, workflow: Workflow):
        """Execute workflow phases"""
        try:
            # Phase 1: Initialization
            await self._initialize_workflow(workflow)
            
            # Phase 2: Agent Selection
            await self._select_agents(workflow)
            
            # Phase 3: Task Execution
            await self._execute_tasks(workflow)
            
            # Phase 4: Result Processing
            await self._process_results(workflow)
            
            # Phase 5: Completion
            await self._complete_workflow(workflow)
            
        except asyncio.CancelledError:
            workflow.status = WorkflowStatus.CANCELLED
            workflow.completed_at = datetime.now()
            logger.info(f"Workflow {workflow.id} was cancelled")
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.error = str(e)
            workflow.completed_at = datetime.now()
            logger.error(f"Workflow {workflow.id} failed: {e}")
        finally:
            if workflow.id in self.running_workflows:
                del self.running_workflows[workflow.id]
    
    async def _initialize_workflow(self, workflow: Workflow):
        """Initialize workflow"""
        workflow.current_phase = WorkflowPhase.INITIALIZATION
        logger.info(f"Initializing workflow {workflow.id}")
        
        # Add initialization logic here
        await asyncio.sleep(0.1)  # Simulate initialization time
    
    async def _select_agents(self, workflow: Workflow):
        """Select appropriate agents for workflow using decision engine"""
        workflow.current_phase = WorkflowPhase.AGENT_SELECTION
        logger.info(f"Selecting agents for workflow {workflow.id}")
        
        # Use decision engine if available
        if self.decision_engine:
            await self._select_agents_with_decision_engine(workflow)
        else:
            # Fallback to simple selection
            await self._select_agents_simple(workflow)
    
    async def _select_agents_with_decision_engine(self, workflow: Workflow):
        """Select agents using decision engine"""
        try:
            from decision.engine import DecisionContext
            from decision.ml_policies import AgentCapability
            
            # Get all available agents
            all_agents = self.agent_registry.list_agents(status='active')
            
            # Convert to AgentCapability objects
            agent_capabilities = []
            for agent_data in all_agents:
                capability = AgentCapability(
                    agent_id=agent_data.get('id', ''),
                    capabilities=agent_data.get('capabilities', []),
                    performance_score=agent_data.get('performance_score', 0.5),
                    availability=True,
                    specialization=agent_data.get('specialization')
                )
                agent_capabilities.append(capability)
            
            # Create decision context
            task_context = {
                'id': workflow.id,
                'type': workflow.workflow_type,
                'priority': workflow.priority.value,
                'payload': workflow.payload,
                'complexity': self._assess_workflow_complexity(workflow)
            }
            
            context = DecisionContext(
                task=task_context,
                system={"load": "normal", "performance": "good"},
                available_agents=agent_capabilities
            )
            
            # Get memory context if available
            if self.memory_manager:
                memory_context = await self.memory_manager.retrieve_context(
                    agent_id="workflow_engine",
                    context_keys=["recent_decisions", "performance_history"],
                    semantic_query=f"workflow type {workflow.workflow_type}"
                )
                context.memory_context = {
                    'short_term': memory_context.short_term,
                    'long_term': [r.__dict__ for r in memory_context.long_term]
                }
            
            # Evaluate decision
            result = await self.decision_engine.evaluate_decision(context)
            
            # Process decision result
            if result.target_type == 'agent':
                workflow.assigned_agents = [result.target]
                workflow.metadata['decision_reasoning'] = result.reasoning
                workflow.metadata['decision_confidence'] = result.confidence
            elif result.target_type == 'workflow':
                # Route to N8N workflow
                workflow.metadata['n8n_workflow_id'] = result.target
                workflow.metadata['decision_reasoning'] = result.reasoning
                workflow.assigned_agents = []  # No agents needed for N8N
            elif result.target_type == 'human':
                # Escalate to human
                workflow.metadata['escalation_id'] = result.escalation_id
                workflow.metadata['decision_reasoning'] = result.reasoning
                workflow.assigned_agents = []
            
            logger.info(f"Decision engine selected: {result.target_type} - {result.target}")
            
        except Exception as e:
            logger.error(f"Decision engine selection failed: {e}")
            await self._select_agents_simple(workflow)
    
    async def _select_agents_simple(self, workflow: Workflow):
        """Simple agent selection fallback"""
        # Determine required capabilities based on workflow type
        required_capabilities = self._get_required_capabilities(workflow.workflow_type)
        
        # Find suitable agents
        suitable_agents = []
        for capability in required_capabilities:
            agents = self.agent_registry.find_agents_by_capability(capability)
            suitable_agents.extend(agents)
        
        # Remove duplicates and filter by status
        unique_agents = {}
        for agent in suitable_agents:
            agent_id = agent.get('id')
            if agent_id and agent.get('status') == 'active':
                unique_agents[agent_id] = agent
        
        workflow.assigned_agents = list(unique_agents.keys())
        logger.info(f"Selected {len(workflow.assigned_agents)} agents for workflow {workflow.id}")
    
    async def _execute_tasks(self, workflow: Workflow):
        """Execute workflow tasks"""
        workflow.current_phase = WorkflowPhase.TASK_EXECUTION
        logger.info(f"Executing tasks for workflow {workflow.id}")
        
        # Check if this is an N8N workflow
        if workflow.metadata.get('n8n_workflow_id'):
            await self._execute_n8n_workflow(workflow)
        else:
            await self._execute_agent_tasks(workflow)
    
    async def _execute_n8n_workflow(self, workflow: Workflow):
        """Execute N8N workflow"""
        try:
            n8n_workflow_id = workflow.metadata['n8n_workflow_id']
            
            if self.n8n_adapter:
                execution = await self.n8n_adapter.execute_workflow(
                    n8n_workflow_id, 
                    workflow.payload
                )
                
                workflow.results['n8n_execution'] = {
                    'execution_id': execution.execution_id,
                    'status': execution.status.value,
                    'result_data': execution.result_data,
                    'error_message': execution.error_message
                }
                
                if execution.status.value == 'completed':
                    workflow.status = WorkflowStatus.COMPLETED
                else:
                    workflow.status = WorkflowStatus.FAILED
                    workflow.error = execution.error_message
                
                logger.info(f"N8N workflow {n8n_workflow_id} executed for workflow {workflow.id}")
            else:
                workflow.status = WorkflowStatus.FAILED
                workflow.error = "N8N adapter not available"
                
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.error = f"N8N workflow execution failed: {e}"
            logger.error(f"N8N workflow execution failed for workflow {workflow.id}: {e}")
    
    async def _execute_agent_tasks(self, workflow: Workflow):
        """Execute tasks using agents"""
        # Create tasks based on workflow type
        tasks = self._create_workflow_tasks(workflow)
        
        # Enqueue tasks
        for task in tasks:
            task_id = await self.task_queue.enqueue_task(task)
            workflow.tasks.append(task_id)
            
            # Assign to available agent
            if workflow.assigned_agents:
                agent_id = workflow.assigned_agents[0]  # Simple round-robin
                self.task_queue.assign_agent(task_id, agent_id)
        
        # Monitor task execution
        await self._monitor_task_execution(workflow)
    
    async def _monitor_task_execution(self, workflow: Workflow):
        """Monitor task execution progress"""
        while workflow.tasks:
            completed_tasks = []
            
            for task_id in workflow.tasks:
                task_status = self.task_queue.get_task_status(task_id)
                if task_status:
                    status = TaskStatus(task_status['status'])
                    if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                        completed_tasks.append(task_id)
                        
                        if status == TaskStatus.FAILED:
                            logger.warning(f"Task {task_id} failed in workflow {workflow.id}")
                        elif status == TaskStatus.COMPLETED:
                            logger.info(f"Task {task_id} completed in workflow {workflow.id}")
            
            # Remove completed tasks
            for task_id in completed_tasks:
                workflow.tasks.remove(task_id)
            
            if not workflow.tasks:
                break
            
            # Wait before checking again
            await asyncio.sleep(1)
    
    async def _process_results(self, workflow: Workflow):
        """Process workflow results"""
        workflow.current_phase = WorkflowPhase.RESULT_PROCESSING
        logger.info(f"Processing results for workflow {workflow.id}")
        
        # Collect results from completed tasks
        for task_id in workflow.tasks:
            task_status = self.task_queue.get_task_status(task_id)
            if task_status and task_status['status'] == TaskStatus.COMPLETED.value:
                workflow.results[task_id] = task_status.get('result')
    
    async def _complete_workflow(self, workflow: Workflow):
        """Complete workflow execution"""
        workflow.current_phase = WorkflowPhase.COMPLETION
        workflow.status = WorkflowStatus.COMPLETED
        workflow.completed_at = datetime.now()
        logger.info(f"Completed workflow {workflow.id}")
    
    def _get_required_capabilities(self, workflow_type: str) -> List[str]:
        """Get required capabilities for workflow type"""
        capability_map = {
            'site_recreation': ['Project management', 'Interface design', 'Code generation', 'Quality assurance'],
            'business_analysis': ['Portfolio analysis', 'Financial analysis', 'Data analysis'],
            'content_creation': ['Content strategy', 'Copywriting', 'SEO optimization'],
            'research_processing': ['Research analysis', 'Knowledge extraction', 'Document processing'],
            'automation': ['Web scraping', 'Browser automation', 'Workflow automation']
        }
        return capability_map.get(workflow_type, ['General capabilities'])
    
    def _create_workflow_tasks(self, workflow: Workflow) -> List[Task]:
        """Create tasks for workflow execution"""
        tasks = []
        
        if workflow.workflow_type == 'site_recreation':
            # Create tasks for site recreation workflow
            tasks.append(Task('analyze_site', {'url': workflow.payload.get('url')}, workflow.priority))
            tasks.append(Task('design_interface', {'requirements': workflow.payload.get('requirements')}, workflow.priority))
            tasks.append(Task('generate_code', {'design': 'from_previous_task'}, workflow.priority))
            tasks.append(Task('test_quality', {'code': 'from_previous_task'}, workflow.priority))
        
        elif workflow.workflow_type == 'business_analysis':
            # Create tasks for business analysis workflow
            tasks.append(Task('analyze_portfolio', {'businesses': workflow.payload.get('businesses')}, workflow.priority))
            tasks.append(Task('financial_analysis', {'data': 'from_previous_task'}, workflow.priority))
            tasks.append(Task('generate_report', {'analysis': 'from_previous_task'}, workflow.priority))
        
        else:
            # Generic workflow
            tasks.append(Task('execute_workflow', workflow.payload, workflow.priority))
        
        return tasks
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow status and details"""
        workflow = self.workflows.get(workflow_id)
        if workflow:
            return workflow.to_dict()
        return None
    
    def list_workflows(self, status: Optional[WorkflowStatus] = None) -> List[Dict[str, Any]]:
        """List workflows with optional filtering"""
        workflows = list(self.workflows.values())
        
        if status:
            workflows = [w for w in workflows if w.status == status]
        
        return [workflow.to_dict() for workflow in workflows]
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel workflow execution"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            logger.error(f"Workflow not found: {workflow_id}")
            return False
        
        if workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]:
            logger.warning(f"Cannot cancel workflow in status {workflow.status.value}: {workflow_id}")
            return False
        
        # Cancel running workflow task
        if workflow_id in self.running_workflows:
            self.running_workflows[workflow_id].cancel()
        
        # Cancel all associated tasks
        for task_id in workflow.tasks:
            await self.task_queue.cancel_task(task_id)
        
        workflow.status = WorkflowStatus.CANCELLED
        workflow.completed_at = datetime.now()
        logger.info(f"Cancelled workflow: {workflow_id}")
        return True
    
    def route_to_agent(self, task: Task, agent_id: str) -> bool:
        """Route task to specific agent"""
        return self.task_queue.assign_agent(task.id, agent_id)
    
    def handle_results(self, task_id: str, result: Any, error: Optional[str] = None) -> bool:
        """Handle task execution results"""
        return self.task_queue.complete_task(task_id, result, error)
    
    def _assess_workflow_complexity(self, workflow: Workflow) -> int:
        """Assess workflow complexity (1-10 scale)"""
        complexity = 1
        
        # Base complexity from workflow type
        type_complexity = {
            'simple': 2,
            'data_processing': 4,
            'automation': 5,
            'integration': 6,
            'complex': 8,
            'critical': 10
        }
        
        complexity = type_complexity.get(workflow.workflow_type, 3)
        
        # Adjust based on payload size
        payload_size = len(str(workflow.payload))
        if payload_size > 10000:
            complexity += 2
        elif payload_size > 1000:
            complexity += 1
        
        # Adjust based on priority
        if workflow.priority == TaskPriority.HIGH:
            complexity += 1
        elif workflow.priority == TaskPriority.CRITICAL:
            complexity += 2
        
        return min(complexity, 10)
    
    def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow engine statistics"""
        total_workflows = len(self.workflows)
        pending_workflows = len([w for w in self.workflows.values() if w.status == WorkflowStatus.PENDING])
        running_workflows = len([w for w in self.workflows.values() if w.status == WorkflowStatus.RUNNING])
        completed_workflows = len([w for w in self.workflows.values() if w.status == WorkflowStatus.COMPLETED])
        failed_workflows = len([w for w in self.workflows.values() if w.status == WorkflowStatus.FAILED])
        cancelled_workflows = len([w for w in self.workflows.values() if w.status == WorkflowStatus.CANCELLED])
        
        return {
            'total_workflows': total_workflows,
            'pending_workflows': pending_workflows,
            'running_workflows': running_workflows,
            'completed_workflows': completed_workflows,
            'failed_workflows': failed_workflows,
            'cancelled_workflows': cancelled_workflows
        }
    
    async def shutdown(self):
        """Gracefully shutdown workflow engine"""
        self._shutdown = True
        
        # Cancel all running workflows
        for workflow_id, running_task in self.running_workflows.items():
            running_task.cancel()
        
        # Wait for running workflows to complete
        if self.running_workflows:
            await asyncio.gather(*self.running_workflows.values(), return_exceptions=True)
        
        logger.info("Workflow engine shutdown complete")

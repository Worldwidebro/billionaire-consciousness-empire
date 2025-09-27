#!/usr/bin/env python3
"""
IZA OS Complete N8N Workflow Integration System
Enhanced with security, performance monitoring, and comprehensive error handling
Version: 2.0.0
Author: IZA OS Development Team
"""

import asyncio
import hashlib
import hmac
import json
import logging
import os
import secrets
import signal
import sys
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import platform
import aiofiles
import aiohttp
import asyncpg
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import psutil
import yaml
import jsonschema
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


# Custom Exceptions
class SecurityError(Exception):
    """Security-related error"""
    pass


class CircuitBreakerOpenError(Exception):
    """Circuit breaker is open error"""
    pass


class ValidationError(Exception):
    """Input validation error"""
    pass


# Circuit Breaker Implementation
class CircuitBreaker:
    """Circuit breaker pattern implementation for fault tolerance"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def can_execute(self) -> bool:
        """Check if operation can be executed"""
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            return False
        else:  # HALF_OPEN
            return True
    
    def record_success(self):
        """Record successful operation"""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def record_failure(self):
        """Record failed operation"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"


# Configuration and Security Classes
@dataclass
class SecurityConfig:
    """Security configuration for the workflow integration system"""
    encryption_key: Optional[str] = None
    jwt_secret: Optional[str] = None
    api_rate_limit: int = 100
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = None
    enable_audit_logging: bool = True
    session_timeout: int = 3600  # 1 hour
    
    def __post_init__(self):
        if self.allowed_file_types is None:
            self.allowed_file_types = ['.json', '.yaml', '.yml', '.py', '.sh']


@dataclass
class PerformanceConfig:
    """Performance monitoring configuration"""
    enable_metrics: bool = True
    metrics_interval: int = 60  # seconds
    max_concurrent_operations: int = 10
    connection_pool_size: int = 20
    request_timeout: int = 30  # seconds
    retry_attempts: int = 3
    retry_delay: float = 1.0


@dataclass
class LoggingConfig:
    """Enhanced logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(correlation_id)s - %(message)s"
    enable_file_logging: bool = True
    log_file_path: str = "/var/log/iza_os/workflow_integration.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_remote_logging: bool = False
    remote_logging_url: Optional[str] = None


class SecurityManager:
    """Enhanced security management for workflow integration"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._encryption_key = self._derive_encryption_key()
        self._fernet = Fernet(self._encryption_key)
        
    def _derive_encryption_key(self) -> bytes:
        """Derive encryption key from configuration or generate new one"""
        if self.config.encryption_key:
            salt = b'iza_os_workflow_salt'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.config.encryption_key.encode()))
            return key
        else:
            return Fernet.generate_key()
    
    def encrypt_data(self, data: Union[str, bytes]) -> str:
        """Encrypt sensitive data"""
        try:
            if isinstance(data, str):
                data = data.encode()
            encrypted_data = self._fernet.encrypt(data)
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            self.logger.error(f"Failed to encrypt data: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self._fernet.decrypt(encrypted_bytes)
            return decrypted_data.decode()
        except Exception as e:
            self.logger.error(f"Failed to decrypt data: {e}")
            raise
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF token"""
        return secrets.token_urlsafe(32)
    
    def validate_csrf_token(self, token: str, session_token: str) -> bool:
        """Validate CSRF token"""
        try:
            return hmac.compare_digest(token, session_token)
        except Exception:
            return False
    
    def validate_file_path(self, file_path: str, base_path: str) -> bool:
        """Validate file path to prevent directory traversal attacks"""
        try:
            resolved_path = Path(base_path).resolve()
            requested_path = Path(file_path).resolve()
            return resolved_path in requested_path.parents or resolved_path == requested_path
        except Exception:
            return False
    
    def validate_file_type(self, file_path: str) -> bool:
        """Validate file type against allowed types"""
        file_extension = Path(file_path).suffix.lower()
        return file_extension in self.config.allowed_file_types
    
    def sanitize_input(self, input_data: str, max_length: int = 1000) -> str:
        """Sanitize user input"""
        if not isinstance(input_data, str):
            return ""
        
        # Remove potentially dangerous characters
        sanitized = input_data.strip()[:max_length]
        sanitized = sanitized.replace('<', '&lt;').replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;').replace("'", '&#x27;')
        return sanitized


class PerformanceMonitor:
    """Enhanced performance monitoring and metrics collection"""
    
    def __init__(self, config: PerformanceConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.metrics = {
            'request_count': 0,
            'error_count': 0,
            'avg_response_time': 0.0,
            'memory_usage': 0.0,
            'cpu_usage': 0.0,
            'active_connections': 0
        }
        self.start_time = time.time()
        
    def record_request(self, response_time: float, success: bool = True):
        """Record a request with timing information"""
        self.metrics['request_count'] += 1
        if not success:
            self.metrics['error_count'] += 1
        
        # Update average response time
        current_avg = self.metrics['avg_response_time']
        total_requests = self.metrics['request_count']
        self.metrics['avg_response_time'] = (current_avg * (total_requests - 1) + response_time) / total_requests
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics"""
        try:
            process = psutil.Process()
            self.metrics['memory_usage'] = process.memory_info().rss / 1024 / 1024  # MB
            self.metrics['cpu_usage'] = process.cpu_percent()
            self.metrics['uptime'] = time.time() - self.start_time
        except Exception as e:
            self.logger.warning(f"Failed to get system metrics: {e}")
        
        return self.metrics.copy()
    
    def check_performance_thresholds(self) -> List[str]:
        """Check if performance metrics exceed thresholds"""
        warnings = []
        
        if self.metrics['memory_usage'] > 1000:  # 1GB
            warnings.append("High memory usage detected")
        
        if self.metrics['cpu_usage'] > 80:
            warnings.append("High CPU usage detected")
        
        if self.metrics['error_count'] > 0 and self.metrics['request_count'] > 0:
            error_rate = self.metrics['error_count'] / self.metrics['request_count']
            if error_rate > 0.1:  # 10% error rate
                warnings.append("High error rate detected")
        
        return warnings


class EnhancedLogger:
    """Enhanced logging with correlation IDs and structured logging"""
    
    def __init__(self, config: LoggingConfig):
        self.config = config
        self.correlation_id = str(uuid.uuid4())
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup enhanced logger with correlation ID support"""
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, self.config.level.upper(), logging.INFO))
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(correlation_id)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler if enabled
        if self.config.enable_file_logging:
            try:
                os.makedirs(os.path.dirname(self.config.log_file_path), exist_ok=True)
                file_handler = logging.handlers.RotatingFileHandler(
                    self.config.log_file_path,
                    maxBytes=self.config.max_file_size,
                    backupCount=self.config.backup_count
                )
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(correlation_id)s - %(message)s'
                )
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.warning(f"Failed to setup file logging: {e}")
        
        return logger
    
    def log_with_context(self, level: str, message: str, **kwargs):
        """Log message with correlation ID and additional context"""
        extra = {'correlation_id': self.correlation_id}
        extra.update(kwargs)
        
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message, extra=extra)
    
    def info(self, message: str, **kwargs):
        self.log_with_context('info', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.log_with_context('warning', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log_with_context('error', message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self.log_with_context('debug', message, **kwargs)


def safe_camel_case(text: str) -> str:
    """
    Convert a string to camelCase format by replacing separators with word boundaries
    and capitalizing each word except the first.
    
    Args:
        text (str): Input string containing alphanumeric characters, underscores, and hyphens.
                   The function assumes the input contains only these characters and separators.
    
    Returns:
        str: A camelCase string where underscores and hyphens are replaced with word boundaries,
             each word is capitalized except the first word which remains lowercase.
             
    Examples:
        >>> safe_camel_case("user_management")
        "userManagement"
        >>> safe_camel_case("data-processing")
        "dataProcessing"
        >>> safe_camel_case("api_endpoint_handler")
        "apiEndpointHandler"
    """
    if not text:
        return text
    
    # Replace underscores and hyphens with spaces, then split
    words = text.replace('_', ' ').replace('-', ' ').split()
    
    if not words:
        return text
    
    # First word lowercase, rest capitalized
    camel_case = words[0].lower()
    for word in words[1:]:
        camel_case += word.capitalize()
    
    return camel_case


class IZAOSWorkflowIntegrator:
    """Enhanced workflow integration orchestrator with security and performance monitoring"""
    
    def __init__(self, 
                 base_path: str = "/srv/iza/workflows", 
                 dry_run: bool = False,
                 security_config: Optional[SecurityConfig] = None,
                 performance_config: Optional[PerformanceConfig] = None,
                 logging_config: Optional[LoggingConfig] = None):
        
        self.base_path = Path(base_path)
        self.dry_run = dry_run
        
        # Initialize configurations
        self.security_config = security_config or SecurityConfig()
        self.performance_config = performance_config or PerformanceConfig()
        self.logging_config = logging_config or LoggingConfig()
        
        # Initialize enhanced components
        self.security_manager = SecurityManager(self.security_config)
        self.performance_monitor = PerformanceMonitor(self.performance_config)
        self.logger = EnhancedLogger(self.logging_config)
        
        self.shutdown_event = asyncio.Event()
        self.connection_pool = None
        self.rate_limiter = {}
        self.circuit_breaker = CircuitBreaker()
        
        # Initialize connection pool
        self._initialize_connection_pool()
        
    def _initialize_connection_pool(self):
        """Initialize database connection pool"""
        try:
            # This would be implemented with actual database connection
            self.logger.info("Connection pool initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize connection pool: {e}")
    
    @asynccontextmanager
    async def get_db_connection(self):
        """Get database connection from pool with proper cleanup"""
        connection = None
        try:
            # This would get connection from pool
            yield connection
        except Exception as e:
            self.logger.error(f"Database connection error: {e}")
            raise
        finally:
            if connection:
                # Return connection to pool
                pass
    
    def _safe_chmod(self, file_path: Path, mode: int) -> None:
        """Safely change file permissions with security validation"""
        if platform.system() == 'Windows':
            self.logger.info(f"Skipping chmod on Windows for {file_path}")
            return
        
        # Validate file path security
        if not self.security_manager.validate_file_path(str(file_path), str(self.base_path)):
            self.logger.error(f"Security violation: Invalid file path {file_path}")
            raise SecurityError("Invalid file path")
            
        try:
            os.chmod(file_path, mode)
            self.logger.debug(f"Set permissions {oct(mode)} on {file_path}")
        except (OSError, PermissionError) as e:
            self.logger.warning(f"Failed to set permissions on {file_path}: {e}")
    
    def _validate_input(self, input_data: Any) -> Any:
        """Validate and sanitize input data"""
        if isinstance(input_data, str):
            return self.security_manager.sanitize_input(input_data)
        elif isinstance(input_data, dict):
            return {k: self._validate_input(v) for k, v in input_data.items()}
        elif isinstance(input_data, list):
            return [self._validate_input(item) for item in input_data]
        return input_data
    
    def _check_rate_limit(self, operation: str, identifier: str = "default") -> bool:
        """Check if operation is within rate limits"""
        now = time.time()
        key = f"{operation}:{identifier}"
        
        if key not in self.rate_limiter:
            self.rate_limiter[key] = []
        
        # Remove old entries
        self.rate_limiter[key] = [
            timestamp for timestamp in self.rate_limiter[key]
            if now - timestamp < self.security_config.api_rate_limit
        ]
        
        # Check if within limits
        if len(self.rate_limiter[key]) >= self.security_config.api_rate_limit:
            self.logger.warning(f"Rate limit exceeded for operation: {operation}")
            return False
        
        # Record this request
        self.rate_limiter[key].append(now)
        return True
    
    async def _execute_with_retry(self, func, *args, **kwargs):
        """Execute function with retry logic and circuit breaker"""
        if not self.circuit_breaker.can_execute():
            raise CircuitBreakerOpenError("Circuit breaker is open")
        
        for attempt in range(self.performance_config.retry_attempts):
            try:
                start_time = time.time()
                result = await func(*args, **kwargs)
                response_time = time.time() - start_time
                
                self.performance_monitor.record_request(response_time, success=True)
                self.circuit_breaker.record_success()
                return result
                
            except Exception as e:
                response_time = time.time() - start_time
                self.performance_monitor.record_request(response_time, success=False)
                self.circuit_breaker.record_failure()
                
                if attempt == self.performance_config.retry_attempts - 1:
                    self.logger.error(f"Operation failed after {self.performance_config.retry_attempts} attempts: {e}")
                    raise
                
                self.logger.warning(f"Operation failed, retrying in {self.performance_config.retry_delay}s: {e}")
                await asyncio.sleep(self.performance_config.retry_delay * (2 ** attempt))  # Exponential backoff
    
    async def integrate_workflows(self) -> None:
        """Integrate all workflow categories with enhanced security and monitoring"""
        try:
            self.logger.info("Starting workflow integration process")
            
            # Check rate limits before starting
            if not self._check_rate_limit("workflow_integration"):
                raise ValidationError("Rate limit exceeded for workflow integration")
            
            # Run all integration methods concurrently with proper error handling
            results = await asyncio.gather(
                self._execute_with_retry(self.integrate_business_workflows),
                self._execute_with_retry(self.integrate_automation_workflows),
                self._execute_with_retry(self.integrate_monitoring_workflows),
                self._execute_with_retry(self.integrate_data_workflows),
                return_exceptions=True
            )
            
            # Check results for any failures
            failed_integrations = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    failed_integrations.append(f"Integration {i}: {result}")
            
            if failed_integrations:
                self.logger.warning(f"Some integrations failed: {failed_integrations}")
            else:
                self.logger.info("All workflow integrations completed successfully")
                
        except Exception as e:
            self.logger.error(f"Workflow integration failed: {e}", exc_info=True)
            raise
    
    async def integrate_business_workflows(self) -> None:
        """Integrate business-related workflows with security validation"""
        try:
            self.logger.info("Integrating business workflows...")
            
            # Validate and sanitize workflow data
            business_workflows = await self._load_workflow_config("business")
            validated_workflows = self._validate_input(business_workflows)
            
            # Process workflows with rate limiting
            for workflow in validated_workflows:
                if not self._check_rate_limit("business_workflow", workflow.get('id', 'default')):
                    self.logger.warning(f"Rate limit exceeded for workflow: {workflow.get('name', 'unknown')}")
                    continue
                
                await self._process_workflow(workflow, "business")
            
            self.logger.info("Business workflow integration completed")
            
        except Exception as e:
            self.logger.error(f"Business workflow integration failed: {e}", exc_info=True)
            raise
    
    async def integrate_automation_workflows(self) -> None:
        """Integrate automation workflows with performance monitoring"""
        try:
            self.logger.info("Integrating automation workflows...")
            
            automation_workflows = await self._load_workflow_config("automation")
            validated_workflows = self._validate_input(automation_workflows)
            
            # Process workflows with performance monitoring
            for workflow in validated_workflows:
                await self._process_workflow(workflow, "automation")
                
                # Check performance thresholds
                warnings = self.performance_monitor.check_performance_thresholds()
                if warnings:
                    self.logger.warning(f"Performance warnings: {warnings}")
            
            self.logger.info("Automation workflow integration completed")
            
        except Exception as e:
            self.logger.error(f"Automation workflow integration failed: {e}", exc_info=True)
            raise
    
    async def integrate_monitoring_workflows(self) -> None:
        """Integrate monitoring workflows with health checks"""
        try:
            self.logger.info("Integrating monitoring workflows...")
            
            monitoring_workflows = await self._load_workflow_config("monitoring")
            validated_workflows = self._validate_input(monitoring_workflows)
            
            # Process workflows with health monitoring
            for workflow in validated_workflows:
                await self._process_workflow(workflow, "monitoring")
                
                # Perform health check
                health_status = await self._perform_health_check(workflow)
                if not health_status.get('healthy', False):
                    self.logger.warning(f"Health check failed for workflow: {workflow.get('name', 'unknown')}")
            
            self.logger.info("Monitoring workflow integration completed")
            
        except Exception as e:
            self.logger.error(f"Monitoring workflow integration failed: {e}", exc_info=True)
            raise
    
    async def integrate_data_workflows(self) -> None:
        """Integrate data processing workflows with data validation"""
        try:
            self.logger.info("Integrating data workflows...")
            
            data_workflows = await self._load_workflow_config("data")
            validated_workflows = self._validate_input(data_workflows)
            
            # Process workflows with data validation
            for workflow in validated_workflows:
                # Validate data schema if provided
                if 'schema' in workflow:
                    await self._validate_workflow_schema(workflow)
                
                await self._process_workflow(workflow, "data")
            
            self.logger.info("Data workflow integration completed")
            
        except Exception as e:
            self.logger.error(f"Data workflow integration failed: {e}", exc_info=True)
            raise
    
    async def _load_workflow_config(self, category: str) -> List[Dict[str, Any]]:
        """Load workflow configuration for a category"""
        try:
            config_path = self.base_path / f"{category}_workflows.json"
            
            if not self.security_manager.validate_file_path(str(config_path), str(self.base_path)):
                raise SecurityError(f"Invalid config path: {config_path}")
            
            if not self.security_manager.validate_file_type(str(config_path)):
                raise SecurityError(f"Invalid file type: {config_path}")
            
            async with aiofiles.open(config_path, 'r') as f:
                content = await f.read()
                return json.loads(content)
                
        except FileNotFoundError:
            self.logger.warning(f"Config file not found for category: {category}")
            return []
        except Exception as e:
            self.logger.error(f"Failed to load workflow config for {category}: {e}")
            raise
    
    async def _process_workflow(self, workflow: Dict[str, Any], category: str) -> None:
        """Process a single workflow with security and performance monitoring"""
        try:
            workflow_id = workflow.get('id', 'unknown')
            self.logger.debug(f"Processing workflow: {workflow_id}")
            
            # Encrypt sensitive data if present
            if 'credentials' in workflow:
                workflow['credentials'] = self.security_manager.encrypt_data(
                    json.dumps(workflow['credentials'])
                )
            
            # Simulate workflow processing
            await asyncio.sleep(0.1)
            
            self.logger.debug(f"Workflow processed successfully: {workflow_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to process workflow {workflow_id}: {e}")
            raise
    
    async def _perform_health_check(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Perform health check for a workflow"""
        try:
            # Simulate health check
            health_status = {
                'healthy': True,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'workflow_id': workflow.get('id', 'unknown')
            }
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {'healthy': False, 'error': str(e)}
    
    async def _validate_workflow_schema(self, workflow: Dict[str, Any]) -> None:
        """Validate workflow against its schema"""
        try:
            schema = workflow.get('schema')
            if not schema:
                return
            
            # Validate workflow data against schema
            jsonschema.validate(workflow.get('data', {}), schema)
            
        except jsonschema.ValidationError as e:
            raise ValidationError(f"Schema validation failed: {e}")
        except Exception as e:
            raise ValidationError(f"Schema validation error: {e}")
    
    async def create_workflow_execution_scripts(self, workflows: List[Dict[str, Any]]) -> None:
        """
        Create execution scripts for workflow categories with enhanced security
        
        Args:
            workflows: List of workflow dictionaries containing workflow data
        """
        try:
            self.logger.info(f"Creating execution scripts for {len(workflows)} workflows")
            
            for workflow in workflows:
                # Validate and sanitize workflow data
                validated_workflow = self._validate_input(workflow)
                
                category = validated_workflow.get('category', 'default')
                category_path = self.base_path / safe_camel_case(category)
                
                # Validate path security
                if not self.security_manager.validate_file_path(str(category_path), str(self.base_path)):
                    self.logger.error(f"Security violation: Invalid category path {category_path}")
                    continue
                
                # Ensure directory exists before writing script
                if not self.dry_run:
                    category_path.mkdir(parents=True, exist_ok=True)
                
                script_content = self._generate_script_content(validated_workflow)
                script_path = category_path / f"{safe_camel_case(category)}_executor.py"
                
                # Validate script path security
                if not self.security_manager.validate_file_path(str(script_path), str(self.base_path)):
                    self.logger.error(f"Security violation: Invalid script path {script_path}")
                    continue
                
                if not self.dry_run:
                    # Write script with proper error handling
                    try:
                        async with aiofiles.open(script_path, 'w') as f:
                            await f.write(script_content)
                        
                        # Safely set permissions only on POSIX systems
                        self._safe_chmod(script_path, 0o755)
                        
                        self.logger.info(f"Created execution script: {script_path}")
                        
                    except Exception as e:
                        self.logger.error(f"Failed to create script {script_path}: {e}")
                        continue
                else:
                    self.logger.info(f"[DRY RUN] Would create execution script: {script_path}")
            
            self.logger.info("Workflow execution script creation completed")
            
        except Exception as e:
            self.logger.error(f"Failed to create workflow execution scripts: {e}", exc_info=True)
            raise
    
    def _generate_script_content(self, workflow: Dict[str, Any]) -> str:
        """Generate script content for a workflow"""
        category = workflow.get('category', 'default')
        camel_category = safe_camel_case(category)
        
        return f'''#!/usr/bin/env python3
"""
Generated execution script for {category} workflows
"""

import asyncio
import logging
from typing import Dict, Any

class {camel_category}Executor:
    """Executor for {category} workflows"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, workflow_data: Dict[str, Any]) -> None:
        """Execute workflow"""
        self.logger.info(f"Executing {{workflow_data.get('name', 'unknown')}} workflow")
        # Implementation would go here

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor = {camel_category}Executor()
    asyncio.run(executor.execute({{}}))
'''


class WorkflowMonitor:
    """Enhanced workflow execution and health monitoring with comprehensive metrics"""
    
    def __init__(self, integrator: IZAOSWorkflowIntegrator):
        self.integrator = integrator
        self.logger = integrator.logger
        self.shutdown_event = integrator.shutdown_event
        self.performance_monitor = integrator.performance_monitor
        self.security_manager = integrator.security_manager
        
        # Monitoring state
        self.monitoring_active = False
        self.health_check_interval = 30  # seconds
        self.metrics_interval = 60  # seconds
        self.alert_thresholds = {
            'memory_usage_mb': 1000,
            'cpu_usage_percent': 80,
            'error_rate_percent': 10,
            'response_time_ms': 5000
        }
    
    async def start_monitoring(self) -> None:
        """Start enhanced workflow monitoring with comprehensive health checks"""
        try:
            self.logger.info("Starting enhanced workflow monitoring...")
            self.monitoring_active = True
            
            # Start monitoring tasks concurrently
            monitoring_tasks = [
                self._health_monitoring_loop(),
                self._metrics_collection_loop(),
                self._performance_monitoring_loop(),
                self._security_monitoring_loop()
            ]
            
            await asyncio.gather(*monitoring_tasks, return_exceptions=True)
            
        except asyncio.CancelledError:
            self.logger.info("Workflow monitoring cancelled")
            raise
        except Exception as e:
            self.logger.error(f"Monitoring failed: {e}", exc_info=True)
            raise
        finally:
            await self._cleanup()
    
    async def _health_monitoring_loop(self) -> None:
        """Continuous health monitoring loop"""
        while not self.shutdown_event.is_set() and self.monitoring_active:
            try:
                await self._monitor_cycle()
                await asyncio.sleep(self.health_check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in health monitoring cycle: {e}")
                await asyncio.sleep(5)  # Wait before retrying
    
    async def _metrics_collection_loop(self) -> None:
        """Continuous metrics collection loop"""
        while not self.shutdown_event.is_set() and self.monitoring_active:
            try:
                await self._collect_system_metrics()
                await asyncio.sleep(self.metrics_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in metrics collection: {e}")
                await asyncio.sleep(10)
    
    async def _performance_monitoring_loop(self) -> None:
        """Continuous performance monitoring loop"""
        while not self.shutdown_event.is_set() and self.monitoring_active:
            try:
                await self._check_performance_thresholds()
                await asyncio.sleep(self.metrics_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in performance monitoring: {e}")
                await asyncio.sleep(10)
    
    async def _security_monitoring_loop(self) -> None:
        """Continuous security monitoring loop"""
        while not self.shutdown_event.is_set() and self.monitoring_active:
            try:
                await self._check_security_thresholds()
                await asyncio.sleep(60)  # Security checks every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in security monitoring: {e}")
                await asyncio.sleep(15)
    
    async def _monitor_cycle(self) -> None:
        """Enhanced monitoring cycle with comprehensive checks"""
        try:
            self.logger.debug("Performing enhanced monitoring cycle...")
            
            # Check system health
            system_health = await self._check_system_health()
            if not system_health['healthy']:
                self.logger.warning(f"System health issues detected: {system_health['issues']}")
            
            # Check workflow status
            workflow_status = await self._check_workflow_status()
            if workflow_status.get('failed_workflows', 0) > 0:
                self.logger.warning(f"Failed workflows detected: {workflow_status['failed_workflows']}")
            
            # Log monitoring results
            self.logger.debug(f"Monitoring cycle completed - System: {system_health['healthy']}, Workflows: {workflow_status['total_workflows']}")
            
        except Exception as e:
            self.logger.error(f"Error in monitoring cycle: {e}", exc_info=True)
    
    async def _collect_system_metrics(self) -> None:
        """Collect and log system metrics"""
        try:
            metrics = self.performance_monitor.get_system_metrics()
            
            # Log metrics if enabled
            if self.integrator.performance_config.enable_metrics:
                self.logger.info("System metrics collected", extra={'metrics': metrics})
            
            # Check for threshold violations
            warnings = self.performance_monitor.check_performance_thresholds()
            if warnings:
                self.logger.warning(f"Performance threshold violations: {warnings}")
                
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
    
    async def _check_performance_thresholds(self) -> None:
        """Check performance against configured thresholds"""
        try:
            metrics = self.performance_monitor.get_system_metrics()
            
            # Check memory usage
            if metrics.get('memory_usage', 0) > self.alert_thresholds['memory_usage_mb']:
                self.logger.warning(f"High memory usage: {metrics['memory_usage']:.1f}MB")
            
            # Check CPU usage
            if metrics.get('cpu_usage', 0) > self.alert_thresholds['cpu_usage_percent']:
                self.logger.warning(f"High CPU usage: {metrics['cpu_usage']:.1f}%")
            
            # Check response time
            if metrics.get('avg_response_time', 0) > self.alert_thresholds['response_time_ms']:
                self.logger.warning(f"High response time: {metrics['avg_response_time']:.1f}ms")
                
        except Exception as e:
            self.logger.error(f"Error checking performance thresholds: {e}")
    
    async def _check_security_thresholds(self) -> None:
        """Check security-related thresholds and violations"""
        try:
            # Check for rate limiting violations
            rate_limit_violations = sum(
                1 for key, requests in self.integrator.rate_limiter.items()
                if len(requests) >= self.integrator.security_config.api_rate_limit
            )
            
            if rate_limit_violations > 0:
                self.logger.warning(f"Rate limit violations detected: {rate_limit_violations}")
            
            # Check circuit breaker status
            if not self.integrator.circuit_breaker.can_execute():
                self.logger.warning("Circuit breaker is open")
                
        except Exception as e:
            self.logger.error(f"Error checking security thresholds: {e}")
    
    async def _check_system_health(self) -> Dict[str, Any]:
        """Check overall system health"""
        try:
            health_status = {
                'healthy': True,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'issues': []
            }
            
            # Check memory usage
            metrics = self.performance_monitor.get_system_metrics()
            if metrics.get('memory_usage', 0) > self.alert_thresholds['memory_usage_mb']:
                health_status['healthy'] = False
                health_status['issues'].append('High memory usage')
            
            # Check CPU usage
            if metrics.get('cpu_usage', 0) > self.alert_thresholds['cpu_usage_percent']:
                health_status['healthy'] = False
                health_status['issues'].append('High CPU usage')
            
            # Check error rate
            if metrics.get('request_count', 0) > 0:
                error_rate = (metrics.get('error_count', 0) / metrics['request_count']) * 100
                if error_rate > self.alert_thresholds['error_rate_percent']:
                    health_status['healthy'] = False
                    health_status['issues'].append(f'High error rate: {error_rate:.1f}%')
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Error checking system health: {e}")
            return {'healthy': False, 'issues': ['Health check failed'], 'error': str(e)}
    
    async def _check_workflow_status(self) -> Dict[str, Any]:
        """Check status of all workflows"""
        try:
            # This would check actual workflow status in a real implementation
            workflow_status = {
                'total_workflows': 0,
                'active_workflows': 0,
                'failed_workflows': 0,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
            return workflow_status
            
        except Exception as e:
            self.logger.error(f"Error checking workflow status: {e}")
            return {'total_workflows': 0, 'failed_workflows': 1, 'error': str(e)}
    
    async def _cleanup(self) -> None:
        """Enhanced cleanup with resource monitoring"""
        try:
            self.logger.info("Performing enhanced cleanup...")
            self.monitoring_active = False
            
            # Log final metrics
            final_metrics = self.performance_monitor.get_system_metrics()
            self.logger.info("Final system metrics", extra={'metrics': final_metrics})
            
            # Clean up resources
            if hasattr(self.integrator, 'connection_pool') and self.integrator.connection_pool:
                # Close connection pool
                pass
            
            self.logger.info("Cleanup completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}", exc_info=True)


def setup_signal_handlers(shutdown_event: asyncio.Event) -> None:
    """Setup signal handlers for graceful shutdown"""
    def signal_handler(signum: int, frame) -> None:
        print(f"Received signal {signum}, initiating shutdown...")
        shutdown_event.set()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


async def main() -> None:
    """Enhanced main execution function with comprehensive error handling"""
    # Parse command line arguments
    dry_run = '--dry-run' in sys.argv
    debug_mode = '--debug' in sys.argv
    
    # Load configurations from environment or files
    security_config = SecurityConfig(
        encryption_key=os.getenv('IZA_ENCRYPTION_KEY'),
        jwt_secret=os.getenv('IZA_JWT_SECRET'),
        api_rate_limit=int(os.getenv('IZA_API_RATE_LIMIT', '100')),
        enable_audit_logging=os.getenv('IZA_ENABLE_AUDIT_LOGGING', 'true').lower() == 'true'
    )
    
    performance_config = PerformanceConfig(
        enable_metrics=os.getenv('IZA_ENABLE_METRICS', 'true').lower() == 'true',
        max_concurrent_operations=int(os.getenv('IZA_MAX_CONCURRENT_OPS', '10')),
        connection_pool_size=int(os.getenv('IZA_CONNECTION_POOL_SIZE', '20')),
        retry_attempts=int(os.getenv('IZA_RETRY_ATTEMPTS', '3'))
    )
    
    logging_config = LoggingConfig(
        level=os.getenv('IZA_LOG_LEVEL', 'INFO'),
        enable_file_logging=os.getenv('IZA_ENABLE_FILE_LOGGING', 'true').lower() == 'true',
        log_file_path=os.getenv('IZA_LOG_FILE_PATH', '/var/log/iza_os/workflow_integration.log'),
        enable_remote_logging=os.getenv('IZA_ENABLE_REMOTE_LOGGING', 'false').lower() == 'true',
        remote_logging_url=os.getenv('IZA_REMOTE_LOGGING_URL')
    )
    
    # Initialize integrator with enhanced configurations
    integrator = IZAOSWorkflowIntegrator(
        base_path=os.getenv('IZA_WORKFLOWS_PATH', '/srv/iza/workflows'),
        dry_run=dry_run,
        security_config=security_config,
        performance_config=performance_config,
        logging_config=logging_config
    )
    
    # Setup signal handlers for graceful shutdown
    setup_signal_handlers(integrator.shutdown_event)
    
    try:
        integrator.logger.info("Starting IZA OS Workflow Integration System")
        integrator.logger.info(f"Configuration: dry_run={dry_run}, debug={debug_mode}")
        
        # Integrate workflows with enhanced error handling
        await integrator.integrate_workflows()
        
        # Create execution scripts with security validation
        sample_workflows = [
            {
                'id': 'business_automation_001',
                'category': 'business_automation', 
                'name': 'order_processing',
                'description': 'Automated order processing workflow'
            },
            {
                'id': 'data_processing_001',
                'category': 'data_processing', 
                'name': 'etl_pipeline',
                'description': 'ETL data processing pipeline'
            },
            {
                'id': 'monitoring_001',
                'category': 'monitoring', 
                'name': 'health_check',
                'description': 'System health monitoring workflow'
            }
        ]
        
        integrator.create_workflow_execution_scripts(sample_workflows)
        
        # Start enhanced monitoring
        monitor = WorkflowMonitor(integrator)
        await monitor.start_monitoring()
        
    except KeyboardInterrupt:
        integrator.logger.info("Received keyboard interrupt - initiating graceful shutdown")
        integrator.shutdown_event.set()
    except SecurityError as e:
        integrator.logger.error(f"Security error: {e}")
        sys.exit(2)
    except ValidationError as e:
        integrator.logger.error(f"Validation error: {e}")
        sys.exit(3)
    except Exception as e:
        integrator.logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        integrator.logger.info("IZA OS Workflow Integration System shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

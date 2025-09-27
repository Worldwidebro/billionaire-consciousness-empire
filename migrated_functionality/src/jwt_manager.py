# JWT Manager for IZA OS

Handles JWT token generation, validation, and management for secure API access.

## Features

- **Token Generation**: Create JWT tokens with custom claims
- **Token Validation**: Verify token authenticity and expiration
- **Key Management**: Rotate signing keys automatically
- **Role-Based Access**: Implement RBAC with JWT claims
- **Token Refresh**: Handle token refresh workflows
- **Audit Logging**: Track all token operations

## Configuration

```python
JWT_CONFIG = {
    "algorithm": "RS256",
    "private_key_path": "auth/private.pem",
    "public_key_path": "auth/public.pem",
    "token_expiry": 3600,  # 1 hour
    "refresh_expiry": 86400,  # 24 hours
    "issuer": "iza-os",
    "audience": "iza-os-api"
}
```

## Usage

### Token Generation
```python
from jwt_manager import JWTManager

jwt_manager = JWTManager()

# Generate access token
token = jwt_manager.generate_token(
    user_id="user_123",
    roles=["admin", "agent_manager"],
    claims={"project": "iza-os", "environment": "production"}
)

# Generate refresh token
refresh_token = jwt_manager.generate_refresh_token(user_id="user_123")
```

### Token Validation
```python
# Validate token
try:
    payload = jwt_manager.validate_token(token)
    user_id = payload["sub"]
    roles = payload["roles"]
    print(f"Authenticated user: {user_id}")
except JWTError as e:
    print(f"Token validation failed: {e}")
```

### Role-Based Access Control
```python
# Check if user has required role
if jwt_manager.has_role(token, "admin"):
    # Admin-only operation
    pass

# Check multiple roles
if jwt_manager.has_any_role(token, ["admin", "agent_manager"]):
    # Operation allowed for admin or agent_manager
    pass
```

## API Integration

### FastAPI Middleware
```python
from fastapi import FastAPI, Depends, HTTPException
from jwt_manager import JWTManager

app = FastAPI()
jwt_manager = JWTManager()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt_manager.validate_token(token)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['sub']}"}
```

### Agent Authentication
```python
class AgentAuthenticator:
    def __init__(self, jwt_manager: JWTManager):
        self.jwt_manager = jwt_manager
    
    def authenticate_agent(self, token: str) -> dict:
        """Authenticate agent request"""
        try:
            payload = self.jwt_manager.validate_token(token)
            
            # Verify agent-specific claims
            if payload.get("type") != "agent":
                raise JWTError("Invalid agent token")
            
            return payload
        except JWTError as e:
            raise AuthenticationError(f"Agent authentication failed: {e}")
    
    def generate_agent_token(self, agent_id: str, agent_type: str) -> str:
        """Generate token for agent"""
        return self.jwt_manager.generate_token(
            user_id=agent_id,
            roles=["agent"],
            claims={
                "type": "agent",
                "agent_type": agent_type,
                "permissions": self.get_agent_permissions(agent_type)
            }
        )
```

## Key Rotation

```python
class KeyRotator:
    def __init__(self, jwt_manager: JWTManager):
        self.jwt_manager = jwt_manager
        self.rotation_interval = 86400  # 24 hours
    
    def rotate_keys(self):
        """Rotate JWT signing keys"""
        # Generate new key pair
        new_private_key = self.generate_private_key()
        new_public_key = self.extract_public_key(new_private_key)
        
        # Update JWT manager
        self.jwt_manager.update_keys(new_private_key, new_public_key)
        
        # Store old keys for token validation during transition
        self.store_old_keys(self.jwt_manager.private_key, self.jwt_manager.public_key)
        
        # Schedule next rotation
        self.schedule_next_rotation()
    
    def validate_with_old_keys(self, token: str) -> dict:
        """Validate token with old keys if current validation fails"""
        try:
            return self.jwt_manager.validate_token(token)
        except JWTError:
            # Try with old keys
            for old_public_key in self.old_public_keys:
                try:
                    return jwt.decode(token, old_public_key, algorithms=["RS256"])
                except JWTError:
                    continue
            raise JWTError("Token validation failed with all keys")
```

## Security Best Practices

### Token Storage
```python
class SecureTokenStorage:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379)
    
    def store_token(self, token: str, user_id: str, expiry: int):
        """Store token in Redis with expiration"""
        key = f"token:{user_id}:{hashlib.sha256(token.encode()).hexdigest()[:16]}"
        self.redis_client.setex(key, expiry, token)
    
    def revoke_token(self, token: str, user_id: str):
        """Revoke token by removing from storage"""
        key = f"token:{user_id}:{hashlib.sha256(token.encode()).hexdigest()[:16]}"
        self.redis_client.delete(key)
    
    def is_token_revoked(self, token: str, user_id: str) -> bool:
        """Check if token is revoked"""
        key = f"token:{user_id}:{hashlib.sha256(token.encode()).hexdigest()[:16]}"
        return self.redis_client.get(key) is None
```

### Rate Limiting
```python
class TokenRateLimiter:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379)
        self.rate_limits = {
            "token_generation": 10,  # 10 tokens per minute
            "token_validation": 100,  # 100 validations per minute
            "refresh_token": 5  # 5 refresh requests per minute
        }
    
    def check_rate_limit(self, operation: str, user_id: str) -> bool:
        """Check if user has exceeded rate limit for operation"""
        key = f"rate_limit:{operation}:{user_id}"
        current_count = self.redis_client.get(key)
        
        if current_count is None:
            self.redis_client.setex(key, 60, 1)
            return True
        
        if int(current_count) >= self.rate_limits[operation]:
            return False
        
        self.redis_client.incr(key)
        return True
```

## Monitoring and Logging

```python
class JWTAuditLogger:
    def __init__(self):
        self.logger = logging.getLogger("jwt_audit")
        self.logger.setLevel(logging.INFO)
    
    def log_token_generation(self, user_id: str, roles: list, success: bool):
        """Log token generation attempt"""
        self.logger.info({
            "event": "token_generation",
            "user_id": user_id,
            "roles": roles,
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_token_validation(self, token_hash: str, user_id: str, success: bool):
        """Log token validation attempt"""
        self.logger.info({
            "event": "token_validation",
            "token_hash": token_hash,
            "user_id": user_id,
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_security_event(self, event_type: str, details: dict):
        """Log security-related events"""
        self.logger.warning({
            "event": "security_event",
            "type": event_type,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        })
```

## Error Handling

```python
class JWTError(Exception):
    """Base JWT error"""
    pass

class TokenExpiredError(JWTError):
    """Token has expired"""
    pass

class InvalidTokenError(JWTError):
    """Token is invalid or malformed"""
    pass

class InsufficientPermissionsError(JWTError):
    """User lacks required permissions"""
    pass

class RateLimitExceededError(JWTError):
    """Rate limit exceeded"""
    pass

def handle_jwt_error(func):
    """Decorator to handle JWT errors gracefully"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TokenExpiredError:
            return {"error": "Token expired", "code": "TOKEN_EXPIRED"}
        except InvalidTokenError:
            return {"error": "Invalid token", "code": "INVALID_TOKEN"}
        except InsufficientPermissionsError:
            return {"error": "Insufficient permissions", "code": "INSUFFICIENT_PERMISSIONS"}
        except RateLimitExceededError:
            return {"error": "Rate limit exceeded", "code": "RATE_LIMIT_EXCEEDED"}
        except JWTError as e:
            return {"error": str(e), "code": "JWT_ERROR"}
    return wrapper
```

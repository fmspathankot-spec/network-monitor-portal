from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# ============= AUTH SCHEMAS =============

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data stored in JWT token"""
    username: Optional[str] = None


class UserResponse(BaseModel):
    """User information response (without password)"""
    id: int
    email: str
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= ROUTER SCHEMAS =============

class RouterCreate(BaseModel):
    """Schema for creating a new router"""
    name: str
    host: str
    username: str
    password: str
    device_type: str = "cisco_ios"
    location: Optional[str] = None


class RouterUpdate(BaseModel):
    """Schema for updating router configuration"""
    name: Optional[str] = None
    host: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    device_type: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


class RouterResponse(BaseModel):
    """Router information response (without password)"""
    id: int
    name: str
    host: str
    device_type: str
    location: Optional[str]
    is_active: bool
    status: str
    last_checked: Optional[datetime]
    
    class Config:
        from_attributes = True


# ============= METRIC SCHEMAS =============

class MetricResponse(BaseModel):
    """Historical metric data response"""
    id: int
    router_id: int
    timestamp: datetime
    cpu_usage: Optional[float]
    memory_usage: Optional[float]
    interfaces_up: int
    interfaces_down: int
    bgp_neighbors_up: int
    bgp_neighbors_down: int
    ospf_neighbors_up: int
    ospf_neighbors_down: int
    
    class Config:
        from_attributes = True


# ============= ALERT SCHEMAS =============

class AlertResponse(BaseModel):
    """Alert information response"""
    id: int
    router_id: int
    alert_type: str
    severity: str
    message: str
    details: Optional[dict]
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ============= NETWORK MONITORING SCHEMAS =============

class InterfaceStatus(BaseModel):
    """Interface status information"""
    interface: str
    ip_address: str
    status: str
    protocol: str


class BGPNeighbor(BaseModel):
    """BGP neighbor information"""
    neighbor: str
    version: str
    as_number: str = ""
    state: str
    prefixes: str


class OSPFNeighbor(BaseModel):
    """OSPF neighbor information"""
    neighbor_id: str
    priority: str
    state: str
    dead_time: str
    address: str
    interface: str


class RouterStatusLive(BaseModel):
    """Live router status from SSH connection"""
    router_id: int
    hostname: str
    interfaces: List[InterfaceStatus]
    wan_links: List[InterfaceStatus]
    bgp_neighbors: List[BGPNeighbor]
    ospf_neighbors: List[OSPFNeighbor]
    is_online: bool
    timestamp: datetime


class RouterCredentials(BaseModel):
    """Credentials for SSH connection"""
    host: str
    username: str
    password: str
    device_type: str = "cisco_ios"

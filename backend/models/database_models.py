from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    """
    User model for authentication and authorization.
    
    Stores user credentials and profile information.
    Each user can own multiple routers.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    routers = relationship("Router", back_populates="owner", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")


class Router(Base):
    """
    Router configuration model.
    
    Stores router connection details and credentials.
    In production, passwords should be encrypted using Fernet or similar.
    """
    __tablename__ = "routers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)
    device_type = Column(String, default="cisco_ios")
    location = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime, nullable=True)
    status = Column(String, default="unknown")  # online, offline, unknown, error
    
    # Foreign key
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="routers")
    metrics = relationship("RouterMetric", back_populates="router", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="router", cascade="all, delete-orphan")


class RouterMetric(Base):
    """
    Time-series metrics for routers.
    
    Stores historical data for graphing and analytics.
    Collected by background monitoring service every 60 seconds.
    """
    __tablename__ = "router_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("routers.id"))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Performance Metrics
    cpu_usage = Column(Float, nullable=True)
    memory_usage = Column(Float, nullable=True)
    
    # Interface Metrics
    interface_count = Column(Integer, default=0)
    interfaces_up = Column(Integer, default=0)
    interfaces_down = Column(Integer, default=0)
    
    # BGP Metrics
    bgp_neighbors_up = Column(Integer, default=0)
    bgp_neighbors_down = Column(Integer, default=0)
    
    # OSPF Metrics
    ospf_neighbors_up = Column(Integer, default=0)
    ospf_neighbors_down = Column(Integer, default=0)
    
    # Raw data (JSON) for detailed analysis
    raw_data = Column(JSON, nullable=True)
    
    # Relationship
    router = relationship("Router", back_populates="metrics")


class Alert(Base):
    """
    Alert model for monitoring events.
    
    Stores alerts when interfaces go down, BGP sessions drop, etc.
    Alerts can be resolved when issues are fixed.
    """
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("routers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Alert Information
    alert_type = Column(String, nullable=False)  # interface_down, bgp_down, ospf_down, router_offline
    severity = Column(String, default="warning")  # info, warning, critical
    message = Column(String, nullable=False)
    details = Column(JSON, nullable=True)  # Additional context
    
    # Status
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    router = relationship("Router", back_populates="alerts")
    user = relationship("User", back_populates="alerts")

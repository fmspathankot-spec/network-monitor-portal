from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio


class ConnectionManager:
    """
    Manages WebSocket connections for real-time updates.
    
    This class handles:
    - Accepting new WebSocket connections
    - Storing active connections per user
    - Broadcasting messages to specific users or all users
    - Cleaning up disconnected sockets
    
    WebSocket flow:
    1. Client connects with JWT token
    2. Manager stores connection
    3. Background tasks send updates via manager
    4. Client receives real-time data
    """
    
    def __init__(self):
        # Store active connections: {user_id: [websocket1, websocket2, ...]}
        # One user can have multiple connections (multiple browser tabs)
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """
        Accept new WebSocket connection.
        
        Args:
            websocket: WebSocket connection object
            user_id: ID of the user connecting
        """
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        print(f"✅ User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """
        Remove WebSocket connection.
        
        Args:
            websocket: WebSocket connection to remove
            user_id: ID of the user disconnecting
        """
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            
            # Remove user entry if no more connections
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        print(f"❌ User {user_id} disconnected")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send message to a specific WebSocket connection.
        
        Args:
            message: Dictionary to send (will be JSON encoded)
            websocket: Target WebSocket connection
        """
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"Error sending message: {e}")
    
    async def broadcast_to_user(self, message: dict, user_id: int):
        """
        Send message to all connections of a specific user.
        
        This is useful when a user has multiple browser tabs open.
        All tabs will receive the update.
        
        Args:
            message: Dictionary to broadcast
            user_id: Target user ID
        """
        if user_id not in self.active_connections:
            return
        
        disconnected = []
        
        for connection in self.active_connections[user_id]:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                print(f"Error broadcasting to user {user_id}: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected sockets
        for connection in disconnected:
            self.disconnect(connection, user_id)
    
    async def broadcast_to_all(self, message: dict):
        """
        Send message to all connected users.
        
        Use this for system-wide announcements.
        
        Args:
            message: Dictionary to broadcast to everyone
        """
        for user_id in list(self.active_connections.keys()):
            await self.broadcast_to_user(message, user_id)
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return sum(len(connections) for connections in self.active_connections.values())
    
    def get_user_count(self) -> int:
        """Get number of unique connected users"""
        return len(self.active_connections)


# Global instance - shared across the application
manager = ConnectionManager()

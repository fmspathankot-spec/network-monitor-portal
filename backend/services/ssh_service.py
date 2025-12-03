from netmiko import ConnectHandler
from typing import Dict, List
import re


class RouterSSHService:
    """
    Service class for SSH connections to network routers.
    
    This class uses Netmiko library which simplifies SSH connections
    to network devices. It supports multiple vendor types (Cisco, Juniper, etc.)
    
    Netmiko handles:
    - SSH connection establishment
    - Device-specific prompts
    - Command execution
    - Output parsing
    """
    
    def __init__(self, host: str, username: str, password: str, device_type: str = "cisco_ios"):
        """
        Initialize SSH connection parameters.
        
        Args:
            host: IP address or hostname of router
            username: SSH username
            password: SSH password
            device_type: Device type (cisco_ios, cisco_xe, juniper, etc.)
        """
        self.connection_params = {
            'device_type': device_type,
            'host': host,
            'username': username,
            'password': password,
            'timeout': 30,
            'session_timeout': 60,
        }
        self.connection = None
    
    def connect(self) -> bool:
        """
        Establish SSH connection to the router.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.connection = ConnectHandler(**self.connection_params)
            return True
        except Exception as e:
            print(f"Connection failed to {self.connection_params['host']}: {str(e)}")
            return False
    
    def disconnect(self):
        """Close SSH connection"""
        if self.connection:
            self.connection.disconnect()
    
    def execute_command(self, command: str) -> str:
        """
        Execute a single command and return output.
        
        Args:
            command: CLI command to execute
            
        Returns:
            Command output as string
            
        Raises:
            Exception: If not connected to device
        """
        if not self.connection:
            raise Exception("Not connected to device")
        
        output = self.connection.send_command(command)
        return output
    
    def get_interface_status(self) -> List[Dict]:
        """
        Get all interface statuses.
        
        Executes 'show ip interface brief' and parses output.
        
        Returns:
            List of dictionaries containing interface information
            
        Example output:
            [
                {
                    'interface': 'GigabitEthernet0/0',
                    'ip_address': '192.168.1.1',
                    'status': 'up',
                    'protocol': 'up'
                },
                ...
            ]
        """
        output = self.execute_command("show ip interface brief")
        interfaces = []
        
        # Parse output line by line
        for line in output.split('\n')[1:]:  # Skip header line
            if line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    interfaces.append({
                        'interface': parts[0],
                        'ip_address': parts[1],
                        'status': parts[4],
                        'protocol': parts[5]
                    })
        
        return interfaces
    
    def get_bgp_summary(self) -> Dict:
        """
        Get BGP neighbor summary.
        
        Executes 'show ip bgp summary' and parses output.
        
        Returns:
            Dictionary with BGP neighbor information
        """
        output = self.execute_command("show ip bgp summary")
        neighbors = []
        lines = output.split('\n')
        
        for line in lines:
            # Look for lines starting with IP addresses (BGP neighbors)
            if re.match(r'^\d+\.\d+\.\d+\.\d+', line):
                parts = line.split()
                if len(parts) >= 10:
                    neighbors.append({
                        'neighbor': parts[0],
                        'version': parts[1],
                        'as': parts[2],
                        'state': parts[9] if parts[9].isdigit() else 'Active',
                        'prefixes': parts[9] if parts[9].isdigit() else '0'
                    })
        
        return {
            'neighbors': neighbors,
            'total_neighbors': len(neighbors)
        }
    
    def get_ospf_neighbors(self) -> List[Dict]:
        """
        Get OSPF neighbor information.
        
        Executes 'show ip ospf neighbor' and parses output.
        
        Returns:
            List of OSPF neighbor dictionaries
        """
        output = self.execute_command("show ip ospf neighbor")
        neighbors = []
        
        for line in output.split('\n')[1:]:  # Skip header
            if line.strip() and re.match(r'^\d+\.\d+\.\d+\.\d+', line):
                parts = line.split()
                if len(parts) >= 6:
                    neighbors.append({
                        'neighbor_id': parts[0],
                        'priority': parts[1],
                        'state': parts[2],
                        'dead_time': parts[3],
                        'address': parts[4],
                        'interface': parts[5]
                    })
        
        return neighbors
    
    def get_wan_links_status(self) -> List[Dict]:
        """
        Get WAN link status.
        
        Filters interfaces that are typically used for WAN connections.
        Customize the wan_keywords list based on your naming convention.
        
        Returns:
            List of WAN interface dictionaries
        """
        all_interfaces = self.get_interface_status()
        
        # Filter WAN interfaces (customize based on your naming convention)
        wan_keywords = ['Serial', 'GigabitEthernet0/0', 'Tunnel', 'Dialer', 'WAN']
        wan_links = [
            iface for iface in all_interfaces 
            if any(keyword in iface['interface'] for keyword in wan_keywords)
        ]
        
        return wan_links
    
    def get_l2_services(self) -> Dict:
        """
        Get Layer 2 service information (VLANs, trunks, etc.).
        
        Returns:
            Dictionary with VLAN and trunk information
        """
        try:
            vlan_output = self.execute_command("show vlan brief")
            trunk_output = self.execute_command("show interfaces trunk")
            
            return {
                'vlan_info': vlan_output,
                'trunk_info': trunk_output
            }
        except Exception as e:
            return {
                'vlan_info': f"Error: {str(e)}",
                'trunk_info': f"Error: {str(e)}"
            }
    
    def get_cpu_memory_usage(self) -> Dict:
        """
        Get CPU and memory usage statistics.
        
        Returns:
            Dictionary with CPU and memory usage percentages
        """
        try:
            output = self.execute_command("show processes cpu")
            
            # Parse CPU usage (simplified - adjust based on your device output)
            cpu_match = re.search(r'CPU utilization.*?(\d+)%', output)
            cpu_usage = float(cpu_match.group(1)) if cpu_match else None
            
            # Get memory info
            mem_output = self.execute_command("show memory statistics")
            
            return {
                'cpu_usage': cpu_usage,
                'memory_usage': None  # Parse based on device output format
            }
        except Exception as e:
            return {
                'cpu_usage': None,
                'memory_usage': None
            }

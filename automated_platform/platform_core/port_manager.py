# # port_manager.py

# import os
# import json
# import socket
# from contextlib import closing

# class PortManager:
#     """Manages port allocation for RAG application instances."""
    
#     def __init__(self):
#         self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#         self.ports_file = os.path.join(self.base_dir, "used_ports.json")
#         self.start_port = 8600  # Starting port number
#         self.end_port = 9000    # Ending port number
#         self.used_ports = self._load_used_ports()
    
#     def _load_used_ports(self):
#         """Load the list of used ports from disk."""
#         if os.path.exists(self.ports_file):
#             try:
#                 with open(self.ports_file, 'r') as f:
#                     return json.load(f)
#             except Exception as e:
#                 print(f"Error loading used ports: {str(e)}")
        
#         return []
    
#     def _save_used_ports(self):
#         """Save the list of used ports to disk."""
#         try:
#             with open(self.ports_file, 'w') as f:
#                 json.dump(self.used_ports, f)
#         except Exception as e:
#             print(f"Error saving used ports: {str(e)}")
    
#     def _is_port_in_use(self, port):
#         """Check if a port is currently in use by any process."""
#         with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
#             return s.connect_ex(('localhost', port)) == 0
    
#     def get_available_port(self):
#         """Get an available port for a new instance.
        
#         Returns:
#             int: Available port number
#         """
#         # Iterate through the port range
#         for port in range(self.start_port, self.end_port + 1):
#             if port not in self.used_ports and not self._is_port_in_use(port):
#                 self.used_ports.append(port)
#                 self._save_used_ports()
#                 return port
        
#         # If no ports are available in the range, raise an exception
#         raise RuntimeError("No available ports in the configured range")
    
#     def mark_port_as_used(self, port):
#         """Mark a port as being used.
        
#         Args:
#             port (int): Port number to mark as used
#         """
#         if port not in self.used_ports:
#             self.used_ports.append(port)
#             self._save_used_ports()
    
#     def release_port(self, port):
#         """Release a port that is no longer being used.
        
#         Args:
#             port (int): Port number to release
#         """
#         if port in self.used_ports:
#             self.used_ports.remove(port)
#             self._save_used_ports()








########################

## port_manager.py

import os
import json
import socket
from contextlib import closing

class PortManager:
    """Manages port allocation for RAG application instances."""
    
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.ports_file = os.path.join(self.base_dir, "used_ports.json")
        self.start_port = 8600  # Starting port number
        self.end_port = 9000    # Ending port number
        self.used_ports = self._load_used_ports()
        
        # Debug output
        print(f"PortManager initialized with base_dir: {self.base_dir}")
        print(f"Ports file: {self.ports_file}")
        print(f"Currently used ports: {self.used_ports}")
    
    def _load_used_ports(self):
        """Load the list of used ports from disk."""
        if os.path.exists(self.ports_file):
            try:
                with open(self.ports_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading used ports: {str(e)}")
        
        return []
    
    def _save_used_ports(self):
        """Save the list of used ports to disk."""
        try:
            with open(self.ports_file, 'w') as f:
                json.dump(self.used_ports, f)
        except Exception as e:
            print(f"Error saving used ports: {str(e)}")
    
    def _is_port_in_use(self, port):
        """Check if a port is currently in use by any process."""
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def get_available_port(self):
        """Get an available port for a new instance.
        
        Returns:
            int: Available port number
        """
        # Iterate through the port range
        for port in range(self.start_port, self.end_port + 1):
            # Convert port to int if it's a string
            port_int = int(port)
            
            if port_int not in self.used_ports and not self._is_port_in_use(port_int):
                self.used_ports.append(port_int)
                self._save_used_ports()
                print(f"Port {port_int} assigned as available")
                return port_int
        
        # If no ports are available in the range, raise an exception
        raise RuntimeError("No available ports in the configured range")
    
    def mark_port_as_used(self, port):
        """Mark a port as being used.
        
        Args:
            port (int): Port number to mark as used
        """
        # Convert port to int if it's a string
        port_int = int(port)
        
        if port_int not in self.used_ports:
            self.used_ports.append(port_int)
            self._save_used_ports()
            print(f"Port {port_int} marked as used")
    
    def release_port(self, port):
        """Release a port that is no longer being used.
        
        Args:
            port (int): Port number to release
        """
        # Convert port to int if it's a string
        port_int = int(port)
        
        if port_int in self.used_ports:
            self.used_ports.remove(port_int)
            self._save_used_ports()
            print(f"Port {port_int} released")
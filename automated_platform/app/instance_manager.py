# # instance_manager.py

# import os
# import sys
# import subprocess
# import json
# import time
# import signal
# import psutil
# from pathlib import Path
# import shutil

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".." )))
# from platform_core.config_manager import ConfigManager            ####
# from platform_core.port_manager import PortManager                 ####

# class InstanceManager:
#     """Manages running RAG application instances."""
    
#     def __init__(self):
#         self.config_manager = ConfigManager()
#         self.port_manager = PortManager()
#         self.processes = {}  # Track running processes by instance_id
        
#         # Load existing processes
#         self._load_running_instances()
    
#     def _load_running_instances(self):
#         """Load information about running instances from disk."""
#         processes_file = os.path.join(self.config_manager.base_dir, "processes.json")
#         if os.path.exists(processes_file):
#             try:
#                 with open(processes_file, 'r') as f:
#                     process_data = json.load(f)
                
#                 # Check if processes are actually running
#                 for instance_id, pid in process_data.items():
#                     if self._is_process_running(pid):
#                         self.processes[instance_id] = pid
#             except Exception as e:
#                 print(f"Error loading process data: {str(e)}")
    
#     def _save_running_instances(self):
#         """Save information about running instances to disk."""
#         processes_file = os.path.join(self.config_manager.base_dir, "processes.json")
#         try:
#             with open(processes_file, 'w') as f:
#                 json.dump(self.processes, f)
#         except Exception as e:
#             print(f"Error saving process data: {str(e)}")
    
#     def _is_process_running(self, pid):
#         """Check if a process with the given PID is running."""
#         try:
#             process = psutil.Process(pid)
#             return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             return False
    
#     def start_instance(self, instance_id, port=None):
#         """Start a RAG application instance.
        
#         Args:
#             instance_id (str): Instance ID to start
#             port (int, optional): Port to run the instance on
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         if instance_id in self.processes and self._is_process_running(self.processes[instance_id]):
#             print(f"Instance {instance_id} is already running")
#             return True
        
#         # Get instance configuration
#         config = self.config_manager.load_config(instance_id)
#         if not config:
#             print(f"Instance {instance_id} not found")
#             return False
        
#         # Use provided port or get from config
#         if port is None:
#             port = config.get('port')
#             if port is None:
#                 port = self.port_manager.get_available_port()
#                 config['port'] = port
#                 self.config_manager.save_config(instance_id, config)
        
#         # Get instance directory
#         instance_dir = self.config_manager.get_instance_dir(instance_id)
        
#         # Start the streamlit app
#         try:
#             # Get current environment variables
#             env = os.environ.copy()
            
#             # Update with instance-specific env variables
#             env_file = os.path.join(instance_dir, ".env")
#             if os.path.exists(env_file):
#                 with open(env_file, 'r') as f:
#                     for line in f:
#                         if '=' in line:
#                             key, value = line.strip().split('=', 1)
#                             env[key] = value
            
#             # Set the port for Streamlit
#             env["PORT"] = str(port)
            
#             # Set PYTHONPATH to include the instance directory
#             if "PYTHONPATH" in env:
#                 env["PYTHONPATH"] = f"{instance_dir}:{env['PYTHONPATH']}"
#             else:
#                 env["PYTHONPATH"] = instance_dir
            
#             # Launch the Streamlit app
#             cmd = [
#                 "streamlit", "run",
#                 os.path.join(instance_dir, "app", "main.py"),
#                 "--server.port", str(port),
#                 "--server.address", "localhost",
#                 "--server.headless", "true",
#                 "--browser.serverAddress", "localhost",
#                 "--browser.serverPort", str(port)
#             ]
            
#             # Start the process
#             process = subprocess.Popen(
#                 cmd,
#                 env=env,
#                 cwd=instance_dir,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 start_new_session=True  # Start in a new session so we can terminate it cleanly
#             )
            
#             # Store the process ID
#             self.processes[instance_id] = process.pid
#             self._save_running_instances()
            
#             # Mark port as in use
#             self.port_manager.mark_port_as_used(port)
            
#             print(f"Started instance {instance_id} on port {port} with PID {process.pid}")
#             return True
        
#         except Exception as e:
#             print(f"Error starting instance {instance_id}: {str(e)}")
#             return False
    
#     def stop_instance(self, instance_id):
#         """Stop a running RAG application instance.
        
#         Args:
#             instance_id (str): Instance ID to stop
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         if instance_id not in self.processes:
#             print(f"Instance {instance_id} is not running")
#             return False
        
#         pid = self.processes[instance_id]
        
#         try:
#             # Try to terminate the process gracefully
#             if self._is_process_running(pid):
#                 process = psutil.Process(pid)
#                 process.terminate()
                
#                 # Wait for up to 5 seconds for the process to terminate
#                 for _ in range(10):
#                     if not self._is_process_running(pid):
#                         break
#                     time.sleep(0.5)
                
#                 # If it's still running, kill it forcefully
#                 if self._is_process_running(pid):
#                     process.kill()
            
#             # Release the port
#             config = self.config_manager.load_config(instance_id)
#             if config and 'port' in config:
#                 self.port_manager.release_port(config['port'])
            
#             # Remove from our tracking
#             del self.processes[instance_id]
#             self._save_running_instances()
            
#             print(f"Stopped instance {instance_id}")
#             return True
        
#         except Exception as e:
#             print(f"Error stopping instance {instance_id}: {str(e)}")
#             return False
    
#     def delete_instance(self, instance_id):
#         """Delete a RAG application instance.
        
#         Args:
#             instance_id (str): Instance ID to delete
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         # Stop the instance if it's running
#         if instance_id in self.processes:
#             self.stop_instance(instance_id)
        
#         # Delete the instance directory
#         try:
#             instance_dir = self.config_manager.get_instance_dir(instance_id)
#             if os.path.exists(instance_dir):
#                 shutil.rmtree(instance_dir)
            
#             # Remove from config
#             self.config_manager.delete_config(instance_id)
            
#             print(f"Deleted instance {instance_id}")
#             return True
        
#         except Exception as e:
#             print(f"Error deleting instance {instance_id}: {str(e)}")
#             return False
    
#     def list_instances(self):
#         """List all RAG application instances.
        
#         Returns:
#             list: List of instance dictionaries with their status
#         """
#         instances = []
        
#         # Get all instance configurations
#         configs = self.config_manager.list_configs()
        
#         for instance_id, config in configs.items():
#             is_running = (
#                 instance_id in self.processes and 
#                 self._is_process_running(self.processes[instance_id])
#             )
            
#             instances.append({
#                 "instance_id": instance_id,
#                 "app_name": config.get("app_name", "RAG Application"),
#                 "port": config.get("port"),
#                 "created_at": config.get("created_at", 0),
#                 "running": is_running,
#                 "pid": self.processes.get(instance_id) if is_running else None
#             })
        
#         # Sort by created date, newest first
#         instances.sort(key=lambda x: x["created_at"], reverse=True)
        
#         return instances




##########################################


# instance_manager.py

import os
import sys
import subprocess
import json
import time
import signal
import psutil
from pathlib import Path
import shutil

# Update the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from platform_core.config_manager import ConfigManager
from platform_core.port_manager import PortManager

class InstanceManager:
    """Manages running RAG application instances."""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.port_manager = PortManager()
        self.processes = {}  # Track running processes by instance_id
        
        # Load existing processes
        self._load_running_instances()
    
    def _load_running_instances(self):
        """Load information about running instances from disk."""
        processes_file = os.path.join(self.config_manager.base_dir, "processes.json")
        if os.path.exists(processes_file):
            try:
                with open(processes_file, 'r') as f:
                    process_data = json.load(f)
                
                # Check if processes are actually running
                for instance_id, pid in process_data.items():
                    if self._is_process_running(pid):
                        self.processes[instance_id] = pid
            except Exception as e:
                print(f"Error loading process data: {str(e)}")
    
    def _save_running_instances(self):
        """Save information about running instances to disk."""
        processes_file = os.path.join(self.config_manager.base_dir, "processes.json")
        try:
            with open(processes_file, 'w') as f:
                json.dump(self.processes, f)
        except Exception as e:
            print(f"Error saving process data: {str(e)}")
    
    def _is_process_running(self, pid):
        """Check if a process with the given PID is running."""
        try:
            process = psutil.Process(pid)
            return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False
    

    # Update the start_instance method in instance_manager.py
    def start_instance(self, instance_id, port=None):
        """Start a RAG application instance.
        
        Args:
            instance_id (str): Instance ID to start
            port (int, optional): Port to run the instance on
        
        Returns:
            bool: True if successful, False otherwise
        """
        if instance_id in self.processes and self._is_process_running(self.processes[instance_id]):
            print(f"Instance {instance_id} is already running")
            return True
        
        # Get instance configuration
        config = self.config_manager.load_config(instance_id)
        if not config:
            print(f"Instance {instance_id} not found")
            return False
        
        # Use provided port or get from config
        if port is None:
            port = config.get('port')
            if port is None:
                port = self.port_manager.get_available_port()
                config['port'] = port
                self.config_manager.save_config(instance_id, config)
        
        # Get instance directory
        instance_dir = self.config_manager.get_instance_dir(instance_id)
        
        # Start the streamlit app
        try:
            # Get current environment variables
            env = os.environ.copy()
            
            # Update with instance-specific env variables
            env_file = os.path.join(instance_dir, ".env")
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            env[key] = value
            
            # Set the port for Streamlit
            env["PORT"] = str(port)
            
            # Set PYTHONPATH to include the instance directory
            if "PYTHONPATH" in env:
                env["PYTHONPATH"] = f"{instance_dir};{env['PYTHONPATH']}"
            else:
                env["PYTHONPATH"] = instance_dir
            
            # Ensure the app path exists
            app_path = os.path.join(instance_dir, "app", "main.py")
            if not os.path.exists(app_path):
                print(f"App file not found: {app_path}")
                return False
            
            # IMPORTANT: Use localhost instead of 0.0.0.0 for Windows compatibility
            cmd = [
                "streamlit", "run",
                app_path,
                "--server.port", str(port),
                "--server.address", "localhost",  # Changed from 0.0.0.0 to localhost for Windows
                "--browser.gatherUsageStats", "false"
            ]
            
            print(f"Starting instance with command: {' '.join(cmd)}")
            print(f"Working directory: {instance_dir}")
            
            # Start the process - use shell=True on Windows for better process handling
            process = subprocess.Popen(
                cmd,
                env=env,
                cwd=instance_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True  # Use shell=True on Windows
            )
            
            # Store the process ID
            self.processes[instance_id] = process.pid
            self._save_running_instances()
            
            # Mark port as in use
            self.port_manager.mark_port_as_used(port)
            
            print(f"Started instance {instance_id} on port {port} with PID {process.pid}")
            print(f"Access the application at: http://localhost:{port}")
            
            # Wait a couple seconds to make sure it starts
            time.sleep(2)
            return True
        
        except Exception as e:
            print(f"Error starting instance {instance_id}: {str(e)}")
            return False


    # def start_instance(self, instance_id, port=None):
    #     """Start a RAG application instance.
        
    #     Args:
    #         instance_id (str): Instance ID to start
    #         port (int, optional): Port to run the instance on
        
    #     Returns:
    #         bool: True if successful, False otherwise
    #     """
    #     if instance_id in self.processes and self._is_process_running(self.processes[instance_id]):
    #         print(f"Instance {instance_id} is already running")
    #         return True
        
    #     # Get instance configuration
    #     config = self.config_manager.load_config(instance_id)
    #     if not config:
    #         print(f"Instance {instance_id} not found")
    #         return False
        
    #     # Use provided port or get from config
    #     if port is None:
    #         port = config.get('port')
    #         if port is None:
    #             port = self.port_manager.get_available_port()
    #             config['port'] = port
    #             self.config_manager.save_config(instance_id, config)
        
    #     # Get instance directory
    #     instance_dir = self.config_manager.get_instance_dir(instance_id)
        
    #     # Start the streamlit app
    #     try:
    #         # Get current environment variables
    #         env = os.environ.copy()
            
    #         # Update with instance-specific env variables
    #         env_file = os.path.join(instance_dir, ".env")
    #         if os.path.exists(env_file):
    #             with open(env_file, 'r') as f:
    #                 for line in f:
    #                     if '=' in line:
    #                         key, value = line.strip().split('=', 1)
    #                         env[key] = value
            
    #         # Set the port for Streamlit
    #         env["PORT"] = str(port)
            
    #         # Set PYTHONPATH to include the instance directory
    #         if "PYTHONPATH" in env:
    #             env["PYTHONPATH"] = f"{instance_dir}:{env['PYTHONPATH']}"
    #         else:
    #             env["PYTHONPATH"] = instance_dir
            
    #         # Ensure the app path exists
    #         app_path = os.path.join(instance_dir, "app", "main.py")
    #         if not os.path.exists(app_path):
    #             print(f"App file not found: {app_path}")
    #             return False
            
    #         # Use --server.address 0.0.0.0 to allow connections from outside localhost
    #         cmd = [
    #             "streamlit", "run",
    #             app_path,
    #             "--server.port", str(port),
    #             "--server.address", "0.0.0.0",
    #             "--server.headless", "true",
    #             "--browser.serverAddress", "0.0.0.0",
    #             "--browser.serverPort", str(port)
    #         ]
            
    #         print(f"Starting instance with command: {' '.join(cmd)}")
    #         print(f"Working directory: {instance_dir}")
            
    #         # Start the process
    #         process = subprocess.Popen(
    #             cmd,
    #             env=env,
    #             cwd=instance_dir,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             start_new_session=True  # Start in a new session so we can terminate it cleanly
    #         )
            
    #         # Store the process ID
    #         self.processes[instance_id] = process.pid
    #         self._save_running_instances()
            
    #         # Mark port as in use
    #         self.port_manager.mark_port_as_used(port)
            
    #         print(f"Started instance {instance_id} on port {port} with PID {process.pid}")
    #         return True
        
    #     except Exception as e:
    #         print(f"Error starting instance {instance_id}: {str(e)}")
    #         return False
    
    def stop_instance(self, instance_id):
        """Stop a running RAG application instance.
        
        Args:
            instance_id (str): Instance ID to stop
        
        Returns:
            bool: True if successful, False otherwise
        """
        if instance_id not in self.processes:
            print(f"Instance {instance_id} is not running")
            return False
        
        pid = self.processes[instance_id]
        
        try:
            # Try to terminate the process gracefully
            if self._is_process_running(pid):
                process = psutil.Process(pid)
                process.terminate()
                
                # Wait for up to 5 seconds for the process to terminate
                for _ in range(10):
                    if not self._is_process_running(pid):
                        break
                    time.sleep(0.5)
                
                # If it's still running, kill it forcefully
                if self._is_process_running(pid):
                    process.kill()
            
            # Release the port
            config = self.config_manager.load_config(instance_id)
            if config and 'port' in config:
                self.port_manager.release_port(config['port'])
            
            # Remove from our tracking
            del self.processes[instance_id]
            self._save_running_instances()
            
            print(f"Stopped instance {instance_id}")
            return True
        
        except Exception as e:
            print(f"Error stopping instance {instance_id}: {str(e)}")
            return False
    
    def delete_instance(self, instance_id):
        """Delete a RAG application instance.
        
        Args:
            instance_id (str): Instance ID to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Stop the instance if it's running
        if instance_id in self.processes:
            self.stop_instance(instance_id)
        
        # Delete the instance directory
        try:
            instance_dir = self.config_manager.get_instance_dir(instance_id)
            if os.path.exists(instance_dir):
                shutil.rmtree(instance_dir)
            
            # Remove from config
            self.config_manager.delete_config(instance_id)
            
            print(f"Deleted instance {instance_id}")
            return True
        
        except Exception as e:
            print(f"Error deleting instance {instance_id}: {str(e)}")
            return False
    
    def list_instances(self):
        """List all RAG application instances.
        
        Returns:
            list: List of instance dictionaries with their status
        """
        instances = []
        
        # Get all instance configurations
        configs = self.config_manager.list_configs()
        
        for instance_id, config in configs.items():
            is_running = (
                instance_id in self.processes and 
                self._is_process_running(self.processes[instance_id])
            )
            
            instances.append({
                "instance_id": instance_id,
                "app_name": config.get("app_name", "RAG Application"),
                "port": config.get("port"),
                "created_at": config.get("created_at", 0),
                "running": is_running,
                "pid": self.processes.get(instance_id) if is_running else None
            })
        
        # Sort by created date, newest first
        instances.sort(key=lambda x: x["created_at"], reverse=True)
        
        return instances
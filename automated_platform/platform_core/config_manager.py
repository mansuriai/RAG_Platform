# # config_manager.py

# import os
# import json
# from pathlib import Path

# class ConfigManager:
#     """Manages configurations for RAG application instances."""
    
#     def __init__(self):
#         # Base directory for the automated platform
#         self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
#         # Instances directory
#         self.instances_dir = os.path.join(self.base_dir, "instances")
#         os.makedirs(self.instances_dir, exist_ok=True)
    
#     def get_instance_dir(self, instance_id):
#         """Get the directory for an instance.
        
#         Args:
#             instance_id (str): Instance ID
        
#         Returns:
#             str: Path to the instance directory
#         """
#         return os.path.join(self.instances_dir, instance_id)
    
#     def save_config(self, instance_id, config):
#         """Save configuration for an instance.
        
#         Args:
#             instance_id (str): Instance ID
#             config (dict): Configuration dictionary
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         instance_dir = self.get_instance_dir(instance_id)
#         os.makedirs(instance_dir, exist_ok=True)
        
#         config_file = os.path.join(instance_dir, "config.json")
        
#         try:
#             with open(config_file, 'w') as f:
#                 json.dump(config, f, indent=2)
#             return True
#         except Exception as e:
#             print(f"Error saving config for {instance_id}: {str(e)}")
#             return False
    
#     def load_config(self, instance_id):
#         """Load configuration for an instance.
        
#         Args:
#             instance_id (str): Instance ID
        
#         Returns:
#             dict: Configuration dictionary, or None if not found
#         """
#         config_file = os.path.join(self.get_instance_dir(instance_id), "config.json")
        
#         if not os.path.exists(config_file):
#             return None
        
#         try:
#             with open(config_file, 'r') as f:
#                 return json.load(f)
#         except Exception as e:
#             print(f"Error loading config for {instance_id}: {str(e)}")
#             return None
    
#     def delete_config(self, instance_id):
#         """Delete configuration for an instance.
        
#         Args:
#             instance_id (str): Instance ID
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         config_file = os.path.join(self.get_instance_dir(instance_id), "config.json")
        
#         if os.path.exists(config_file):
#             try:
#                 os.remove(config_file)
#                 return True
#             except Exception as e:
#                 print(f"Error deleting config for {instance_id}: {str(e)}")
#                 return False
        
#         return False
    
#     def list_configs(self):
#         """List all instance configurations.
        
#         Returns:
#             dict: Dictionary mapping instance IDs to configurations
#         """
#         configs = {}
        
#         for dir_name in os.listdir(self.instances_dir):
#             instance_dir = os.path.join(self.instances_dir, dir_name)
            
#             if os.path.isdir(instance_dir):
#                 config_file = os.path.join(instance_dir, "config.json")
                
#                 if os.path.exists(config_file):
#                     try:
#                         with open(config_file, 'r') as f:
#                             config = json.load(f)
#                             configs[dir_name] = config
#                     except Exception as e:
#                         print(f"Error loading config for {dir_name}: {str(e)}")
        
#         return configs



#################################


# # config_manager.py

# import os
# import json
# from pathlib import Path

# class ConfigManager:
#     """Manages configurations for RAG application instances."""
    
#     def __init__(self):
#         # Base directory for the automated platform
#         self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
#         # Instances directory
#         self.instances_dir = os.path.join(self.base_dir, "instances")
#         os.makedirs(self.instances_dir, exist_ok=True)
        
#         # For debugging
#         print(f"ConfigManager initialized with base_dir: {self.base_dir}")
#         print(f"Instances directory: {self.instances_dir}")
    
#     def get_instance_dir(self, instance_id):
#         """Get the directory for an instance.
        
#         Args:
#             instance_id (str): Instance ID
        
#         Returns:
#             str: Path to the instance directory
#         """
#         instance_dir = os.path.join(self.instances_dir, instance_id)
#         print(f"Getting instance directory: {instance_dir}")
#         return instance_dir
    
#     def save_config(self, instance_id, config):
#         """Save configuration for an instance.
        
#         Args:
#             instance_id (str): Instance ID
#             config (dict): Configuration dictionary
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         instance_dir = self.get_instance_dir(instance_id)
#         os.makedirs(instance_dir, exist_ok=True)
        
#         config_file = os.path.join(instance_dir, "config.json")
        
#         try:
#             with open(config_file, 'w') as f:
#                 json.dump(config, f, indent=2)
#             return True
#         except Exception as e:
#             print(f"Error saving config for {instance_id}: {str(e)}")
#             return False
    
#     def load_config(self, instance_id):
#         """Load configuration for an instance.
        
#         Args:
#             instance_id (str): Instance ID
        
#         Returns:
#             dict: Configuration dictionary, or None if not found
#         """
#         config_file = os.path.join(self.get_instance_dir(instance_id), "config.json")
        
#         if not os.path.exists(config_file):
#             print(f"Config file not found: {config_file}")
#             return None
        
#         try:
#             with open(config_file, 'r') as f:
#                 return json.load(f)
#         except Exception as e:
#             print(f"Error loading config for {instance_id}: {str(e)}")
#             return None
    
#     def delete_config(self, instance_id):
#         """Delete configuration for an instance.
        
#         Args:
#             instance_id (str): Instance ID
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         config_file = os.path.join(self.get_instance_dir(instance_id), "config.json")
        
#         if os.path.exists(config_file):
#             try:
#                 os.remove(config_file)
#                 return True
#             except Exception as e:
#                 print(f"Error deleting config for {instance_id}: {str(e)}")
#                 return False
        
#         return False
    
#     def list_configs(self):
#         """List all instance configurations.
        
#         Returns:
#             dict: Dictionary mapping instance IDs to configurations
#         """
#         configs = {}
        
#         # Check if instances directory exists
#         if not os.path.exists(self.instances_dir):
#             print(f"Instances directory does not exist: {self.instances_dir}")
#             return configs
        
#         for dir_name in os.listdir(self.instances_dir):
#             instance_dir = os.path.join(self.instances_dir, dir_name)
            
#             if os.path.isdir(instance_dir):
#                 config_file = os.path.join(instance_dir, "config.json")
                
#                 if os.path.exists(config_file):
#                     try:
#                         with open(config_file, 'r') as f:
#                             config = json.load(f)
#                             configs[dir_name] = config
#                     except Exception as e:
#                         print(f"Error loading config for {dir_name}: {str(e)}")
        
#         return configs






################################3 router .py #####################

# config_manager

import os
import json
from pathlib import Path

class ConfigManager:
    """Manages configurations for RAG application instances."""
    
    def __init__(self):
        # Base directory for the automated platform
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        # Instances directory
        self.instances_dir = os.path.join(self.base_dir, "instances")
        os.makedirs(self.instances_dir, exist_ok=True)
        
        # For debugging
        print(f"ConfigManager initialized with base_dir: {self.base_dir}")
        print(f"Instances directory: {self.instances_dir}")
    
    def get_instance_dir(self, instance_id):
        """Get the directory for an instance.
        
        Args:
            instance_id (str): Instance ID
        
        Returns:
            str: Path to the instance directory
        """
        instance_dir = os.path.join(self.instances_dir, instance_id)
        print(f"Getting instance directory: {instance_dir}")
        return instance_dir
    
    def save_config(self, instance_id, config):
        """Save configuration for an instance.
        
        Args:
            instance_id (str): Instance ID
            config (dict): Configuration dictionary
        
        Returns:
            bool: True if successful, False otherwise
        """
        instance_dir = self.get_instance_dir(instance_id)
        os.makedirs(instance_dir, exist_ok=True)
        
        config_file = os.path.join(instance_dir, "config.json")
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config for {instance_id}: {str(e)}")
            return False
    
    def load_config(self, instance_id):
        """Load configuration for an instance.
        
        Args:
            instance_id (str): Instance ID
        
        Returns:
            dict: Configuration dictionary, or None if not found
        """
        config_file = os.path.join(self.get_instance_dir(instance_id), "config.json")
        
        if not os.path.exists(config_file):
            print(f"Config file not found: {config_file}")
            return None
        
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config for {instance_id}: {str(e)}")
            return None
    
    def delete_config(self, instance_id):
        """Delete configuration for an instance.
        
        Args:
            instance_id (str): Instance ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        config_file = os.path.join(self.get_instance_dir(instance_id), "config.json")
        
        if os.path.exists(config_file):
            try:
                os.remove(config_file)
                return True
            except Exception as e:
                print(f"Error deleting config for {instance_id}: {str(e)}")
                return False
        
        return False
    
    def list_configs(self):
        """List all instance configurations.
        
        Returns:
            dict: Dictionary mapping instance IDs to configurations
        """
        configs = {}
        
        # Check if instances directory exists
        if not os.path.exists(self.instances_dir):
            print(f"Instances directory does not exist: {self.instances_dir}")
            return configs
        
        for dir_name in os.listdir(self.instances_dir):
            instance_dir = os.path.join(self.instances_dir, dir_name)
            
            if os.path.isdir(instance_dir):
                config_file = os.path.join(instance_dir, "config.json")
                
                if os.path.exists(config_file):
                    try:
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                            configs[dir_name] = config
                    except Exception as e:
                        print(f"Error loading config for {dir_name}: {str(e)}")
        
        return configs
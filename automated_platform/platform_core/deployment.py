# #deployment.py

# import os
# import sys
# import shutil
# import subprocess
# from pathlib import Path

# from platform_core.config_manager import ConfigManager             ###

# class DeploymentManager:
#     """Manages deployment of RAG application instances."""
    
#     def __init__(self):
#         self.config_manager = ConfigManager()
    
#     def prepare_deployment(self, instance_id, config):
#         """Prepare deployment files for an instance.
        
#         Args:
#             instance_id (str): Instance ID
#             config (dict): Instance configuration
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         try:
#             # Get instance directory
#             instance_dir = self.config_manager.get_instance_dir(instance_id)
            
#             # Create deployment script
#             self._create_deployment_script(instance_id, config)
            
#             # Create requirements.txt
#             self._create_requirements_file(instance_id)
            
#             return True
#         except Exception as e:
#             print(f"Error preparing deployment for {instance_id}: {str(e)}")
#             return False
    
#     def _create_deployment_script(self, instance_id, config):
#         """Create deployment script for the instance.
        
#         Args:
#             instance_id (str): Instance ID
#             config (dict): Instance configuration
#         """
#         instance_dir = self.config_manager.get_instance_dir(instance_id)
#         script_path = os.path.join(instance_dir, "run.py")
        
#         with open(script_path, 'w') as f:
#             f.write("""import os
# import sys
# import streamlit.web.cli as stcli

# # Get the directory of this script
# dir_path = os.path.dirname(os.path.realpath(__file__))

# # Add the instance directory to the Python path
# sys.path.insert(0, dir_path)

# # Run the Streamlit app
# if __name__ == "__main__":
#     # Get port from environment or use default
#     port = int(os.environ.get("PORT", "8501"))
    
#     sys.argv = [
#         "streamlit", "run",
#         os.path.join(dir_path, "app", "main.py"),
#         "--server.port", str(port),
#         "--server.address", "0.0.0.0",
#         "--server.headless", "true",
#         "--browser.serverAddress", "localhost",
#         "--browser.serverPort", str(port)
#     ]
    
#     sys.exit(stcli.main())
# """)
        
#         # Make the script executable
#         os.chmod(script_path, 0o755)
    
#     def _create_requirements_file(self, instance_id):
#         """Create requirements.txt file for the instance.
        
#         Args:
#             instance_id (str): Instance ID
#         """
#         instance_dir = self.config_manager.get_instance_dir(instance_id)
#         requirements_path = os.path.join(instance_dir, "requirements.txt")
        
#         with open(requirements_path, 'w') as f:
#             f.write("""streamlit>=1.22.0
# langchain>=0.0.270
# langchain_community>=0.0.13
# langchain_huggingface>=0.0.6
# openai>=1.3.0
# anthropic>=0.8.0
# pinecone-client>=2.2.4
# faiss-cpu>=1.7.4
# chromadb>=0.4.10
# sentence-transformers>=2.2.2
# pdfplumber>=0.10.2
# PyPDF2>=3.0.0
# python-dotenv>=1.0.0
# beautifulsoup4>=4.12.2
# requests>=2.31.0
# lxml>=4.9.3
# numpy>=1.24.0
# pandas>=2.0.0
# psutil>=5.9.5
# """)

#     def create_docker_deployment(self, instance_id, config):
#         """Create Docker deployment files for the instance.
        
#         Args:
#             instance_id (str): Instance ID
#             config (dict): Instance configuration
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         try:
#             instance_dir = self.config_manager.get_instance_dir(instance_id)
            
#             # Create Dockerfile
#             dockerfile_path = os.path.join(instance_dir, "Dockerfile")
#             with open(dockerfile_path, 'w') as f:
#                 f.write("""FROM python:3.10-slim

# WORKDIR /app

# # Copy requirements first for better caching
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application
# COPY . .

# # Expose the port the app will run on
# EXPOSE ${PORT:-8501}

# # Command to run the application
# CMD ["python", "run.py"]
# """)
            
#             # Create docker-compose.yml
#             compose_path = os.path.join(instance_dir, "docker-compose.yml")
#             with open(compose_path, 'w') as f:
#                 f.write(f"""version: '3'

# services:
#   rag-app:
#     build: .
#     ports:
#       - "{config.get('port', 8501)}:{config.get('port', 8501)}"
#     environment:
#       - PORT={config.get('port', 8501)}
#     volumes:
#       - ./data:/app/data
#       - ./pdfs:/app/pdfs
#     restart: unless-stopped
# """)
            
#             return True
#         except Exception as e:
#             print(f"Error creating Docker deployment for {instance_id}: {str(e)}")
#             return False

#     def build_and_run_docker(self, instance_id):
#         """Build and run Docker container for the instance.
        
#         Args:
#             instance_id (str): Instance ID
        
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         try:
#             instance_dir = self.config_manager.get_instance_dir(instance_id)
            
#             # Check if Docker is installed
#             try:
#                 subprocess.run(["docker", "--version"], check=True, capture_output=True)
#             except (subprocess.SubprocessError, FileNotFoundError):
#                 print("Docker is not installed or not in PATH")
#                 return False
            
#             # Build and run using docker-compose
#             subprocess.run(
#                 ["docker-compose", "up", "-d", "--build"],
#                 cwd=instance_dir,
#                 check=True
#             )
            
#             return True
#         except Exception as e:
#             print(f"Error building and running Docker for {instance_id}: {str(e)}")
#             return False







################################

## deployment.py

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Update import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from platform_core.config_manager import ConfigManager

class DeploymentManager:
    """Manages deployment of RAG application instances."""
    
    def __init__(self):
        self.config_manager = ConfigManager()
    
    def prepare_deployment(self, instance_id, config):
        """Prepare deployment files for an instance.
        
        Args:
            instance_id (str): Instance ID
            config (dict): Instance configuration
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get instance directory
            instance_dir = self.config_manager.get_instance_dir(instance_id)
            
            # Create deployment script
            self._create_deployment_script(instance_id, config)
            
            # Create requirements.txt
            self._create_requirements_file(instance_id)
            
            # Create batch file for Windows
            self._create_windows_batch_file(instance_id, config)
            
            # Create shell script for Linux/Mac
            self._create_shell_script(instance_id, config)
            
            return True
        except Exception as e:
            print(f"Error preparing deployment for {instance_id}: {str(e)}")
            return False
    
    def _create_deployment_script(self, instance_id, config):
        """Create deployment script for the instance.
        
        Args:
            instance_id (str): Instance ID
            config (dict): Instance configuration
        """
        instance_dir = self.config_manager.get_instance_dir(instance_id)
        script_path = os.path.join(instance_dir, "run.py")
        
        with open(script_path, 'w') as f:
            f.write("""import os
import sys
import streamlit.web.cli as stcli

# Get the directory of this script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Add the instance directory to the Python path
sys.path.insert(0, dir_path)

# Run the Streamlit app
if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", "8501"))
    
    sys.argv = [
        "streamlit", "run",
        os.path.join(dir_path, "app", "main.py"),
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.serverAddress", "localhost",
        "--browser.serverPort", str(port)
    ]
    
    print(f"Starting Streamlit app on port {port}")
    print(f"Command: {' '.join(sys.argv)}")
    print(f"Working directory: {dir_path}")
    
    sys.exit(stcli.main())
""")
        
        # Make the script executable
        os.chmod(script_path, 0o755)
    
    def _create_windows_batch_file(self, instance_id, config):
        """Create a Windows batch file for easy startup.
        
        Args:
            instance_id (str): Instance ID
            config (dict): Instance configuration
        """
        instance_dir = self.config_manager.get_instance_dir(instance_id)
        batch_path = os.path.join(instance_dir, "run_app.bat")
        
        port = config.get("port", 8501)
        
        with open(batch_path, 'w') as f:
            f.write(f"@echo off\n")
            f.write(f"echo Starting RAG Application on port {port}...\n")
            f.write(f"set PORT={port}\n")
            f.write(f"python run.py\n")
            f.write(f"pause\n")
    
    def _create_shell_script(self, instance_id, config):
        """Create a shell script for Linux/Mac startup.
        
        Args:
            instance_id (str): Instance ID
            config (dict): Instance configuration
        """
        instance_dir = self.config_manager.get_instance_dir(instance_id)
        shell_path = os.path.join(instance_dir, "run_app.sh")
        
        port = config.get("port", 8501)
        
        with open(shell_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write(f"echo Starting RAG Application on port {port}...\n")
            f.write(f"export PORT={port}\n")
            f.write(f"python run.py\n")
        
        # Make the script executable
        os.chmod(shell_path, 0o755)
    
    def _create_requirements_file(self, instance_id):
        """Create requirements.txt file for the instance.
        
        Args:
            instance_id (str): Instance ID
        """
        instance_dir = self.config_manager.get_instance_dir(instance_id)
        requirements_path = os.path.join(instance_dir, "requirements.txt")
        
        with open(requirements_path, 'w') as f:
            f.write("""streamlit>=1.22.0
langchain>=0.0.270
langchain_community>=0.0.13
langchain_huggingface>=0.0.6
openai>=1.3.0
anthropic>=0.8.0
pinecone-client>=2.2.4
faiss-cpu>=1.7.4
chromadb>=0.4.10
sentence-transformers>=2.2.2
pdfplumber>=0.10.2
PyPDF2>=3.0.0
python-dotenv>=1.0.0
beautifulsoup4>=4.12.2
requests>=2.31.0
lxml>=4.9.3
numpy>=1.24.0
pandas>=2.0.0
psutil>=5.9.5
""")

    def create_docker_deployment(self, instance_id, config):
        """Create Docker deployment files for the instance.
        
        Args:
            instance_id (str): Instance ID
            config (dict): Instance configuration
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            instance_dir = self.config_manager.get_instance_dir(instance_id)
            
            # Create Dockerfile
            dockerfile_path = os.path.join(instance_dir, "Dockerfile")
            with open(dockerfile_path, 'w') as f:
                f.write("""FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app will run on
EXPOSE ${PORT:-8501}

# Command to run the application
CMD ["python", "run.py"]
""")
            
            # Create docker-compose.yml
            compose_path = os.path.join(instance_dir, "docker-compose.yml")
            with open(compose_path, 'w') as f:
                f.write(f"""version: '3'

services:
  rag-app:
    build: .
    ports:
      - "{config.get('port', 8501)}:{config.get('port', 8501)}"
    environment:
      - PORT={config.get('port', 8501)}
    volumes:
      - ./data:/app/data
      - ./pdfs:/app/pdfs
    restart: unless-stopped
""")
            
            return True
        except Exception as e:
            print(f"Error creating Docker deployment for {instance_id}: {str(e)}")
            return False
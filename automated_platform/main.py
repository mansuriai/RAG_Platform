# # main.py

# import os
# import sys
# import streamlit.web.cli as stcli

# def run():
#     """Run the Automated Platform application."""
#     # Get the directory of this script
#     dir_path = os.path.dirname(os.path.realpath(__file__))
    
#     # Add the directory to the Python path
#     sys.path.insert(0, dir_path)
    
#     # Run the Streamlit app
#     sys.argv = [
#         "streamlit", "run",
#         os.path.join(dir_path, "app", "platform_ui.py"),
#         "--server.port", "8501",
#         "--server.address", "localhost"
#     ]
    
#     sys.exit(stcli.main())

# if __name__ == "__main__":
#     run()

####################

# main.py

import os
import sys
import streamlit.web.cli as stcli

def run():
    """Run the Automated Platform application."""
    # Get the directory of this script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # Add the directory to the Python path
    sys.path.insert(0, dir_path)
    
    # Print debug information
    print(f"Starting Automated Platform from: {dir_path}")
    print(f"Python path: {sys.path}")
    
    # Path to the platform UI
    app_path = os.path.join(dir_path, "app", "platform_ui.py")
    
    # Check if the file exists
    if not os.path.exists(app_path):
        print(f"Error: Platform UI file not found at {app_path}")
        return
    
    print(f"Found platform UI at: {app_path}")
    
    # Run the Streamlit app
    sys.argv = [
        "streamlit", "run",
        app_path,
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ]
    
    print(f"Running command: {' '.join(sys.argv)}")
    sys.exit(stcli.main())

if __name__ == "__main__":
    run()
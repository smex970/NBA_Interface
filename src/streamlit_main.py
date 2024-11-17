from streamlit_interface import streamlit_interface

import subprocess

def execute_shell_command(command):
    try:
        result = subprocess.run(['/bin/bash', '-c', command], check=True, text=True, capture_output=True)
        print("Command executed successfully")
        print("Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing command")
        print("Return code:", e.returncode)
        print("Output:\n", e.output)
        print("Error message:\n", e.stderr)

# Activer l'environnement virtuel et installer les paquets nécessaires
command_activate_venv = "source venv/bin/activate"
command_install_requirements = "pip install -r ../requirements.txt"

execute_shell_command(command_activate_venv)
execute_shell_command(command_install_requirements)

ST = streamlit_interface()
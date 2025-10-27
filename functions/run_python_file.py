import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    command = ['python', abs_file_path] + args
    try:
        result = subprocess.run(command, 
        timeout=30, 
        capture_output=True, 
        cwd=abs_working_dir,  
        text=True,
        check=False)

        output_parts = []
        stdout_output = result.stdout
        if stdout_output:
            output_parts.append(f"STDOUT:\n{stdout_output}")

        stderr_output = result.stderr
        if stderr_output:
            output_parts.append(f"STDERR:\n{stderr_output}")

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        if not output_parts:
            return "No output produced"

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute python file with optional arguments in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to execute, relative to the working directory. If not provided, show error.",
            ),
        },
    ),
    )        
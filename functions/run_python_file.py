import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:  # pyright: ignore[reportReturnType]
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if valid_target_path == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file'
        if valid_target_path == True:
            programm = ["python", target_path]
            if args != None:
                programm.extend(args)
            result = subprocess.run(  # noqa: PLW1510
                programm,
                cwd= working_dir_abs,
                capture_output=True,
                text=True,
                timeout=30,
            )
            text_output = ""
            if result.returncode != 0:
                text_output += f"Process exited with code {result.returncode}\n"
            if result.stdout == "" and result.stderr == "":
                text_output += "No output produced\n"
            if result.stdout != "":
                text_output += f"STDOUT: {result.stdout}\n"
            if result.stderr != "":
                text_output += f"STDERR: {result.stderr}\n"
            return text_output

    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "run python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "required": {
                        "file_path"
                    "type": "string",
                    "description": "file path to run python file from, relative to the working directory",
                "array":{
                    "type": "string"
                },
            },
        },
    },
}
}
}

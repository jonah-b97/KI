import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:  # pyright: ignore[reportReturnType]
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if valid_target_path == False:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if valid_target_path == True:
            with open(target_path, "r") as f:
                content = f.read(MAX_CHARS)
                if f.read(MAX_CHARS):
                    content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return content
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Lists content of  files in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "required": {
                        "file_path"
                    "type": "string",
                    "description": "file path to list conten from, relative to the working directory",
                },
            },
        },
    },
}
}

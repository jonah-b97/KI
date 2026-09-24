import os


def write_file(working_directory: str, file_path: str, content: str) -> str:  # pyright: ignore[reportReturnType]
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if valid_target_path == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        if valid_target_path == True:
            os.makedirs((os.path.dirname(target_path)), exist_ok=True)
            with open(target_path, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write to file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "required": {
                        "file_path"
                    "type": "main.txt",
                    "description": "file_path path of file to write content to, relative to the working directory",
                "content":{
                    "required": {
                        "content"
                    "type": "string"
                }
                },
            },
        },
    },
}
}
}

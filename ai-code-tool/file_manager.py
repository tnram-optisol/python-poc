import os
import zipfile

def create_project_structure(code_structure, project_name):
    """Creates the project folder structure and saves code into respective files."""
    project_path = os.path.abspath(project_name)
    os.makedirs(project_path, exist_ok=True)

    for file_path, file_content in code_structure.items():
        # Create necessary directories
        full_path = os.path.join(project_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write the content to the file
        with open(full_path, "w") as file:
            file.write(file_content)

    return project_path

def zip_project(project_path):
    """Zips the entire project folder."""
    zip_path = f"{project_path}.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_path)
                zipf.write(file_path, arcname)
    return zip_path

import argparse
from ai_code_handler import generate_project_code
from file_manager import create_project_structure, zip_project


def main():
    parser = argparse.ArgumentParser(description="Generate a project structure with AI assistance.")
    parser.add_argument("--project_name", type=str, required=True, help="Name of your project")
    parser.add_argument("--frontend", type=str, default="React", help="Frontend framework (e.g., React, Vue)")
    parser.add_argument("--backend", type=str, default="Node.Js", help="Backend framework (e.g., Node.Js, Flask, Django)")
    parser.add_argument("--database", type=str, default="MongoDB", help="Database (e.g., MongoDB, SQLite, PostgreSQL)")

    args = parser.parse_args()

    print("Generating your project. Please wait...")

    try:
        # Step 1: Generate code using AI
        project_code = generate_project_code(args.project_name,args.frontend, args.backend, args.database)

        # Step 2: Create project structure
        project_path = create_project_structure(project_code, args.project_name)

        # Step 3: Zip the project
        zip_path = zip_project(project_path)

        print(f"Project generated successfully! Find your project at: {zip_path}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()

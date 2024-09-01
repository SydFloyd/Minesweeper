import os

# Specify the output file
output_file = "merged_code.txt"

# List of files to write first in the specified order
priority_files = [
    "readme.md",
    "main.py",
    "game_manager.py",
    "input_handler.py"
    "grid_manager.py",
    "event_manager.py",
    "ui_manager.py"
]

ignore_files = [
    "event_manager.py",
    # "high_score_manager.py",
    "persistence_manager.py"
]

def write_file_content(filename, file):
    with open(filename, "r") as f:
        file.write(f"\n# Content of {filename}\n\n")
        file.write(f.read())
        file.write("\n\n")

def main():
    # Get the current working directory
    cwd = os.getcwd()
    print(f"Current Working Directory: {cwd}")

    # Open the output file in write mode
    with open(output_file, "w") as file:
        file.write(f"# Current Working Directory: {cwd}\n")

        # Write contents of priority files
        for filename in priority_files:
            if os.path.exists(filename):
                write_file_content(filename, file)

        # Write contents of other python files that do not start with "_"
        for filename in sorted(os.listdir(cwd)):
            if filename.split('.') in ['py', 'md'] and not filename.startswith("_") and filename not in priority_files and filename not in ignore_files:
                write_file_content(filename, file)

        epilogue = f"Files excluded from printout: {ignore_files}"
        file.write(epilogue)

if __name__ == "__main__":
    main()

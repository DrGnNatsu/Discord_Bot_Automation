import subprocess # For running shell commands
import os # For path operations
import shutil # For file operations

def generate_grammar():
    ANTLR_JAR = "antlr4-4.9.2-complete.jar"
    GRAMMAR_FILE = "GuildFlow.g4"
    OUTPUT_DIR = "./compiled_files"
    
    print("Generating grammar...")
    
    # Check if the antlr jar file exists
    if not os.path.isfile(ANTLR_JAR):
        raise FileNotFoundError(f"ANTLR jar file not found: {ANTLR_JAR}")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    # Construct the ANTLR command
    command = [
        "java", "-jar", ANTLR_JAR,
        "-Dlanguage=Python3",
        "-visitor",
        "-no-listener",
        GRAMMAR_FILE,
        "-o", OUTPUT_DIR
    ]
    
    # Run the ANTLR command
    try:
        subprocess.run(command, check=True)
        print("Grammar generation completed successfully.")
        
        # Create an empty __init__.py file in the output directory to mark it as a package
        init_file = os.path.join(OUTPUT_DIR, "__init__.py")
        if not os.path.exists(init_file):
            open(init_file, 'a').close()
            
    except subprocess.CalledProcessError as e:
        print(f"Error during grammar generation: {e}")
        raise
    
if __name__ == "__main__":
    generate_grammar()
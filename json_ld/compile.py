import os
import sys

# --- Configuration ---

# 1. The directory where the input files are located. 
#    Based on your structure (mainfolder/dcat_prov), this should be 'dcat_prov'.
INPUT_DIRECTORY = 'rdip'

# 2. OPTIONAL: Filter files by extension (e.g., '.json' or '.jsonld').
#    Use None or an empty string '' to include ALL files in the directory.
FILE_EXTENSION_FILTER = '.json'

# 3. The name of the single output file where all content will be written.
OUTPUT_FILE_NAME = 'combined_ontology_data.txt'

# --- Script Logic ---

def combine_files(input_dir, output_file_name, extension_filter=None):
    """
    Scans a directory for files (optionally filtered by extension) and 
    writes all contents to a single output file, prefixed by a comment 
    with the filename.
    """
    print(f"Starting consolidation process in directory: '{input_dir}'")
    print(f"Output target: {output_file_name}")

    # Check if the input directory exists
    if not os.path.isdir(input_dir):
        print(f"ERROR: Input directory '{input_dir}' not found or is not a directory. Please check the 'INPUT_DIRECTORY' configuration.")
        return

    try:
        # 1. Discover all files in the directory
        all_entries = os.listdir(input_dir)
        
        # 2. Filter files based on two conditions: 
        #    a) it must be a file (not a sub-folder)
        #    b) it must match the extension filter (if one is provided)
        input_files = []
        for entry in all_entries:
            full_path = os.path.join(input_dir, entry)
            # Check if it's a file
            if os.path.isfile(full_path):
                # Check for extension filter
                if not extension_filter or entry.lower().endswith(extension_filter.lower()):
                    input_files.append(entry)

        
        if extension_filter and extension_filter.strip():
            print(f"Filtering by extension: {extension_filter}. Found {len(input_files)} file(s).")
        else:
            print(f"No extension filter applied. Found {len(input_files)} file(s).")

        # Sort the files alphabetically for consistent output order
        input_files.sort()
        
        if not input_files:
            print("WARNING: No files found matching the criteria. Nothing to combine.")
            return

        # 3. Open the output file for writing
        # Note: 'w' will overwrite the file if it exists.
        with open(output_file_name, 'w', encoding='utf-8') as outfile:
            
            # Write a header for the combined file
            outfile.write(f"############################################################\n")
            outfile.write(f"# Consolidated Data File generated from {len(input_files)} sources in '{input_dir}'.\n")
            outfile.write(f"############################################################\n\n")

            # 4. Iterate through each file and append its content
            for filename in input_files:
                print(f"-> Processing: {filename}")
                
                # Construct the full path
                full_path = os.path.join(input_dir, filename)

                try:
                    # Write the file name as a Python comment
                    outfile.write(f"\n\n# --- START FILE: {filename} (Path: {full_path}) ---\n")
                    
                    # Read the content of the current file
                    with open(full_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                    
                    # Write the content to the combined file
                    outfile.write(content.strip()) # strip() prevents extra blank lines if the input file ends with one
                    
                    outfile.write(f"\n# --- END FILE: {filename} ---\n")

                except Exception as e:
                    print(f"   ERROR reading/writing file '{filename}' from path '{full_path}': {e}", file=sys.stderr)
                    
        print(f"\n✅ Successfully combined {len(input_files)} files into '{output_file_name}'.")

    except Exception as e:
        print(f"\nAn unexpected error occurred during file combination: {e}", file=sys.stderr)

if __name__ == "__main__":
    combine_files(INPUT_DIRECTORY, OUTPUT_FILE_NAME, FILE_EXTENSION_FILTER)
import os

def rename_images(directory, prefix, dry_run=True):
    count = 1
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                ext = os.path.splitext(filename)[1]
                new_name = f"{prefix}_{count}{ext}"
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_name)

                if dry_run:
                    print(f"Dry run would rename: {old_path} to {new_path}")
                else:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} to {new_path}")
                
                count += 1

if __name__ == "__main__":
    # Get the directory of the current Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_dir, "input")

    rename_prefix = input("What do you want to call the files? (an underscore and number will be added)").strip()
    dry_input = input("Preview changes? (Y/N): ").strip().lower()
    dry_run = dry_input in ["yes", "y", ""]

    if os.path.isdir(input_folder):
        rename_images(input_folder, rename_prefix, dry_run)
        if dry_run:
            print("\n:D Dry run complete. No files were renamed.")
        else:
            print("\n:D Files renamed successfully.")
    else:
        print(f"D: 'input' folder not found at: {input_folder}")

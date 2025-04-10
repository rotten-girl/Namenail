import os
import shutil

def rename_and_move_images(base_name="image"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input")
    output_path = os.path.join(script_dir, "output")

    os.makedirs(output_path, exist_ok=True)

    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"} #remove gif support? add a toggle????

    counter = 1

    for file in os.listdir(input_path):
        file_path = os.path.join(input_path, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in image_extensions:
                new_filename = f"{base_name}_{counter:03d}{ext}"
                dest_path = os.path.join(output_path, new_filename)
                shutil.copy2(file_path, dest_path)
                print(f"renamed {file} -> {new_filename}")
                counter += 1

    print(f"\n:D Done!! Your images have been renamed and copied to the output folder!")

if __name__ == "__main__":
    print("Hihi!! Please read the readme if you have any issues!!")
    base = input("Enter the base name for the images (default: 'image'): ").strip() or "image"
    rename_and_move_images(base_name=base)

# bros how do I add functional error messages
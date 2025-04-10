import os
import shutil

def rename_and_move_images(base_name="image"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input")
    output_path = os.path.join(script_dir, "output")

    if not os.path.exists(input_path): #no input folder error
        print(f"D: ur input is borked, make sure it's at: {input_path}")
        return

    os.makedirs(output_path, exist_ok=True)

    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"} #gif support??? does it break gifs??

    counter = 0

    for file in os.listdir(input_path):
        file_path = os.path.join(input_path, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in image_extensions:
                counter += 1
                new_filename = f"{base_name}_{counter:03d}{ext}"
                dest_path = os.path.join(output_path, new_filename)
                shutil.copy2(file_path, dest_path)
                print(f"{file} renamed to {new_filename}") #rnename confirmation

    if counter == 0:
        print("D: u got no images to change!") #no imgs error
    else:
        print(f"\n:D ur files have been renamed <3") #success!!

if __name__ == "__main__":
    print("Hihi!! Please make sure you need the readme if you have any issues!! If the readme doesn't have the info u need, come terrorize me on github :3")
    base = input("What do u wanna rename ur files to? (default is 'image')").strip() or "image"
    rename_and_move_images(base_name=base)

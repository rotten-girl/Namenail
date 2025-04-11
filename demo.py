import os
import shutil
from PIL import Image
import sys

def rename_and_move_images(base_name="image", generate_thumbs=False, thumb_size=200, input_path="input", output_path="output", thumb_path=None):
    if not input_path or not output_path:
        print("one of ur paths is cooked.", file=sys.stderr)
        return

    if generate_thumbs and not thumb_path:
        thumb_path = os.path.join(output_path, "thumbnails")

    if not os.path.isdir(input_path):
        print(f"ur input folder is borked, make sure it's at: {input_path}", file=sys.stderr)
        return

    os.makedirs(output_path, exist_ok=True)
    if generate_thumbs:
        os.makedirs(thumb_path, exist_ok=True)

    valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    images = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) and os.path.splitext(f)[1].lower() in valid_exts]

    if not images:
        print("u got no images!!", file=sys.stderr)
        return

    for i, file in enumerate(images, 1):
        ext = os.path.splitext(file)[1].lower()
        new_filename = f"{base_name}_{i:03d}{ext}"
        src = os.path.join(input_path, file)
        dst = os.path.join(output_path, new_filename)
        shutil.copy2(src, dst)
        print(f"{file} renamed to {new_filename} :p")

        if generate_thumbs:
            try:
                with Image.open(src) as img:
                    img.thumbnail((thumb_size, thumb_size))
                    thumb_file = os.path.join(thumb_path, f"th_{new_filename}")
                    img.save(thumb_file)
                    print(f":D made th_{new_filename}")
            except Exception as e:
                print(f"D: couldn't make a thumb for {file}: {e}", file=sys.stderr)

    print(":D All files have been renamed!")

if __name__ == "__main__":
    print("Hihi! Please read the readme if u haven't yet!!")
    base_name = input("prefix for renamed imgs? (default: 'image'): ").strip() or "image"
    input_path = input("where's ur input folder? (default: './input'): ").strip() or "input"
    output_path = input("where's ur output folder?  './output'): ").strip() or "output"
    generate_thumbs = input("wanna make thumbnails?(y/n, default: n): ").strip().lower() == "y"

    thumb_size = 200
    thumb_path = None
    if generate_thumbs:
        thumb_size_input = input("how big do u want the thumbails to b? (default: 200): ").strip()
        if thumb_size_input.isdigit():
            size = int(thumb_size_input)
            if 100 <= size <= 300:
                thumb_size = size
        thumb_path = input("where's should I put ur thumbnails? (default: './output/thumbnails'): ").strip() or os.path.join(output_path, "thumbnails")

    rename_and_move_images(
        base_name=base_name,
        generate_thumbs=generate_thumbs,
        thumb_size=thumb_size,
        input_path=input_path,
        output_path=output_path,
        thumb_path=thumb_path
    )

import os
import shutil
from PIL import Image
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from jinja2 import Template

# the gui console thing
class ConsoleOutput:
    def __init__(self, widget, tag):
        self.widget = widget
        self.tag = tag

    def write(self, message):
        self.widget.config(state='normal')
        self.widget.insert(tk.END, message, self.tag)
        self.widget.see(tk.END)
        self.widget.config(state='disabled')

    def flush(self):
        pass

def rename_and_move_images(base_name="image", generate_thumbs=False, thumb_size=200, input_path="input", output_path="output", thumb_path=None):
    if not input_path or not output_path:
        print("one of ur paths is cooked.", file=sys.stderr)
        return

    if generate_thumbs and not thumb_path:
        thumb_path = os.path.join(output_path, "thumbnails")

    if not os.path.isdir(input_path):
        print(f"ur input folder doesn't exist so I made one here: {input_path}")
        os.makedirs(input_path, exist_ok=True)

    os.makedirs(output_path, exist_ok=True)
    if generate_thumbs:
        os.makedirs(thumb_path, exist_ok=True)

    valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    images = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) and os.path.splitext(f)[1].lower() in valid_exts]

    if not images:
        print("u got no images!!", file=sys.stderr)
        return

    renamed_images = []
    for i, file in enumerate(images, 1):
        ext = os.path.splitext(file)[1].lower()
        new_filename = f"{base_name}_{i:03d}{ext}"
        src = os.path.join(input_path, file)
        dst = os.path.join(output_path, new_filename)
        shutil.copy2(src, dst)
        print(f"{file} renamed to {new_filename} :p")
        renamed_images.append(new_filename)

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
    return renamed_images

def generate_html_gallery(image_dir, thumb_dir, images, output_file="gallery.html"):
    html_template = Template("""
        <div class="gallery">
          {% for img in images %}
            <div class="gallery-item">
              <img src="{{ thumb_dir }}/th_{{ img }}" data-full="{{ full_dir }}/{{ img }}" loading="lazy">
            </div>
          {% endfor %}
        </div>
    """)
    html = html_template.render(images=images, full_dir=os.path.basename(image_dir), thumb_dir=os.path.basename(thumb_dir))
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"ur html is here: {output_file}")

def launch_gui():
    def browse_input():
        path = filedialog.askdirectory()
        if path:
            input_entry.delete(0, tk.END)
            input_entry.insert(0, path)

    def browse_output():
        path = filedialog.askdirectory()
        if path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, path)

    def browse_thumbs():
        path = filedialog.askdirectory()
        if path:
            thumb_entry.delete(0, tk.END)
            thumb_entry.insert(0, path)

    def on_run_all():
        base = prefix_entry.get().strip() or "image"
        inp = input_entry.get().strip() or "input"
        out = output_entry.get().strip() or "output"
        gen_thumbs = thumb_var.get()
        size = 200
        thumb_out = thumb_entry.get().strip() or os.path.join(out, "thumbnails")

        if gen_thumbs:
            size_input = thumbsize_entry.get().strip()
            if size_input.isdigit():
                sz = int(size_input)
                if 100 <= sz <= 300:
                    size = sz
        else:
            thumb_out = None

        images = rename_and_move_images(
            base_name=base,
            generate_thumbs=gen_thumbs,
            thumb_size=size,
            input_path=inp,
            output_path=out,
            thumb_path=thumb_out
        )

        if images and gen_thumbs:
            generate_html_gallery(image_dir=out, thumb_dir=thumb_out, images=images)

    root = tk.Tk()
    root.title("CT Gallery")
    root.configure(padx=30, pady=30)

    tk.Label(root, text="Prefix for ur renamed images:").grid(row=0, column=0)
    prefix_entry = tk.Entry(root, width=40)
    prefix_entry.insert(0, "image")
    prefix_entry.grid(row=0, column=1, columnspan=2)

    tk.Label(root, text="input folder:").grid(row=1, column=0)
    input_entry = tk.Entry(root, width=40)
    input_entry.insert(0, "input")
    input_entry.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=browse_input).grid(row=1, column=2)

    tk.Label(root, text="output folder:").grid(row=2, column=0)
    output_entry = tk.Entry(root, width=40)
    output_entry.insert(0, "output")
    output_entry.grid(row=2, column=1)
    tk.Button(root, text="Browse", command=browse_output).grid(row=2, column=2)

    thumb_var = tk.BooleanVar()
    tk.Checkbutton(root, text="wanna make thumbnails?", variable=thumb_var).grid(row=3, column=0, columnspan=3)

    tk.Label(root, text="Thumbnail size (100-300):").grid(row=4, column=0)
    thumbsize_entry = tk.Entry(root, width=10)
    thumbsize_entry.insert(0, "200")
    thumbsize_entry.grid(row=4, column=1)

    tk.Label(root, text="thumbnail output:").grid(row=5, column=0)
    thumb_entry = tk.Entry(root, width=40)
    thumb_entry.insert(0, os.path.join("output", "thumbnails"))
    thumb_entry.grid(row=5, column=1)
    tk.Button(root, text="Browse", command=browse_thumbs).grid(row=5, column=2)

    tk.Button(root, text="do the things!", command=on_run_all).grid(row=6, column=0, columnspan=3, pady=10)

    console = tk.Text(root, height=10, width=80, state='disabled', bg="#0f0f0f")
    console.grid(row=7, column=0, columnspan=3)
    console.tag_config("INFO", foreground="#00ff00")
    console.tag_config("ERROR", foreground="#ff4d4d")
    sys.stdout = ConsoleOutput(console, "INFO")
    sys.stderr = ConsoleOutput(console, "ERROR")

    root.mainloop()

if __name__ == "__main__":
    launch_gui()

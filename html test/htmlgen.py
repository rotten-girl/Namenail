from pathlib import Path
from jinja2 import Template

# Image folder (relative or absolute)
image_folder = Path("images")
images = [img.name for img in image_folder.glob("*.jpg")]

# Just the gallery block
gallery_template = """
<div class="gallery">
  {% for img in images %}
    <img src="{{ folder }}/{{ img }}" alt="{{ img }}">
  {% endfor %}
</div>
"""

# Render HTML
template = Template(gallery_template)
html = template.render(images=images, folder=image_folder.name)

# Write to file or paste into your page
with open("gallery_snippet.html", "w") as f:
    f.write(html)

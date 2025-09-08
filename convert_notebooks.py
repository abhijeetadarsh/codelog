import nbformat
import re
from nbconvert import MarkdownExporter
from traitlets.config import Config
from pathlib import Path
import os

# --- Configuration ---
# Directory where your source .ipynb files are
NOTEBOOK_DIR = Path('content/notebooks')

# Directory where the final .md files will be saved for Pelican
# We save them directly in the main 'content' folder
OUTPUT_DIR = Path('content')

# Directory where images extracted from notebooks will be stored
IMAGE_DIR = OUTPUT_DIR / 'images'

# --- Main Script ---
def convert_notebook(notebook_path):
    """
    Converts a Jupyter notebook to a Pelican-compatible Markdown file.
    - Extracts metadata from the first raw cell.
    - Converts notebook content to Markdown.
    - Saves images from code outputs to a dedicated folder.
    - Combines metadata and content into a single .md file.
    """
    print(f"-> Processing: {notebook_path.name}")

    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)

    # 1. Extract Metadata from the first raw cell
    metadata = {}
    first_cell = notebook_content.cells[0]
    if first_cell.cell_type != 'raw':
        print(f"   [!] Warning: First cell in {notebook_path.name} is not a 'Raw NBConvert' cell. Skipping.")
        return
    
    lines = first_cell.source.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()

    if 'Title' not in metadata or 'Date' not in metadata:
        print(f"   [!] ERROR: Missing 'Title' or 'Date' in {notebook_path.name}. Aborting conversion for this file.")
        return

    # Create a URL-friendly 'slug' from the title if not provided
    if 'Slug' not in metadata:
        slug = re.sub(r'[^\w-]+', '-', metadata['Title'].lower()).strip('-')
        metadata['Slug'] = slug
    else:
        slug = metadata['Slug']

    # 2. Configure the Markdown Exporter to handle images
    # This tells nbconvert to save images as separate files
    c = Config()
    # The path where images will be saved, relative to the OUTPUT_DIR
    c.ExtractOutputPreprocessor.output_filename_template = f"images/{slug}/{{unique_key}}_{{cell_index}}_{{index}}{{extension}}"
    
    exporter = MarkdownExporter(config=c)
    
    # Exclude the first raw cell from the final output
    notebook_content.cells.pop(0)

    # 3. Convert the notebook to Markdown
    (body, resources) = exporter.from_notebook_node(notebook_content)

    # 4. Write the extracted images to files
    # The 'resources' dictionary contains the images and their filenames
    if 'outputs' in resources:
        # Ensure the target image directory exists
        image_path_for_post = IMAGE_DIR / slug
        image_path_for_post.mkdir(parents=True, exist_ok=True)
        
        for filename, data in resources['outputs'].items():
            output_path = OUTPUT_DIR / filename
            with open(output_path, 'wb') as f:
                f.write(data)
            print(f"   [OK] Image saved to {output_path}")

    # 5. Create the final Markdown file with metadata header
    markdown_header = "\n".join([f"{key}: {value}" for key, value in metadata.items()])
    final_markdown_content = f"{markdown_header}\n\n{body}"
    
    output_md_path = OUTPUT_DIR / f"{slug}.md"
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(final_markdown_content)
        
    print(f"   [OK] Markdown file saved to {output_md_path}\n")


if __name__ == '__main__':
    # Ensure the main output and image directories exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGE_DIR.mkdir(exist_ok=True)

    # Clean up old generated markdown files to avoid orphans
    for md_file in OUTPUT_DIR.glob('*.md'):
        md_file.unlink()
    print("Cleaned old .md files from content/ directory.\n")

    # Find all .ipynb files and convert them
    for notebook_path in NOTEBOOK_DIR.glob('*.ipynb'):
        convert_notebook(notebook_path)

    print("✅ Notebook conversion to Markdown complete.")
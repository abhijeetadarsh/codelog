import nbformat
import re
import base64
import uuid
import shutil
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor
from traitlets.config import Config
from pathlib import Path
import os

# --- Configuration ---
NOTEBOOK_DIR = Path('notebooks')
OUTPUT_DIR = Path('content')
IMAGE_DIR = OUTPUT_DIR / 'nbimages'

# --- Preprocessor for RELATIVE IMAGE PATHS in Markdown ---

class PelicanRelativePathPreprocessor(Preprocessor):
    """
    Processes Markdown cells to find relative image paths,
    copies the image to the output directory, and rewrites the path.
    """
    def preprocess_cell(self, cell, resources, cell_index):
        if cell.cell_type != 'markdown':
            return cell, resources

        # Regex to find all markdown image links
        # ![alt text](path/to/image.png)
        regex = r"!\[(.*?)\]\((?!https?://|{|/)(.*?)\)"
        
        # The notebook's path is needed to resolve relative image paths
        notebook_path = Path(resources['metadata']['path']) / resources['metadata']['name']
        notebook_dir = notebook_path.parent
        slug = resources.get('slug', 'default-slug')
        
        # This function will be called for each match
        def rewrite_path(match):
            alt_text = match.group(1)
            relative_path = match.group(2)
            
            # Construct the source and destination paths
            src_path = (notebook_dir / relative_path).resolve()
            
            if not src_path.is_file():
                print(f"   [!] Image not found at {src_path}. Skipping.")
                return match.group(0) # Return the original string if file not found

            # Create a unique name for the destination file to avoid conflicts
            dest_filename = f"{uuid.uuid4().hex}{src_path.suffix}"
            dest_dir = IMAGE_DIR / slug
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / dest_filename
            
            # Copy the file
            shutil.copy(src_path, dest_path)
            print(f"   [OK] Copied relative image: {src_path.name} -> {dest_path}")
            
            # Rewrite the URL to the Pelican-friendly format
            pelican_url = f"{{static}}/nbimages/{slug}/{dest_filename}"
            
            return f"![{alt_text}]({pelican_url})"

        # Use re.sub with our function to perform the replacement
        cell.source = re.sub(regex, rewrite_path, cell.source)
        
        return cell, resources

# --- Preprocessor for EMBEDDED ATTACHMENTS in Markdown ---

class PelicanMarkdownAttachmentsPreprocessor(Preprocessor):
    """
    Extracts attached images from markdown cells, saves them, and updates the link.
    """
    def preprocess_cell(self, cell, resources, cell_index):
        if cell.cell_type != 'markdown' or not hasattr(cell, 'attachments'):
            return cell, resources

        slug = resources.get('slug', 'default-slug')
        post_image_path = IMAGE_DIR / slug
        post_image_path.mkdir(parents=True, exist_ok=True)

        for filename, attachment in cell.attachments.items():
            for mimetype, b64_data in attachment.items():
                image_data = base64.b64decode(b64_data)
                ext = mimetype.split('/')[-1]
                unique_filename = f"{uuid.uuid4().hex}.{ext}"
                output_filepath = post_image_path / unique_filename
                
                with open(output_filepath, 'wb') as f:
                    f.write(image_data)
                print(f"   [OK] Markdown attachment saved to {output_filepath}")

                pelican_url = f"{{static}}/images/{slug}/{unique_filename}"
                cell.source = cell.source.replace(f"attachment:{filename}", pelican_url)

        return cell, resources

# --- Main Script ---
def convert_notebook(notebook_path):
    print(f"-> Processing: {notebook_path.name}")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)

    # 1. Extract Metadata
    metadata = {}
    if not notebook_content.cells or notebook_content.cells[0].cell_type != 'raw':
        print(f"   [!] Warning: First cell in {notebook_path.name} is not a 'Raw NBConvert' cell. Skipping.")
        return
    
    first_cell = notebook_content.cells.pop(0)
    lines = first_cell.source.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()

    if 'Title' not in metadata or 'Date' not in metadata:
        print(f"   [!] ERROR: Missing 'Title' or 'Date' in {notebook_path.name}. Aborting.")
        return

    slug = metadata.get('Slug', re.sub(r'[^\w-]+', '-', metadata['Title'].lower()).strip('-'))
    metadata['Slug'] = slug

    # 2. Configure the Markdown Exporter with all preprocessors
    c = Config()
    
    # A. For CODE CELL outputs (e.g., plots)
    c.ExtractOutputPreprocessor.output_filename_template = f"images/{slug}/{{unique_key}}_{{cell_index}}_{{index}}{{extension}}"
    
    # B. Add our CUSTOM preprocessors for MARKDOWN cells
    c.MarkdownExporter.preprocessors = [
        PelicanRelativePathPreprocessor,
        PelicanMarkdownAttachmentsPreprocessor
    ]
    
    exporter = MarkdownExporter(config=c)
    
    # 3. Convert the notebook
    # Pass metadata so preprocessors can access the notebook's original path and slug
    resources = {
        'slug': slug,
        'metadata': {
            'path': str(notebook_path.parent),
            'name': notebook_path.name
        }
    }
    (body, resources) = exporter.from_notebook_node(notebook_content, resources)

    # 4. Write images from CODE outputs
    if 'outputs' in resources:
        for filename, data in resources['outputs'].items():
            output_path = OUTPUT_DIR / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(data)
            print(f"   [OK] Code output image saved to {output_path}")

    # 5. Create the final Markdown file
    markdown_header = "\n".join([f"{key}: {value}" for key, value in metadata.items()])
    final_markdown_content = f"{markdown_header}\n\n{body}"
    
    output_md_path = OUTPUT_DIR / f"{slug}.md"
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(final_markdown_content)
        
    print(f"   [OK] Markdown file saved to {output_md_path}\n")


if __name__ == '__main__':
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Clean up old generated content to avoid orphans
    for md_file in OUTPUT_DIR.glob('*.md'):
        md_file.unlink()
    print("Cleaned old .md files from content/ directory.")

    if IMAGE_DIR.exists():
        shutil.rmtree(IMAGE_DIR)
        print("Cleaned old image directory.\n")
    IMAGE_DIR.mkdir(exist_ok=True)

    for notebook_path in NOTEBOOK_DIR.glob('*.ipynb'):
        convert_notebook(notebook_path)

    print("✅ Notebook conversion to Markdown complete.")
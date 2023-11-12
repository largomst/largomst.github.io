import os
import shutil
from markdown import markdown
from jinja2 import Environment, FileSystemLoader

CONTENT_DIR = 'Content'
PUBLIC_DIR = 'docs'
ASSETS_DIR = 'Assets'
INDEX_TEMPLATE = 'index_template.html'
PAGE_TEMPLATE = 'page_template.html'

# Step 1: Copy assets
shutil.copytree(ASSETS_DIR, os.path.join(PUBLIC_DIR, ASSETS_DIR), dirs_exist_ok=True)

# Step 2: Process markdown files
markdown_files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]

env = Environment(loader=FileSystemLoader('.'))
page_template = env.get_template(PAGE_TEMPLATE)

html_files = []
for md_file in markdown_files:
    # Convert markdown to html
    with open(os.path.join(CONTENT_DIR, md_file), 'r', encoding='utf-8') as file:
        md_content = file.read()
    html_content = markdown(md_content)
    # Create new html file
    html_file = md_file[:-3] + '.html'
    html_files.append(html_file)
    with open(os.path.join(PUBLIC_DIR, html_file), 'w', encoding='utf-8') as file:
        file.write(page_template.render(content=html_content, index_url='index.html'))

# Step 3: Create index file
index_template = env.get_template(INDEX_TEMPLATE)
with open(os.path.join(PUBLIC_DIR, 'index.html'), 'w', encoding='utf-8') as file:
    file.write(index_template.render(pages=html_files))
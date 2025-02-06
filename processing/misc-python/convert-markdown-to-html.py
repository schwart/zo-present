from markdown_it import MarkdownIt
from pathlib import Path
import fnmatch
import os

md = MarkdownIt('commonmark', {'breaks':True,'html':True})

def render_markdown_to_html(input_path, output_path):
    with open(input_path, "r") as f:
        text = f.read()

    html_body = md.render(text)

    html_head = """
    <!DOCTYPE html>
    <html>

    <head>
        <meta charset="UTF-8">
        <title>Page Title</title>
    </head>

    <body style="font-family: sans-serif">
    """

    html_footer = """
    </body>

    </html>
    """

    full_html = html_head + html_body + html_footer

    Path(output_path).write_text(full_html)

# returns a list of (input_path, output_path) tuples
def get_all_markdown_files_recursive(input_path):
    paths = []
    for dirpath, _, filenames in os.walk(input_path):
        for filename in fnmatch.filter(filenames, "*.human.md"):
            input_path = os.path.join(dirpath, filename)
            output_path = os.path.join(dirpath, filename.replace(".md", ".html"))
            paths.append((input_path, output_path))
    return paths

input_path = "/Users/conallmcginty/Desktop/zoe-present/outputs/"

# now we have all the (dirpath, full_path)'s set up
for input_path, output_path in get_all_markdown_files_recursive(input_path):
    print(f"Rendering {input_path}")
    render_markdown_to_html(input_path, output_path)

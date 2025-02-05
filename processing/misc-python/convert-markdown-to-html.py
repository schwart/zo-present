from markdown_it import MarkdownIt
from pathlib import Path

md = MarkdownIt('commonmark', {'breaks':True,'html':True})


input_path = "/Users/conallmcginty/Desktop/zoe-present/outputs/entire_chat.md"

with open(input_path, "r") as f:
    text = f.read()

tokens = md.parse(text)
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

Path("index.html").write_text(full_html)

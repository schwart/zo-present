import pyperclip
import argparse
import os

parser = argparse.ArgumentParser(description="Template an llm prompt.")
parser.add_argument("--input-file", "-i", required=True, help="Path to the input markdown file")

args = parser.parse_args()
input_file = args.input_file
if not input_file.endswith(".robot.md"):
    raise Exception(f"{input_file} is not a robot Markdown file")

print(f"Processing file: {args.input_file}")

# load the input file
with open(input_file, "r") as f:
    input_text = f.read()

# load the llm prompt template from this directory
this_directory = os.path.dirname(__file__)
llm_template = os.path.join(this_directory, "llmPrompt.txt")
with open(llm_template, "r") as f:
    template = f.read()

full_prompt = template.replace("[[MARKDOWN_TEXT_HERE]]", input_text)

# copy it to clipboard
pyperclip.copy(full_prompt)

print("Templated prompt is saved to clipboard")

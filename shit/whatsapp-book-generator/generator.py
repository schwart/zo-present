from jinja2 import Template
import emoji
import re
from datetime import datetime, timedelta

def emoji_to_latex(text):
    def replace_emoji(match):
        emoji_char = match.group(0)
        if emoji.is_emoji(emoji_char):
            emoji_name = emoji.demojize(emoji_char).strip(':').replace('_', '-')
            return f'\\emoji{{{emoji_name}}}'
        return emoji_char
    
    return re.sub(r'[^\u0000-\u007F]', replace_emoji, text)

# Generate some sample messages with dates and times
start_date = datetime(2024, 1, 1, 9, 0)  # Start from Jan 1, 2024, 9:00 AM
messages = []
current_date = start_date

for i in range(20):  # Generate 20 messages
    message_type = "text" if i % 3 != 0 else "image"
    direction = "left" if i % 2 == 0 else "right"
    
    message = {
        "type": message_type,
        "direction": direction,
        "content": f"Message {i+1}" if message_type == "text" else f"image{(i//3)%2 + 1}.jpg",
        "date": current_date.strftime("%B %d, %Y"),
        "time": current_date.strftime("%H:%M"),
        "new_date": i == 0 or current_date.date() != messages[-1]["date"].date() if messages else False
    }
    
    if message_type == "text":
        message["content"] = emoji_to_latex(message["content"] + " 😊👍")
    
    messages.append(message)
    
    # Increment time by a random amount between 5 minutes and 2 hours
    current_date += timedelta(minutes=5 + (i * 13) % 115)

# Load the template
with open('latex.template.tex', 'r') as file:
    template_string = file.read()

# Create a Jinja2 template object
template = Template(template_string)

# Render the template with your messages
rendered_latex = template.render(messages=messages)

# Save the rendered LaTeX to a file
with open('output.tex', 'w') as file:
    file.write(rendered_latex)

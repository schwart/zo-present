import os
import shutil

content_dir_name = "content"

def link_attachments_to_output_directory(rows, output_dir):
    content_dir = os.path.join(output_dir, content_dir_name)
    if os.path.exists(content_dir):
        shutil.rmtree(content_dir, ignore_errors=True)
    os.mkdir(content_dir)
    attachments = list(rows[rows["type"] == "ATTACHMENT"]["message"])
    for input_path in attachments:
        file_name = os.path.basename(input_path)
        output_path = os.path.join(content_dir, file_name)
        os.symlink(input_path, output_path)

def image_attachment(message):
    filename = os.path.basename(message)
    filepath = os.path.join(content_dir_name, filename)
    return f'<img src="{filepath}" width="300">'

def audio_attachment(message):
    filename = os.path.basename(message)
    filepath = os.path.join(content_dir_name, filename)
    return f'<audio controls width="300" src="{filepath}"></audio>'

def video_attachment(message):
    filename = os.path.basename(message)
    filepath = os.path.join(content_dir_name, filename)
    return f'<video controls width="300" src="{filepath}"></video>'

def is_image(attachment_type):
    return attachment_type in ["PHOTO", "GIF", "STICKER", "TIFF_PHOTO"]

def is_audio(attachment_type):
    return attachment_type == "AUDIO"

def is_video(attachment_type):
    return attachment_type == "VIDEO"

def message_for_attachment_type(message, attachment_type):
    # valid attachment types
    # PHOTO
    # GIF
    # STICKER
    # TIFF_PHOTO
    # VIDEO
    # AUDIO
    if is_image(attachment_type):
        return image_attachment(message)
    if is_audio(attachment_type):
        return audio_attachment(message)
    if is_video(attachment_type):
        return video_attachment(message)

    return message

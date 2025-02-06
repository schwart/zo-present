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

def image_attachment(row):
    message = row["message"]
    filename = os.path.basename(message)
    filepath = os.path.join(content_dir_name, filename)
    # include a description of the image if there is one
    image_element = '<img src="{filepath}" width="300">'
    if "image_description" in row and str(row["image_description"]) != "nan":
        description = row["image_description"]
        image_description = f"> Image Description: {description}"
        return f'{image_element}\n\n{image_description}'
    return image_element

def audio_attachment(row):
    message = row["message"]
    filename = os.path.basename(message)
    filepath = os.path.join(content_dir_name, filename)
    audio_element = f'<audio controls width="300" src="{filepath}"></audio>'
    if "audio_transcript" in row and str(row["audio_transcript"]) != "nan":
        description = row["audio_transcript"]
        audio_transcript = f"> Audio Transcription: {description}"
        return f'{audio_element}\n\n{audio_transcript}'
    return audio_element

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

def message_for_attachment_type(row):
    # valid attachment types
    # PHOTO
    # GIF
    # STICKER
    # TIFF_PHOTO
    # VIDEO
    # AUDIO
    message = row["message"]
    attachment_type = row["attachment_type"]
    if is_image(attachment_type):
        return image_attachment(row)
    if is_audio(attachment_type):
        return audio_attachment(row)
    if is_video(attachment_type):
        return video_attachment(message)

    return message

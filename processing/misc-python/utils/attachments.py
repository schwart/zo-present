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

def get_image_description(row):
    if "image_description" in row and str(row["image_description"]) != "nan":
        description = row["image_description"]
        return f"> Image Description: {description}"
    else:
        return ""

def image_attachment(row, human):
    message = row["message"]
    filename = os.path.basename(message)
    filepath = os.path.join(content_dir_name, filename)

    # if they're a human, we want to include the image element and the description
    # if they're a robot, they just need the description
    image_description = get_image_description(row)
    image_element = f'<img src="{filepath}" width="300">'

    if human:
        return f'{image_description}\n\n{image_element}'
    else:
        return image_description

def get_audio_transcript(row):
    if "audio_transcript" in row and str(row["audio_transcript"]) != "nan":
        description = row["audio_transcript"]
        return f"> Audio Transcription: {description}"
    else:
        return ""


def audio_attachment(row, human):
    message = row["message"]
    filename = os.path.basename(message)
    filepath = os.path.join(content_dir_name, filename)

    # if they're a human, we want to include the audio element and the transcript
    # if they're a robot, they just need the transcript
    audio_transcript = get_audio_transcript(row)
    audio_element = f'<audio controls width="300" src="{filepath}"></audio>'

    if human:
        return f'{audio_transcript}\n\n{audio_element}'
    else:
        return audio_transcript

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

def message_for_attachment_type(row, human):
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
        return image_attachment(row, human)
    if is_audio(attachment_type):
        return audio_attachment(row, human)
    if is_video(attachment_type):
        return video_attachment(message)

    return message

def get_all_audio_attachments(df):
    # get all rows that are audio attachments
    # that don't already have a transcript written to them
    attachment_mask = df["type"] == "ATTACHMENT"
    audio_attachment_mask = df["attachment_type"] == "AUDIO"

    try:
        transcript_mask = df["audio_transcript"].isnull() == True
        return df.loc[attachment_mask & audio_attachment_mask & transcript_mask]
    # this means there's no "audio_transcript" column yet
    # in that case, just return all the audio attachments
    except KeyError:
        return df.loc[attachment_mask & audio_attachment_mask]

def get_all_image_attachments(df):
    # get all rows that are image attachments
    # that don't already have a transcript written to them
    attachment_mask = df["type"] == "ATTACHMENT"
    #TODO: need to update this to handle more image types
    image_attachment_mask = df["attachment_type"] == "PHOTO"

    try:
        transcript_mask = df["image_description"].isnull() == True
        return df.loc[attachment_mask & image_attachment_mask & transcript_mask]
    # this means there's no "image_transcript" column yet
    # in that case, just return all the image attachments
    except KeyError:
        return df.loc[attachment_mask & image_attachment_mask]


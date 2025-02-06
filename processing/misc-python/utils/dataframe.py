import pandas as pd
import os

def get_attachment_absolute_path(row):
    prefix = "/Users/conallmcginty/Desktop/zoe-present/chat-data/"
    out_path = os.path.join(prefix, row["message"])
    if os.path.exists(out_path) == False:
        print(row)
        raise Exception(f"{out_path} does not exist")
    return out_path

def load_dataframe(file_path):
    # will have the following columns
    # timestamp (initially a string type)
    # author
    # message (if type column is "ATTACHMENT", this will be the path to an image)
    # type (either MESSAGE or ATTACHMENT)
    # transcript (the whisper transcript of the audio file)
    df = pd.read_csv(file_path, header=0)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def initialise_dataframe(df):
    # set file paths so they're absolute
    is_attachment_mask = df["type"] == "ATTACHMENT"
    df.loc[is_attachment_mask, "message"] = df.loc[is_attachment_mask].apply(get_attachment_absolute_path, axis=1)

    # need to work out the type of attachments based on their file name
    # photo
    df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "PHOTO" in row["message"], axis=1), "attachment_type"] = "PHOTO"
    # audio
    df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "AUDIO" in row["message"], axis=1), "attachment_type"] = "AUDIO"
    # sticker
    df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "STICKER" in row["message"], axis=1), "attachment_type"] = "STICKER"
    # video
    df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "VIDEO" in row["message"], axis=1), "attachment_type"] = "VIDEO"
    # gif
    df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "GIF" in row["message"], axis=1), "attachment_type"] = "GIF"
    # tiff
    df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and ".tiff" in row["message"], axis=1), "attachment_type"] = "TIFF_PHOTO"
    return df

def sanity_checks(df):
    # check that we don't have any attachments with no attachment type assigned
    all_attachments_with_no_type = df[(df["attachment_type"].isnull()) & (df["type"] == "ATTACHMENT")]["message"]
    len_all_attachments_with_no_type = len(all_attachments_with_no_type)
    print(f"Length of all attachments with no type: {len_all_attachments_with_no_type}")
    if len_all_attachments_with_no_type > 0:
        raise Exception("There are some attachments with no type!")

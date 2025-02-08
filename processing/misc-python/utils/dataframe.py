import pandas as pd
import sqlite3
import os

def get_attachment_absolute_path(row):
    prefix = "/Users/conallmcginty/Desktop/zoe-present/chat-data/"
    out_path = os.path.join(prefix, row["message"])
    if os.path.exists(out_path) == False:
        print(row)
        raise Exception(f"{out_path} does not exist")
    return out_path

def symlink_attachment_path_to_folder(input_path, output_dir):
    filename = os.path.basename(input_path)
    output_path = os.path.join(output_dir, filename)
    os.symlink(input_path, output_path)

def from_csv(input_path):
    # will have the following columns
    # timestamp (initially a string type)
    # author
    # message (if type column is "ATTACHMENT", this will be the path to an image)
    # type (either MESSAGE or ATTACHMENT)
    # transcript (the whisper transcript of the audio file)
    df = pd.read_csv(input_path, header=0)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def to_csv(df, output_path):
    df.to_csv(output_path, index = False, date_format='%Y-%m-%dT%H:%M:%SZ')

def to_sqlite(df, output_path):
    with sqlite3.connect(output_path) as connection:
        df.to_sql("dataframe", connection, if_exists="replace")

def from_sqlite(input_path):
    with sqlite3.connect(input_path) as connection:
        df = pd.read_sql_query("SELECT * from dataframe", connection, index_col="index")
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

def get_all_attachments_with_no_attachment_type(df):
    # check that we don't have any attachments with no attachment type assigned
    attachments = df["type"] == "ATTACHMENT"
    attachment_isnt_null = df["attachment_type"].isnull()
    return df[attachments & attachment_isnt_null]

def ask_to_remove_attachments_with_no_type(df, input_path):
    attachments_with_no_type = get_all_attachments_with_no_attachment_type(df)
    attachment_paths = attachments_with_no_type["message"]
    len_all_attachments_with_no_type = len(attachment_paths)
    print(f"Number of attachments with no type: {len_all_attachments_with_no_type}")
    if len_all_attachments_with_no_type > 0:
        for attachment in attachment_paths:
            print(attachment)
        response = input("Above are the attachments that we're going to skip, is that fine?")
        if response.lower() == 'y':
            # remove them from the data frame
            # save the csv back
            dropped = df.drop(attachments_with_no_type.index)
            to_csv(dropped, input_path)
            return dropped
        raise Exception("There are some attachments with no type!")
    return df

def remove_any_blank_author_rows(df, input_path):
    no_author = df.loc[df["author"].isnull()]
    print(f"Number of blank author rows: {len(no_author.index)}")
    dropped = df.drop(no_author.index)
    to_csv(dropped, input_path)
    return dropped

def sanity_checks(df, input_path):
    df = ask_to_remove_attachments_with_no_type(df, input_path)
    df = remove_any_blank_author_rows(df, input_path)
    return df

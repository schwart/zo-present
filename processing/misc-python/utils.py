import pandas as pd
import os
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

def load_dataframe(file_path):
    # will have the following columns
    # timestamp (initially a string type)
    # author
    # message (if type column is "ATTACHMENT", this will be the path to an image)
    # type (either MESSAGE or ATTACHMENT)
    df = pd.read_csv(file_path, header=0, names=["timestamp", "author", "message", "type"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

files_we_cant_find = []

def get_attachment_absolute_path(row):
    prefix = "/Users/conallmcginty/Desktop/zoe-present/chat-data/"
    out_path = os.path.join(prefix, row["message"])
    if os.path.exists(out_path) == False:
        print(row)
        files_we_cant_find.append(out_path)
        # raise Exception(f"{out_path} does not exist")
    return out_path

def get_rows_for_month(df, start_year, start_month):
    '''
        Example: get_rows_for_month(df, 2023, 9)

        Will get all rows from 2023-09-01 up to 2023-10-01
    '''
    start_date = date(start_year, start_month, 1)
    end_date = start_date + relativedelta(months=1)

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    mask = (df["timestamp"] >= start_date) & (df["timestamp"] < end_date)
    results = df.loc[mask]
    return results

def get_rows_for_day(df, start_year, start_month, start_day):
    start_date = date(start_year, start_month, start_day)
    end_date = start_date + relativedelta(days=1)

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    mask = (df["timestamp"] >= start_date) & (df["timestamp"] < end_date)
    results = df.loc[mask]
    return results

def createMarkdownTextForMessageType(message, message_type, attachment_type):
    return message

def createMarkdownEntryForRow(row):
    header = "# Text"
    author = f"> Author: {row['author']}"
    date_time = f"> Date/time: {row['timestamp']}"
    message_type = f"Type: {row['type']}"
    message = createMarkdownTextForMessageType(row['message'], row['type'], row['attachment_type'])
    # build the text of the message
    return (
        f"{header}\n"
        f"{author}\n"
        f"{date_time}\n"
        f"{message_type}\n\n"
        f"{message}\n"
    )

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

    # check that there's no files that we can't find
    len_files_we_cant_find = len(files_we_cant_find)
    print(f"Length of all files we can't find: {len_files_we_cant_find}")
    if len_files_we_cant_find > 0:
        for f in files_we_cant_find:
            print(f)
        raise Exception("There are some attachments that we can't find!")


input_file = "/Users/conallmcginty/Desktop/zoe-present/outputs/chat.csv"
output_file = "/Users/conallmcginty/Desktop/zoe-present/outputs/entire_chat.md"

df = load_dataframe(input_file)
df = initialise_dataframe(df)
sanity_checks(df)

markdown_elements = []
for index, row in df.iterrows():
    markdown_elements.append(createMarkdownEntryForRow(row))

with open(output_file, "w") as f:
    for el in markdown_elements:
        f.write(el)

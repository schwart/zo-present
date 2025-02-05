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

file_path = "/Users/conallmcginty/Desktop/zoe-present/outputs/chat.csv"
df = load_dataframe(file_path)
# fix file paths so they're absolute
is_attachment_mask = df["type"] == "ATTACHMENT"
df.loc[is_attachment_mask, "message"] = df.loc[is_attachment_mask].apply(get_attachment_absolute_path, axis=1)

# need to work out the type of attachments based on their file name
df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "PHOTO" in row["message"], axis=1), "attachment_type"] = "PHOTO"
df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "AUDIO" in row["message"], axis=1), "attachment_type"] = "AUDIO"
df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "STICKER" in row["message"], axis=1), "attachment_type"] = "STICKER"


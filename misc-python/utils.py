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

def get_attachment_absolute_path(row):
    prefix = "/Users/conallmcginty/Desktop/zoe-present"
    out_path = os.path.join(prefix, row["message"])
    os.path.exists(out_path)
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

file_path = "/Users/conallmcginty/Desktop/zoe-present/node-whatapp-generator/whatsapp-chat.csv"
df = load_dataframe(file_path)
# fix file paths so they're absolute
is_attachment_mask = df["type"] == "ATTACHMENT"
df.loc[is_attachment_mask, "message"] = df.loc[is_attachment_mask].apply(get_attachment_absolute_path, axis=1)

# need to work out the type of attachments based on their file name
df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "PHOTO" in row["message"], axis=1), "attachment_type"] = "PHOTO"
df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "AUDIO" in row["message"], axis=1), "attachment_type"] = "AUDIO"
df.loc[df.apply(lambda row: row["type"] == "ATTACHMENT" and "STICKER" in row["message"], axis=1), "attachment_type"] = "STICKER"


start_year = 2023
end_year = 2023

file = open("manuscript.txt", "a")

for year in range(start_year, end_year + 1):
    for month in range(9, 10):
        rows = get_rows_for_month(df, year, month)
        if not rows.empty:
            # here we're iterating through the months of a year
            # we need to iterate through the days of that month
            start_of_month = 1
            end_of_month = calendar.monthrange(year, month)[1] + 1
            print(f"{year}-{month}")
            for day in range(start_of_month, end_of_month):
                day_rows = get_rows_for_day(rows, year, month, day)
                if not day_rows.empty:
                    # here's all the rows for a single day!!!
                    print(f"{day} - {len(day_rows)}", end = ", ")
                    # write the date
                    date_string = f"----- {day}/{month}/{year} -----\n"
                    file.write(date_string)
                    # we need to keep track of the author of the messages
                    # there will be "runs"
                    previous_author = None
                    previous_time = day_rows.iloc[0]["timestamp"] - timedelta(days = 1)
                    for index, row in day_rows.iterrows():
                        # check if we need to place an author tag
                        current_author = row["author"]
                        if current_author != previous_author:
                            # write the author row
                            file.write(f"{current_author}\n")
                            # set the current_time to equal the time in this row
                            # force the time to be printed by pretending that the previous time was yonks ago
                            previous_time = previous_time - timedelta(days = 1)
                        # write the time of the message
                        current_time = row["timestamp"]
                        # if the last time we wrote a timestamp was more than 10 minutes ago
                        if current_time - timedelta(minutes = 10) > previous_time:
                            # we've written a message over ten minutes ago
                            # write the time
                            time_string = current_time.strftime("%H:%M")
                            file.write(f"{time_string}\n")
                            previous_time = current_time

                        message = row["message"]
                        if row["type"] == "ATTACHMENT":
                            message = f"%[{message}]%"
                        file.write(f"{message}\n")
                        file.write(f"-------------------------------------------\n")

                        previous_author = current_author

            print()

# i think the text parsing is done now
# from here we can build up the 

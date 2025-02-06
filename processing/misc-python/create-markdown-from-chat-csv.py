import os
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from utils import attachments
from utils import dataframe


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
    if message_type == "ATTACHMENT":
        return attachments.message_for_attachment_type(message, attachment_type)
    else:
        return message

def attachment_type_text(row):
    if row["type"] == "ATTACHMENT":
        attachment_type = f"> Attachment Type: {row['attachment_type']}"
        file_name = os.path.basename(row["message"])
        file_name = f"> File Name: {file_name}"
        return f"{attachment_type}\n{file_name}"
    else:
        return ""

def createMarkdownEntryForRow(row):
    header = "# Text"
    author = f"> Author: {row['author']}"
    date_time = f"> Date/time: {row['timestamp']}"
    message_type = f"> Type: {row['type']}"
    attachment_type = attachment_type_text(row)
    message = createMarkdownTextForMessageType(row['message'], row['type'], row['attachment_type'])
    # build the text of the message
    return (
        f"{header}\n"
        f"{author}\n"
        f"{date_time}\n"
        f"{message_type}\n"
        f"{attachment_type}\n\n"
        f"{message}\n\n"
    )

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



input_file = "/Users/conallmcginty/Desktop/zoe-present/outputs/chat.csv"
output_file = "/Users/conallmcginty/Desktop/zoe-present/outputs/entire_chat.md"
output_root = "/Users/conallmcginty/Desktop/zoe-present/outputs/markdown"

create_dir(output_root)

df = dataframe.load_dataframe(input_file)
df = dataframe.initialise_dataframe(df)
dataframe.sanity_checks(df)

start_year = 2023
end_year = 2024
for year in range(start_year, end_year + 1):
    for month in range(1, 12 + 1):
        rows_for_month = get_rows_for_month(df, year, month)
        if rows_for_month.empty:
            continue
        month_name = calendar.month_name[month].lower()
        # create output directory for this month
        month_string = str(month).zfill(2)
        formatted_date = f"{year}-{month_string}-{month_name}"
        output_dir = os.path.join(output_root, formatted_date)
        create_dir(output_dir)
        # create markdown elements
        markdown_output_path = os.path.join(output_dir, f"{formatted_date}.md")
        markdown_elements = []
        for index, row in rows_for_month.iterrows():
            markdown_elements.append(createMarkdownEntryForRow(row))
        # write them to the output path
        with open(markdown_output_path, "w") as f:
            for el in markdown_elements:
                f.write(el)
        attachments.link_attachments_to_output_directory(rows_for_month, output_dir)
        # print when we're finished that month
        print(f"{year} - {month_name} - {markdown_output_path}")


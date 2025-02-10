from utils import dataframe
import pandas as pd
import os

input_file = "/Users/conallmcginty/Desktop/zoe-present/outputs/chat.csv"

df = dataframe.from_csv(input_file)

df["status"] = "not-checked"

df = dataframe.sanity_checks(df, input_file)

text_viewer_project = "/Users/conallmcginty/Desktop/zoe-present/processing/text-viewer/"
database_output_path = os.path.join(text_viewer_project, "mydb.sqlite")

# write database to output
dataframe.to_sqlite(df, database_output_path)

public_folder = os.path.join(text_viewer_project, "public", "attachments")
# make sure public folder exists
if not os.path.exists(public_folder):
    os.makedirs(public_folder, exist_ok=True)

# symlink all attachments to the public folder of the text viewer
attachments = df[df["type"] == "ATTACHMENT"]
for input_path in attachments["message"]:
    dataframe.symlink_attachment_path_to_folder(input_path, public_folder)

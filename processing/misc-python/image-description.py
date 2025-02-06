import ollama
from utils import dataframe

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

def get_image_description(input_file):
    print(f"Describing {input_file}")
    res = ollama.chat(
        model="minicpm-v",
        messages=[
            {
                'role': 'user',
                'content': 'Describe this image in clear english language. No other language other than english should be used. Keep the descriptions as short as possible.',
                'images': [input_file]
            }
        ]
    )
    text = res['message']['content']
    print(f"Description: {text}")
    return text

input_csv = "/Users/conallmcginty/Desktop/zoe-present/outputs/chat.csv"

df = dataframe.load_dataframe(input_csv)
df = dataframe.initialise_dataframe(df)
image = get_all_image_attachments(df)

print(f"Processing {len(image)} image files")

for index, row in image.iterrows():
    input_file = row["message"]
    df.loc[index, "image_description"] = get_image_description(input_file)
    # write the df back to the csv now
    # means we don't have to re-do this file again
    # as the next time we run the script it won't be processed
    df.to_csv(input_csv, index = False, date_format='%Y-%m-%dT%H:%M:%SZ')
    print(f"Finished processing: {input_file}")
    print("\n\n")

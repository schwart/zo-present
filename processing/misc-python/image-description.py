import ollama
from utils import dataframe, attachments

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

df = dataframe.from_csv(input_csv)
df = dataframe.initialise_dataframe(df)
image = attachments.get_all_image_attachments(df)

print(f"Processing {len(image)} image files")

for index, row in image.iterrows():
    input_file = row["message"]
    df.loc[index, "image_description"] = get_image_description(input_file)
    # write the df back to the csv now
    # means we don't have to re-do this file again
    # as the next time we run the script it won't be processed
    dataframe.to_csv(df, input_csv)
    print(f"Finished processing: {input_file}")
    print("\n\n")

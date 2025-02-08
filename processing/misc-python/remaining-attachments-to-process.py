from utils import dataframe, attachments

input_csv = "/Users/conallmcginty/Desktop/zoe-present/outputs/chat.csv"

df = dataframe.from_csv(input_csv)
df = dataframe.initialise_dataframe(df)

audio = attachments.get_all_audio_attachments(df)
image = attachments.get_all_image_attachments(df)

print(f"Number of remaining audio attachments: {len(audio.index)}")
print(f"Number of remaining image attachments: {len(image.index)}")


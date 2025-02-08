import whisper
from utils import dataframe, attachments

def get_transcript(input_file):
    print(f"Processing {input_file}")
    result = model.transcribe(input_file)
    return result["text"]

# load model first
print("Loading model...")
model = whisper.load_model("turbo")
print("Finished loading model")

input_csv = "/Users/conallmcginty/Desktop/zoe-present/outputs/chat.csv"

df = dataframe.from_csv(input_csv)
df = dataframe.initialise_dataframe(df)
audio = attachments.get_all_audio_attachments(df)

print(f"Processing {len(audio)} audio files")

for index, row in audio.iterrows():
    input_file = row["message"]
    df.loc[index, "audio_transcript"] = get_transcript(input_file)
    # write the df back to the csv now
    # means we don't have to re-do this file again
    # as the next time we run the script it won't be processed
    dataframe.to_csv(df, input_csv)
    print(f"Finished processing: {input_file}")


# file_one = "/Users/conallmcginty/Desktop/zoe-present/chat-data/00000627-AUDIO-2023-09-28-18-39-42.opus"
# file_two = "/Users/conallmcginty/Desktop/zoe-present/chat-data/00016486-AUDIO-2024-03-07-17-41-34.opus"
#
#
#
# result_two = model.transcribe(file_two)
# print("Result two:")
# print(result_two["text"])

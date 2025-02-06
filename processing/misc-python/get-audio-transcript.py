import whisper
from utils import dataframe

def get_all_audio_attachments(df):
    # get all rows that are audio attachments
    # that don't already have a transcript written to them
    attachment_mask = df["type"] == "ATTACHMENT"
    audio_attachment_mask = df["attachment_type"] == "AUDIO"

    try:
        transcript_mask = df["audio_transcript"].isnull() == True
        return df.loc[attachment_mask & audio_attachment_mask & transcript_mask]
    # this means there's no "audio_transcript" column yet
    # in that case, just return all the audio attachments
    except KeyError:
        return df.loc[attachment_mask & audio_attachment_mask]

def get_transcript(input_file):
    print(f"Processing {input_file}")
    result = model.transcribe(input_file)
    return result["text"]

# load model first
print("Loading model...")
model = whisper.load_model("turbo")
print("Finished loading model")

input_csv = "/Users/conallmcginty/Desktop/zoe-present/outputs/chat.csv"

df = dataframe.load_dataframe(input_csv)
df = dataframe.initialise_dataframe(df)
audio = get_all_audio_attachments(df)

print(f"Processing {len(audio)} audio files")

for index, row in audio.iterrows():
    input_file = row["message"]
    df.loc[index, "audio_transcript"] = get_transcript(input_file)
    # write the df back to the csv now
    # means we don't have to re-do this file again
    # as the next time we run the script it won't be processed
    df.to_csv(input_csv, index = False, date_format='%Y-%m-%dT%H:%M:%SZ')
    print(f"Finished processing: {input_file}")


# file_one = "/Users/conallmcginty/Desktop/zoe-present/chat-data/00000627-AUDIO-2023-09-28-18-39-42.opus"
# file_two = "/Users/conallmcginty/Desktop/zoe-present/chat-data/00016486-AUDIO-2024-03-07-17-41-34.opus"
#
#
#
# result_two = model.transcribe(file_two)
# print("Result two:")
# print(result_two["text"])

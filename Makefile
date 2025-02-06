OUTPUT_DIRECTORY = outputs
CSV_OUTPUT = $(OUTPUT_DIRECTORY)/chat.csv

.PHONY: clean csv audio_transcript image_description

$(CSV_OUTPUT):
	npm run parse --prefix "./processing/chat-parser/"
	touch $(CSV_OUTPUT)

csv: $(CSV_OUTPUT)

audio_transcript: csv
	python ./processing/misc-python/get-audio-transcript.py

image_description: csv
	python ./processing/misc-python/image-description.py

clean:
	echo "Cleaning $(OUTPUT_DIRECTORY)"
	rm -rf $(OUTPUT_DIRECTORY)/*

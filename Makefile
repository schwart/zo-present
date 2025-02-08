OUTPUT_DIRECTORY = outputs
CSV_OUTPUT = $(OUTPUT_DIRECTORY)/chat.csv
MARKDOWN_DIRECTORY = $(OUTPUT_DIRECTORY)/markdown
MARKDOWN_MARKER = $(MARKDOWN_DIRECTORY)/.markdown_generated
HTML_MARKER = $(MARKDOWN_DIRECTORY)/.html_generated

.PHONY: clean csv audio_transcript image_description markdown

$(CSV_OUTPUT):
	npm run parse --prefix "./processing/chat-parser/"
	touch $(CSV_OUTPUT)

csv: $(CSV_OUTPUT)

audio_transcript: csv
	python ./processing/misc-python/get-audio-transcript.py

image_description: csv
	touch $(MARKDOWN_MARKER)
	python ./processing/misc-python/image-description.py

$(MARKDOWN_MARKER): csv
	python ./processing/misc-python/create-markdown-from-chat-csv.py
	touch $(MARKDOWN_MARKER)

markdown: $(MARKDOWN_MARKER)

$(HTML_MARKER): $(MARKDOWN_MARKER)
	python ./processing/misc-python/convert-markdown-to-html.py
	touch $(HTML_MARKER)

html: $(HTML_MARKER)

clean-all:
	echo "Cleaning $(OUTPUT_DIRECTORY)"
	rm -rf $(OUTPUT_DIRECTORY)/*

clean-md:
	echo "Cleaning all .md and .html files"
	rm -rf $(MARKDOWN_DIRECTORY)

remaining:
	python ./processing/misc-python/remaining-attachments-to-process.py

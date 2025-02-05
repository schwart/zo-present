# Zoë Present

This is a repo containing all the stuff for Zoë's VERY LATE anniversary present.

I've not touched it in a while so I'm just going to list out what's in here for now,
and we can start to put together a plan soon.

## Contents

.
|-- README.md
|-- chat-data -> The "raw" chat data exported from Whatsapp.
|-- design -> All stuff related to the design of the final book.
|-- outputs -> Any outputs from processing scripts.
`-- processing -> Any scripts that process the chat data in some way.

## Steps

### Initial Parsing

First, we need to parse the chat into a CSV file, so it can be easily be parsed by OTHER tools.

The `chat-parser` project does this. Then it'll output a `chat.csv` file to the `outputs` folder.

### Split into months

Next we, need to split the parsed chat into months.


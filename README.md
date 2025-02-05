# Zoë Present

This is a repo containing all the stuff for Zoë's VERY LATE anniversary present.

I've not touched it in a while so I'm just going to list out what's in here for now,
and we can start to put together a plan soon.

## Contents

.
|-- README.md -> This file
|-- chat -> Where the "raw" chat data lives. Contains `_chat.txt` which is the raw text chat.
|-- chat-parser -> Takes the raw text chat and transforms it into a CSV.
|-- in-design -> Any stuff I've made in InDesign for this book.
|-- latex -> Failed latex files from me trying to use latex to make the book.
|-- misc-python -> Some csv parsing stuff, uses pandas to try to split things into months?
|-- outputs -> For any output files that are generated.
`-- whatsapp-book-generator -> The python "book" generator that uses latex.


## Steps

### Initial Parsing

First, we need to parse the chat into a CSV file, so it can be easily be parsed by OTHER tools.

The `chat-parser` project does this. Then it'll output a `chat.csv` file to the `outputs` folder.

### Split into months

Next we, need to split the parsed chat into months.


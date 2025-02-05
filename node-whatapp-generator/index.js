const fs = require("node:fs");
const whatsapp = require("whatsapp-chat-parser");

const text = fs.readFileSync("_chat.txt", 'utf8');
const messages = whatsapp.parseString(text, { parseAttachments: true });

console.log(`Number of messages: ${messages.length}`);

// cols
// - date
// - author
// - message
// - type


const filePath = "whatsapp-chat.csv";

fs.appendFileSync(filePath, "timestamp,author,message\n");

function getMessageText(message) {
	if (message.attachment) {
		return message.attachment.fileName;
	}
	return message.message.replaceAll("\"", "\"\"");
}

for (const message of messages) {
	if (message.date === undefined) {
		throw new Error(`Can't parse ${message.message}`);
	}
	const timestamp = message.date.toISOString();
	const author = message.author;
	const mess = getMessageText(message);
	const type = message.attachment ? "ATTACHMENT" : "MESSAGE";
	const line = `${timestamp},${author},\"${mess}\",${type}\n`;
	fs.appendFileSync(filePath, line);
}

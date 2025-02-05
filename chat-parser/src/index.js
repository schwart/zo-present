const whatsapp = require("whatsapp-chat-parser");
const path = require("node:path");
const fs = require("node:fs");
const { 
	askToOverwriteOutput, 
	getChatText, 
	initialiseCsvFile, 
	createCsvLineFromMessage 
} = require("./utils");


async function run() {
	// get the input path
	const chatInputPath = path.resolve("../chat/_chat.txt");
	// get the ouptut path
	const outputPath = path.resolve("../outputs/chat.csv");
	// check if the output path should be overwritten
	await askToOverwriteOutput(outputPath);
	initialiseCsvFile(outputPath);
	// parse the chat into messages
	const inputText = getChatText(chatInputPath);
	const messages = whatsapp.parseString(inputText, { parseAttachments: true });
	console.log(`Number of messages: ${messages.length}`);
	// convert message to csv line, append it to output file
	for (const message of messages) {
		const line = createCsvLineFromMessage(message);
		fs.appendFileSync(outputPath, line);
	}
	return outputPath;
}

run()
	.then((outputPath) => console.log(`Written output to: ${outputPath}`))
	.catch((err) => console.error("Error creating csv.", err));

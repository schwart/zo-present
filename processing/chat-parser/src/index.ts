import * as fs from "node:fs";
const {
} = require("./utils");
import { parseString } from "./chat-parser/index";
import path from "node:path";
import {
	askToOverwriteOutput,
	getChatText,
	initialiseCsvFile,
	createCsvLineFromMessage
} from "./utils";


async function run() {
	// get the input path
	const chatInputPath = path.resolve("../../chat-data/_chat.txt");
	// get the ouptut path
	const outputPath = path.resolve("../../outputs/chat.csv");
	// check if the output path should be overwritten
	await askToOverwriteOutput(outputPath);
	initialiseCsvFile(outputPath);
	// parse the chat into messages
	const inputText = getChatText(chatInputPath);
	const messages = parseString(inputText, { parseAttachments: true });
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

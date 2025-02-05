import process from "node:process";
import * as readline from "node:readline/promises";
import * as fs from "node:fs";
import {Message} from "./chat-parser";

// checks if the output file passed in already exists
// if it does, asks the user if they want to overwrite it
export async function askToOverwriteOutput(outputPath: string) {
	if (fs.existsSync(outputPath)) {
		const rl = readline.createInterface({
			input: process.stdin,
			output: process.stdout
		});

		const answer = await rl.question(`Output path (${outputPath}) already exists, overwrite? (y/n)`);
		const ans = answer.trim().toLowerCase();
		switch (ans) {
			case 'y': {
				// should delete output path then return
				console.log(`Deleting ${outputPath}`);
				fs.unlinkSync(outputPath);
				break;
			}
			case 'n': {
				console.log("Not overwriting, exiting...");
				process.exit(0);
			}
			Default: {
				console.log("Invalid input, exiting...");
				process.exit(1);
			}
		}

		rl.close();
	}
}

// cols
// - date
// - author
// - message
// - type
export function initialiseCsvFile(outputPath: string) {
	fs.appendFileSync(outputPath, "timestamp,author,message,type\n");
}

export function getChatText(chatInputPath: string) {
	console.log(`Using ${chatInputPath}`);
	return fs.readFileSync(chatInputPath, 'utf8');
}

export function getMessageText(message: Message) {
	if (message.attachment) {
		return message.attachment.fileName;
	}
	return message.message.replaceAll("\"", "\"\"");
}

// cols
// - date
// - author
// - message
// - type
export function createCsvLineFromMessage(message: Message) {
	if (message.date === undefined) {
		throw new Error(`Can't parse ${message.message}`);
	}
	const timestamp = message.date.toISOString();
	const author = message.author;
	const mess = getMessageText(message);
	const type = message.attachment ? "ATTACHMENT" : "MESSAGE";
	const csvLine = `${timestamp},${author},\"${mess}\",${type}\n`;
	return csvLine;
}

const readline = require("node:readline/promises");
const process = require("node:process");
const fs = require("node:fs");

// checks if the output file passed in already exists
// if it does, asks the user if they want to overwrite it
async function askToOverwriteOutput(outputPath) {
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
			default: {
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
function initialiseCsvFile(outputPath) {
	fs.appendFileSync(outputPath, "timestamp,author,message,type\n");
}

function getChatText(chatInputPath) {
	console.log(`Using ${chatInputPath}`);
	return fs.readFileSync(chatInputPath, 'utf8');
}

function getMessageText(message) {
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
function createCsvLineFromMessage(message) {
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

module.exports = {
	askToOverwriteOutput,
	initialiseCsvFile,
	getChatText,
	createCsvLineFromMessage
}

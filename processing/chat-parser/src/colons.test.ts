import { parseString } from "./chat-parser/index";
import path from "node:path";
import {
    getChatText,
    createCsvLineFromMessage
} from "./utils";


async function run() {
    const chatInputPath = path.resolve("./testChat.txt");
    const inputText = getChatText(chatInputPath);
    const messages = parseString(inputText, { parseAttachments: true });
    console.log(`Number of messages: ${messages.length}`);
    // convert message to csv line, append it to output file
    for (const message of messages) {
        const line = createCsvLineFromMessage(message);
    }
    return "something";
}

run()
    .then((outputPath) => console.log(`Written output to: ${outputPath}`))
    .catch((err) => console.error("Error creating csv.", err));

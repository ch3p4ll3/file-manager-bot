# file-manager-bot
file-manager-bot is a telegram bot that allows you to execute shell commands, 
upload your pc files to a telegram channel (max 2GB), save the files you send to the bot on your pc

## How it works
with the bot you can choose the files you want, if you send the command `dw <path>` a 
userbot will load the requested file on a telegram channel. If you send a document 
to the bot the document will be saved in a folder called downloads inside the files 
folder of this project. To navigate through the folders you can use the `cd <path>` command, 
any other message you send to the bot will be executed on the shell and, once the 
execution is finished, one or more messages will be sent with the command output.

## Available commands
-   `dw <path>` - Sends the file specified in <path> on the channel
-   `cd <path>` - Moves to the specified folder
-   All other messages sent execute them as if they were written in the shell
-   If you send a document to the bot it will download it to the download folder
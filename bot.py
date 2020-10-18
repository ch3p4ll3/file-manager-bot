import os
import subprocess
import shlex

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, \
    MessageEmpty

from userbot import upload
from json_validation import get_configs

app = Client("my_bot", bot_token=get_configs().bot.token,
             api_hash=get_configs().userbot.api_hash,
             api_id=get_configs().userbot.api_id,
             workdir=os.path.abspath(os.path.dirname(__file__)))


def split_every_n_chars(string, n) -> list:
    return [(string[i:i+n]) for i in range(0, len(string), n)]


def run_command(message: Message) -> None:
    command = shlex.split(message.text)
    result = subprocess.run(command, stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')

    try:
        message.reply_text(result)
    except MessageTooLong:
        for i in split_every_n_chars(result, 2048):
            message.reply_text(i)

    except MessageEmpty:
        pass


def change_dir(message: Message) -> None:
    path = shlex.split(message.text)[1]
    if os.path.exists(path):
        os.chdir(path)
        message.reply_text(f"Chrooted in {path}")
    else:
        message.reply_text("Error, path does not exists")


def download(message: Message) -> None:
    message.download(f"{os.path.abspath(os.path.dirname(__file__))}/"
                     f"downloads/{message.document.file_name}")


@app.on_message(filters.command("help"))
def handle_help_command(client: Client, message: Message) -> None:
    if message.chat.id in get_configs().bot.id:
        message.reply_text(f"Welcome to {client.get_me().first_name}!\n\n"
                           f"Available commands:\n"
                           f"`dw <path>` - Sends the file specified in "
                           f"<path> on the channel\n"
                           f"`cd <path>` - Moves to the specified folder\n"
                           f"All other messages sent execute them as if "
                           f"they were written in the shell\n"
                           f"If you send a document to the bot it will "
                           f"download it to the download folder",
                           parse_mode="markdown")
    else:
        message.reply_text(f"Welcome to {client.get_me().first_name}!\n\n"
                           f"Unfortunately you are not among the users "
                           f"authorized to use this bot! You can still "
                           f"grab your copy [here]"
                           f"(https://github.com/ch3p4ll3/file-manager-bot)",
                           parse_mode="markdown")


@app.on_message(filters.command("start"))
def handle_start_command(client: Client, message: Message) -> None:
    if message.chat.id in get_configs().bot.id:
        message.reply_text(f"Welcome to {client.get_me().first_name}!\n\n"
                           f"This bot allows you to execute shell commands, "
                           f"upload your pc files to a telegram channel "
                           f"(max 2GB), save the files you send to the "
                           f"bot on your pc.\n\n"
                           f"run /help for the command list")
    else:
        message.reply_text(f"Welcome to {client.get_me().first_name}!\n\n"
                           f"Unfortunately you are not among the users "
                           f"authorized to use this bot! You can still "
                           f"grab your copy [here]"
                           f"(https://github.com/ch3p4ll3/file-manager-bot)",
                           parse_mode="markdown")


@app.on_message(filters.private & filters.text)
def handle_text(client: Client, message: Message) -> None:
    if message.chat.id in get_configs().bot.id:
        if message.text.startswith("dw "):
            upload(message)

        elif message.text.startswith("cd "):
            change_dir(message)

        else:
            run_command(message)
    else:
        message.reply_text("You are not authorized")


@app.on_message(filters.private & filters.document)
def handle_files(client: Client, message: Message) -> None:
    if message.chat.id in get_configs().bot.id:
        download(message)
    else:
        message.reply_text("You are not authorized")

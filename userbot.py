import shlex

from pyrogram import Client
from pyrogram.types import Message
import os

from json_validation import get_configs


def upload(message: Message):
    api_id = get_configs().userbot.api_id
    api_hash = get_configs().userbot.api_hash
    work_dir = os.path.abspath(os.path.dirname(__file__))

    with Client("my_account", api_id=api_id, api_hash=api_hash,
                workdir=work_dir) as app:
        path = shlex.split(message.text)[1]
        if os.path.exists(path) and os.path.isfile(path):
            try:
                message.reply_text(f"Sending file {path}")
                app.send_document(get_configs().bot.channel_id, path)
            except ValueError:
                message.reply_text("Telegram doesn't support uploading "
                                   "files bigger than 2000 MiB")
        else:
            message.reply_text("The path does not exist or is not a file")

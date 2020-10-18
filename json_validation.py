from typing import List
from pydantic import BaseModel
import json
import os


class Bot(BaseModel):
    token: str
    id: List[int] = []
    channel_id: int


class Userbot(BaseModel):
    api_id: int
    api_hash: str


class Validator(BaseModel):
    bot: Bot
    userbot: Userbot


def get_configs():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f"{current_dir}/login.json") as login_file:
        validator = Validator(**json.load(login_file))
        return validator

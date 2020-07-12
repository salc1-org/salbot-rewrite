"""
Created by vcokltfre at 2020-07-12
"""
import json
import os
## For now temporary methods which will allow salbot to function without a working API using JSON. These bindings should stay the same when the api is online.

## Code in this section is temporary to use JSON

temp_stor = "./api/data/"

def create_file_structure():
    if not os.path.exists(temp_stor):
        os.makedirs(temp_stor)
        with open(temp_stor + "mutes.json", 'w') as f:
            json.dump([], f)

## End JSON code

class UserNotFound(Exception):
    pass

def getmute(userid: int) -> dict:
    with open(temp_stor + "mutes.json") as f:
        jsd = json.load(f)

    for item in jsd:
        if item["uid"] == userid:
            return item

    raise UserNotFound(f"getmute: User {userid} not found.")

def getmutes() -> list:
    with open(temp_stor + "mutes.json") as f:
        return json.load(f)

def mute(userid: int, time_end: int, reason: str, by: int, guild: int) -> bool:
    with open(temp_stor + "mutes.json") as f:
        jsd = json.load(f)

    for item in jsd:
        if item["uid"] == userid:
            return False

    jsd.append({
        "uid":userid,
        "end":time_end,
        "reason":reason,
        "by":by,
        "guild":guild
    })

    with open(temp_stor + "mutes.json", 'w') as f:
        json.dump(jsd, f)

    return True

def unmute(userid: int) -> bool:
    with open(temp_stor + "mutes.json") as f:
        jsd = json.load(f)

    for i, item in enumerate(jsd):
        if item["uid"] == userid:
            jsd.pop(i)
            with open(temp_stor + "mutes.json", 'w') as f:
                json.dump(jsd, f)
            return True

    return False
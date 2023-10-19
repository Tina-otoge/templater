from templater.objects import Image

import templater

schemas = {
    2: {
        "background": "https://cdn.discordapp.com/attachments/485898960247193610/1099004139402448947/business-community.png",
        "size": 20,
        "positions": [
            "10 30",
            "50 20",
        ],
    }
}

schema = schemas.get(len(templater.params.profile_ids))
if not schema:
    raise ValueError("No schema for this number of profiles")

templater.items["background"].src = schema["background"]
templater.items["avatars"].apply = {"size": schema["size"]}
for position in schema["positions"]:
    templater.items["avatars"].items.append(Image(position=position))

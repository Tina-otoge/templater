from templater.ext import discord

import templater

for index, profile_id in enumerate(templater.params.profile_ids):
    user = discord.get_user(profile_id)
    templater.items["avatars"].items[index].src = user.avatar_url

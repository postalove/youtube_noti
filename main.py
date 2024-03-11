'''
Discord-Bot-Module template. For detailed usages,
 check https://interactions-py.github.io/interactions.py/

Copyright (C) 2024  __retr0.init__

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import interactions
# Use the following method to import the internal module in the current same directory
import json
import requests
import re
# Import the os module to get the parent path to the local files
import os
# aiofiles module is recommended for file operation
import aiofiles
import asyncio
# You can listen to the interactions.py event
from interactions.api.events import MessageCreate
# You can create a background task
from interactions import Task, IntervalTrigger
from . import youtube

class YoutubeNoti(interactions.Extension):
    module_base: interactions.SlashCommand = interactions.SlashCommand(
        name="add",
        description="添加"
    )
    module_group: interactions.SlashCommand = module_base.group(
        name="Youtube",
        description="Youtube"
    )


        

    @module_group.subcommand("notification", sub_cmd_description="添加Youtube更新提醒")
    
    @interactions.slash_option(
        name = "youtube_channel_url",
        description = "youtubep频道链接",
        required = True,
        opt_type = interactions.OptionType.STRING
    )
    async def noti(self, ctx: interactions.SlashContext, youtube_channel_url: str):
        # The local file path is inside the directory of the module's main script file
        if '技术公务员' not in [role.name for role in ctx.author.roles]:
            await ctx.send('Missing Permission',ephemeral=True)
            return
        
        try:
            history=ctx.channel.history
            async for mess in history(limit=1):
                match = re.search(r"/channels/(?P<channel_id>\d+)/(?P<thread_id>\d+)", mess.jump_url)
                if match:
                    channel_id=match.group("channel_id")
                    thread_id=match.group("thread_id")
                    if channel_id != 1216434305455358033:
                        await ctx.send('Unvalid channel!',ephemeral=True)
                        return 

                else:
                    await ctx.send('Unvalid channel!',ephemeral=True)
                    return 
                
            async with aiofiles.open(f"{os.path.dirname(__file__)}/youtubedata.json",mode='r') as afp:
                data = await json.loads(afp)
            data[str(thread_id)]={}
            data[str(thread_id)]["youtube_channel_name"]=youtube.get_youtube_channel_name(youtube_channel_url)
            data[str(thread_id)]["youtube_channel"]=youtube_channel_url
            data[str(thread_id)]["latest_video_url"]="none"
            async with aiofiles.open(f"{os.path.dirname(__file__)}/youtubedata.json",mode='w') as afp:

                json.dumps(data,afp)
            await ctx.send('Channel loaded!',ephemeral=True)
        except:
            await ctx.send("Failed to add!",ephemeral=True)   
        
        

    @interactions.listen(MessageCreate)
    async def on_messagecreate(self, event: MessageCreate):
        if not self.check_youtube.running:
            self.check_youtube.start()
            

    @Task.create(IntervalTrigger(minutes=5))
    async def check_youtube(self):
        try:
            async with aiofiles.open(f"{os.path.dirname(__file__)}/youtubedata.json",mode='r') as f:
                data=json.load(f)
                
                #printing here to show
            print("Now Checking!")

                #checking for all the channels in youtubedata.json file
            for thread_id in data:
                print(f"Now Checking For {data[thread_id]['youtube_channel']}")
                    #getting youtube channel's url
                channel = f"{data[thread_id]['youtube_channel']}"

                    #getting html of the /videos page
                html = requests.get(channel+"/videos").text

                    #getting the latest video's url
                    #put this line in try and except block cause it can give error some time if no video is uploaded on the channel
                try:
                    latest_video_url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
                except:
                    continue

                    #checking if url in youtubedata.json file is not equals to latest_video_url
                if not str(data[thread_id]["latest_video_url"]) == latest_video_url:

                    #changing the latest_video_url
                    data[str(thread_id)]['latest_video_url'] = latest_video_url

                    #dumping the data
                    async with aiofiles.open(f"{os.path.dirname(__file__)}/youtubedata.json",mode='w') as afp:
                        json.dumps(data, afp)

                    #getting the channel to send the message
                    
                    thread = self.bot.get_guild(1150630510696075404).get_channel(1216434305455358033).get_thread(int(thread_id))

                    #sending the msg in discord channel
                    #you can mention any role like this if you want
                    channel_name=data[thread_id]['youtube_channel_name']
                    msg = f"{channel_name} Just Uploaded A Video : {latest_video_url}"
                    #if you'll send the url discord will automaitacly create embed for it
                    #if you don't want to send embed for it then do <{latest_video_url}>

                    await thread.send(msg)
                await asyncio.sleep(10)
        except:
            return
    # The command to start the task

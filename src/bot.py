import get_atis
from gtts import gTTS
import os
import discord
from dotenv import load_dotenv

language = "en"

airport_icao = "LOWW"
information_spoken = "Hotel"
runways_dep = "3 4 and 2 9"
runways_arr = "1 6"
ils = "1 6"


def make_atis_mp3(airport_icao, information_spoken, runways_dep, runways_arr, ils):
    atis_text = get_atis.get_atis(airport_icao, information_spoken, runways_dep, runways_arr, ils)

    speech = gTTS(text=atis_text, lang=language, slow=False)

    speech.save("ATIS.mp3")

## Discord Bot


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


"""
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startwith("!atis generate"):
        text = message.content.split(",")

        airport_icao = text[1]
        information_spoken = text[2]
        runways_dep = text[3]
        runways_arr = text[4]
        ils = text[5]

        make_atis_mp3(airport_icao, information_spoken, runways_dep, runways_arr, ils)
        voice_channel = "kek"
        vc = await client.join_voice_channel(voice_channel)
        player = vc.create_ffmpeg_player('ATIS.mp3', after=lambda: print('done'))
        player.start()
        while not player.is_done():
            await asyncio.sleep(1)

        # disconnect after the player has finished
        player.stop()

client.run(TOKEN)
"""

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        global current_atis

        if message.author.id == self.user.id:
            return

        ID = "704757993723396107"

        id = client.get_guild(ID)
        channels = ["bot"]

        if str(message.channel) in channels:

            if message.content.startswith("!atis generate"):
                text = message.content.split(",")

                airport_icao = text[1]
                information_spoken = text[2]
                runways_dep = text[3]
                runways_arr = text[4]
                ils = text[5]

                make_atis_mp3(airport_icao, information_spoken, runways_dep, runways_arr, ils)
                global current_atis
                current_atis = str(airport_icao)
                channel = message.author.voice.channel
                await message.channel.send(f"Generated and playing ATIS for {current_atis} in {channel.name}")
                try:
                    vc = await channel.connect()
                except discord.errors.ClientException:
                    pass

                #
                vc.play(discord.FFmpegPCMAudio('ATIS.mp3'))
                while vc.is_playing():
                    pass

                await vc.disconnect()
                #print("Done playing")

            if message.content.startswith("!atis play"):
                channel = message.author.voice.channel
                await message.channel.send(f"Playing ATIS for {current_atis} in {channel.name}")

                try:
                    vc = await channel.connect()
                except discord.errors.ClientException:
                    pass

                try:

                    vc.play(discord.FFmpegPCMAudio('ATIS.mp3'))
                    while vc.is_playing():
                        pass

                except Exception as e:
                    print(e)
                    await message.channel.send("Sry there is no ATIS avaible at the moment!")

                await vc.disconnect()
                #print("Done playing")

            if message.content.startswith("!atis info"):
                await message.channel.send(f"Current ATIS is for {current_atis}")

            if message.content.startswith("!atis raw"):
                await message.channel.send(get_atis.get_raw_atis(current_atis))
client = MyClient()
client.run(TOKEN)

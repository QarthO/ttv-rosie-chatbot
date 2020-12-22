from twitchio.ext import commands

irc_token = 'oauth:aytrhdypc5gy6l0gimol6xv53n7jhs'
client_id = 'dx5nmofsy63hp5updnr8ifksaoygbf'
bot_nick = 'roseiol'
command_prefix = '!'
channel = 'roselol'

simple_commands = {
        "discord": "https://discord.gg/u4XF65k",
        "twitter": "https://twitter.com/rohhse",
        "website": "rosD https://roselol.com/ rosD",
        "instagram": "https://www.instagram.com/rowstheboat/",
        "raffle": "rosePOP GET RAFFLE TICKET IN POINTS STORE FOR A rosePOP  rosePOP CHANCE TO GET DRAWN IN GIF FORM rosePOP",
        "youtube": "rosD my new youtube video https://bit.ly/38iN6X2 rosD",
        "rank": "rank your mom NODDERS",
        "playlist": "https://spoti.fi/34r0EhV",
        "commission": "https://bit.ly/3h6nz7i",
        "uwu": "https://www.twitch.tv/roselol/clip/AgreeableTentativeSushiFloof?filter=clips&range=30d&sort=time",
        "gettingoverit": "https://clips.twitch.tv/PatientCheerfulAubergineJebaited https://clips.twitch.tv/GoodCooperativeMilkPipeHype https://clips.twitch.tv/CourageousEagerDonkeyUWot",
        "money": "https://clips.twitch.tv/FaithfulFlaccidStarTinyFace",
        "apples": "https://www.twitch.tv/roselol/clip/DependableRelatedCoffeeStinkyCheese?filter=clips&range=24hr&sort=time",
        "patrick": "https://www.twitch.tv/roselol/clip/ShakingSincereSkirretBCouch?filter=clips&range=7d&sort=time",
        "yoshi": "https://www.twitch.tv/roselol/clip/SilkyInexpensiveCoyoteAMPTropPunch?filter=clips&range=7d&sort=time",
        "catmarching": "https://www.youtube.com/watch?v=lAIGb1lfpBw&t=14s"
    }

smart_responses = {
        "hey": "hi tiffShy",
        "oops": "yep catJAM",
        "shit": "SHITTERS",
        "nice": "POGSLIDE POGSLIDE POGSLIDE POGSLIDE POGSLIDE POGSLIDE POGSLIDE POGSLIDE POGSLIDE POGSLIDE POGSLIDE POGSLIDE",
        "catjam": "catJAM catJAM catJAM catJAM catJAM catJAM catJAM catJAM catJAM catJAM catJAM catJAM",
        "lul": "LUL",
        "yes": "NOPERS",
        "joe": "joe mama pepeD",
        "rank": "rank your mom NODDERS",
        "hi": "hey peepoShy",
        "playlist": "https://spoti.fi/34r0EhV",
}

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=irc_token,
            client_id=client_id, 
            nick=bot_nick, 
            prefix=command_prefix,
            initial_channels=[channel]
        )

    # On bot startup
    async def event_ready(self):
        print(f'Bot {bot_nick} connected to twitch.tv/{channel}')
        ws = bot._ws  # this is only needed to send messages within event_ready
        await ws.send_privmsg(channel, f"/me is online")

    # Everytime a message is sent in the channel
    async def event_message(self, message):
        #await self.handle_simple_commands(message)
        await self.handle_commands(message)
        await self.handle_smart_responses(message)

    # Advance Commdands
    @commands.command(name='shoutout', aliases={'so'})
    async def cmd_shoutout(self, ctx):
        msg = ctx.content.split()
        if len(msg) != 2: return
        who = msg[1][1:] if msg[1].startswith('@') else msg[1]
        print(f'Shouting out: {who}')
        response = f'/me BOOBA go --> https://www.twitch.tv/{who} <-- or i ziggs ult you . . . (in game)'
        await ctx.send(response)

    @commands.command(name='timeout')
    async def cmd_timeout(self, ctx):
        username = ctx.author.name
        time = 5
        reason = 'You timed yourself out... lol!'
        print(f'Self timing out: {username}')
        await ctx.send(f'/me bye bye @{username}!!!')
        await ctx.timeout(user=username, duration=time, reason=reason)
    
    @commands.command(name='vanish')
    async def cmd_vanish(self, ctx):
        username = ctx.author.name
        time = 1
        reason = 'Clearing your chat messages'
        print(f'Vanishing: {username}')
        await ctx.timeout(user=username, duration=time, reason=reason)

    @commands.command(name='simple_commands', aliases=simple_commands.keys())
    async def handle_simple_commands(self, ctx):
        response = simple_commands.get(ctx.content[1:])
        await ctx.send(response)

    async def handle_smart_responses(self, message):
        for trigger in smart_responses:
            if trigger in message.content:
                print(f'Trigger: {trigger}')
                print(f'Message: {message.content}')
                await self.get_context(message).send(smart_responses.get(trigger))
            


    

bot = Bot()
bot.run()

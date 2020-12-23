import yaml
from twitchio.ext import commands



irc_token = ''
client_id = ''
bot_nick = 'roseiol'
command_prefix = '!'
channel = 'roselol'

cmds = ''

with open('auth.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    irc_token = data.get('auth-id')
    client_id = data.get('client-id')

with open('commands.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    cmds = data.get('commands')
    
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
        print(f'Bot connected to twitch.tv/roselol')
        ws = bot._ws  # this is only needed to send messages within event_ready
        await ws.send_privmsg(channel, f"/me is online")

    # Everytime a message is sent in the channel
    async def event_message(self, message):
        await self.handle_commands(message)

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

    @commands.command(name='commands_from_file', aliases=cmds.keys())
    async def commands_from_file(self, ctx):
        response = cmds.get(ctx.content[1:]).get('response')
        await ctx.send(response)

bot = Bot()
bot.run()

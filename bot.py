#████████╗██╗    ██╗██╗████████╗ ██████╗██╗  ██╗     ██████╗██╗  ██╗ █████╗ ████████╗██████╗  ██████╗ ████████╗
#╚══██╔══╝██║    ██║██║╚══██╔══╝██╔════╝██║  ██║    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝
#   ██║   ██║ █╗ ██║██║   ██║   ██║     ███████║    ██║     ███████║███████║   ██║   ██████╔╝██║   ██║   ██║   
#   ██║   ██║███╗██║██║   ██║   ██║     ██╔══██║    ██║     ██╔══██║██╔══██║   ██║   ██╔══██╗██║   ██║   ██║   
#   ██║   ╚███╔███╔╝██║   ██║   ╚██████╗██║  ██║    ╚██████╗██║  ██║██║  ██║   ██║   ██████╔╝╚██████╔╝   ██║   
#   ╚═╝    ╚══╝╚══╝ ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝  ╚═════╝    ╚═╝                                                                                                             

import yaml
from twitchio.ext import commands
import datetime
from random import randint
import requests

from commands import Commands

#Reads auth data
def read_auth():
    with open('config/auth.yml') as f_auth:
        data = yaml.load(f_auth, Loader=yaml.FullLoader)
        bot_username = data.get('bot-name')
        irc_token = data.get('auth-id')
        client_id = data.get('client-id')
        cmd_prefix = data.get('cmd-prefix')
        channel = data.get('channel')
    return (bot_username, irc_token, client_id, cmd_prefix, channel)

#Reads config
def read_config():
    with open('config/broadcasts.yml') as f_broadcasts:
        data = yaml.load(f_broadcasts, Loader=yaml.FullLoader)
        broadcasts = data.get('broadcasts')
    return broadcasts

config_data = read_config() #config_data = broadcasts
broadcasts = config_data

# Main Twitch Bot Class
class Bot(commands.Bot):
    cmds_on_cooldown = dict()
    n_current = 0
    def __init__(self):
        self.auth_data = read_auth() #auth_data = (bot_username, irc_token, client_id, cmd_prefix, channel)
        self.bot_username = self.auth_data[0]
        self.irc_token = self.auth_data[1]
        self.client_id = self.auth_data[2]
        self.cmd_prefix = self.auth_data[3]
        self.channel = self.auth_data[4]

        super().__init__(
            nick = self.bot_username,
            irc_token = self.irc_token,
            client_id = self.client_id,
            prefix = self.cmd_prefix,
            initial_channels = [self.channel]
        )

        self.bot_commands = Commands('config/commands.yml', self.cmd_prefix)

    # On bot startup
    async def event_ready(self):
        print(f'\nBot: {self.bot_username}')
        print(f'Channel: {self.channel}')
        print('Connected!\n')
        ws = bot._ws
        await ws.send_privmsg(self.channel, f"/me is online")

    # Everytime a message is sent in the channel
    async def event_message(self, message):
        if message.author.name == self.bot_username: return # ignores itself
        await self.bot_commands.handler(message, await self.get_context(message))
        await self.handle_commands(message)
        await self.handle_broadcast(message)


#  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗     ██╗  ██╗ █████╗ ███╗   ██╗██████╗ ██╗     ███████╗██████╗
# ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗    ██║  ██║██╔══██╗████╗  ██║██╔══██╗██║     ██╔════╝██╔══██╗
# ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║    ███████║███████║██╔██╗ ██║██║  ██║██║     █████╗  ██████╔╝
# ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║    ██╔══██║██╔══██║██║╚██╗██║██║  ██║██║     ██╔══╝  ██╔══██╗
# ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝    ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗███████╗██║  ██║
#  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝

    # @commands.command(name='commands', aliases={'cmds'})
    # async def cmd_list_commands(self, ctx):
    #     cmd_label_list = simple_cmds.keys()
    #     cmd_list = ', !'.join(cmd_label_list) + ', !shoutout, !so, !timeout, !vanish'
    #     response = '/me !' + cmd_list
    #     await ctx.send(response)

    @commands.command(name='shoutout', aliases={'so'})
    async def cmd_shoutout(self, ctx):
        msg = ctx.content.split()
        user_roles = self.get_roles(ctx.author)
        cmd_roles = ['mod', 'broadcaster']
        mixed = set(cmd_roles) & set(user_roles)
        if not mixed: return
        if len(msg) != 2: return
        who = msg[1][1:] if msg[1].startswith('@') else msg[1]
        print(f'Shouting out: {who}')
        response = f'/me BOOBA go --> https://www.twitch.tv/{who} <-- or i ziggs ult you . . . (in game)'
        await ctx.send(response)

    def get_roles(self, user):
        roles = []
        badges = user._badges
        if 'broadcaster' in badges: roles.append('broadcaster')
        if 'moderator' in badges: roles.append('mod')
        if 'vip' in badges: roles.append('vip')
        if 'subscriber' in badges: roles.append('sub')
        roles.append('pleb')
        return roles

    # @commands.command(name='timeout')
    # async def cmd_timeout(self, ctx):
    #     username = ctx.author.name
    #     time = 5
    #     reason = 'u timed urself out'
    #     print(f'Self timing out: {username}')
    #     await ctx.send(f'/me bye bye @{username}!!!')
    #     await ctx.timeout(user=username, duration=time, reason=reason)

    # @commands.command(name='vanish')
    # async def cmd_vanish(self, ctx):
    #     username = ctx.author.name
    #     time = 1
    #     reason = 'Clearing your chat messages'
    #     print(f'Vanishing: {username}')
    #     await ctx.timeout(user=username, duration=time, reason=reason)

# ██████╗ ██████╗  ██████╗  █████╗ ██████╗  ██████╗ █████╗ ███████╗████████╗    ██╗  ██╗ █████╗ ███╗   ██╗██████╗ ██╗     ███████╗██████╗
# ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝    ██║  ██║██╔══██╗████╗  ██║██╔══██╗██║     ██╔════╝██╔══██╗
# ██████╔╝██████╔╝██║   ██║███████║██║  ██║██║     ███████║███████╗   ██║       ███████║███████║██╔██╗ ██║██║  ██║██║     █████╗  ██████╔╝
# ██╔══██╗██╔══██╗██║   ██║██╔══██║██║  ██║██║     ██╔══██║╚════██║   ██║       ██╔══██║██╔══██║██║╚██╗██║██║  ██║██║     ██╔══╝  ██╔══██╗
# ██████╔╝██║  ██║╚██████╔╝██║  ██║██████╔╝╚██████╗██║  ██║███████║   ██║       ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗███████╗██║  ██║
# ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝       ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝

    async def handle_broadcast(self, message):
        if message.author.name == 'roseiol': return
        msg = message.content.split(" ") 
        if message.content[0] == "!": return
        if randint(1,15) == 3:
            ws = bot._ws
            await ws.send_privmsg(self.channel, f'/me {broadcasts[self.n_current]}')
            if self.n_current >= (len(broadcasts)-1): self.n_current = 0
            else: self.n_current +=1
        return

bot = Bot()
bot.run()

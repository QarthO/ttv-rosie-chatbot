# ██████╗  ██████╗ ███████╗██████╗  ██████╗ ████████╗
# ██╔══██╗██╔═══██╗██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
# ██████╔╝██║   ██║███████╗██████╔╝██║   ██║   ██║   
# ██╔══██╗██║   ██║╚════██║██╔══██╗██║   ██║   ██║   
# ██║  ██║╚██████╔╝███████║██████╔╝╚██████╔╝   ██║   
# ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═════╝  ╚═════╝    ╚═╝                                                    

import yaml
from twitchio.ext import commands
import datetime
from random import randint

irc_token = ''
client_id = ''
bot_nick = ''
command_prefix = '!'
channel = ''

cmds = ''
broadcasts = ''
listeners = ''

# Reads config files
with open('auth.yml') as f_auth, open('commands.yml') as f_commands, open('broadcasts.yml') as f_broadcasts, open('listeners.yml') as f_listeners:
    data = yaml.load(f_auth, Loader=yaml.FullLoader)
    irc_token = data.get('auth-id')
    client_id = data.get('client-id')
    bot_nick = data.get('bot-name')
    command_prefix = data.get('cmd-prefix')
    channel = data.get('channel')
    data = yaml.load(f_commands, Loader=yaml.FullLoader)
    cmds = data.get('commands')
    data = yaml.load(f_broadcasts, Loader=yaml.FullLoader)
    broadcasts = data.get('broadcasts')
    data = yaml.load(f_listeners, Loader=yaml.FullLoader)
    listeners = data.get('listeners')

# Main Twitch Bot Class
class Bot(commands.Bot):

    cmds_on_cooldown = dict()
    n_current = 0
    time_last_broadcast = ''

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
        print(f'\nBot: {bot_nick}')
        print(f'Channel: {channel}')
        print('Connected!\n')
        ws = bot._ws
        await ws.send_privmsg(channel, f"/me is online")

    # Everytime a message is sent in the channel
    async def event_message(self, message):
        if message.author.name == 'roseiol': return
        await self.handle_commands(message)
        await self.handle_broadcast(message)
        await self.handle_listener(message)

    

#  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗     ██╗  ██╗ █████╗ ███╗   ██╗██████╗ ██╗     ███████╗██████╗ 
# ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗    ██║  ██║██╔══██╗████╗  ██║██╔══██╗██║     ██╔════╝██╔══██╗
# ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║    ███████║███████║██╔██╗ ██║██║  ██║██║     █████╗  ██████╔╝
# ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║    ██╔══██║██╔══██║██║╚██╗██║██║  ██║██║     ██╔══╝  ██╔══██╗
# ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝    ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗███████╗██║  ██║
#  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
                                                                                                                                                                                                                                                                
    @commands.command(name='commands', aliases={'cmds'})
    async def cmd_list_commands(self, ctx):
        cmd_label_list = cmds.keys()
        response = '/me !' + ', !'.join(cmd_label_list + ', !shoutout, !so, !timeout, !vanish')
        await ctx.send(response)

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
        cmd_label = ctx.content[1:]
        cmd = cmds.get(cmd_label)
        if not self.check_roles(cmd_label, ctx.author): return
        if not self.check_cooldown(cmd_label):
            response = cmd.get('response')
            cooldown = cmd.get('cooldown')
            available_time = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
            self.cmds_on_cooldown[cmd_label] = available_time
            await ctx.send(f'/me {response}')
        self.check_roles(cmd_label, ctx.author)
    
    def check_cooldown(self, cmd_label):
        if cmd_label in self.cmds_on_cooldown.keys():
            available_time = self.cmds_on_cooldown.get(cmd_label)
            if datetime.datetime.now() > available_time:
                del self.cmds_on_cooldown[cmd_label]
                return False
            return True
        return False

    def check_roles(self, cmd_label, user):
        cmd = cmds.get(cmd_label)
        cmd_roles = cmd.get('roles')
        user_roles = self.get_roles(user)
        mixed = set(cmd_roles) & set(self.get_roles(user))
        return True if mixed else False

    def get_roles(self, user):
        roles = []
        badges = user._badges
        if 'broadcaster' in badges: roles.append('broadcaster')
        if 'moderator' in badges: roles.append('mod')
        if 'vip' in badges: roles.append('vip')
        if 'subscriber' in badges: roles.append('sub')
        roles.append('pleb')
        return roles

# ██████╗ ██████╗  ██████╗  █████╗ ██████╗  ██████╗ █████╗ ███████╗████████╗    ██╗  ██╗ █████╗ ███╗   ██╗██████╗ ██╗     ███████╗██████╗ 
# ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝    ██║  ██║██╔══██╗████╗  ██║██╔══██╗██║     ██╔════╝██╔══██╗
# ██████╔╝██████╔╝██║   ██║███████║██║  ██║██║     ███████║███████╗   ██║       ███████║███████║██╔██╗ ██║██║  ██║██║     █████╗  ██████╔╝
# ██╔══██╗██╔══██╗██║   ██║██╔══██║██║  ██║██║     ██╔══██║╚════██║   ██║       ██╔══██║██╔══██║██║╚██╗██║██║  ██║██║     ██╔══╝  ██╔══██╗
# ██████╔╝██║  ██║╚██████╔╝██║  ██║██████╔╝╚██████╗██║  ██║███████║   ██║       ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗███████╗██║  ██║
# ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝       ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝

    async def handle_broadcast(self, message):
        if message.author.name == 'roseiol': return
        if randint(1,10) == 3:
            ws = bot._ws
            await ws.send_privmsg(channel, f'/me {broadcasts[self.n_current]}')
            if self.n_current >= (len(broadcasts)-1): self.n_current = 0 
            else: self.n_current +=1
        return

# ██╗     ██╗███████╗████████╗███████╗███╗   ██╗███████╗██████╗     ██╗  ██╗ █████╗ ███╗   ██╗██████╗ ██╗     ███████╗██████╗ 
# ██║     ██║██╔════╝╚══██╔══╝██╔════╝████╗  ██║██╔════╝██╔══██╗    ██║  ██║██╔══██╗████╗  ██║██╔══██╗██║     ██╔════╝██╔══██╗
# ██║     ██║███████╗   ██║   █████╗  ██╔██╗ ██║█████╗  ██████╔╝    ███████║███████║██╔██╗ ██║██║  ██║██║     █████╗  ██████╔╝
# ██║     ██║╚════██║   ██║   ██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗    ██╔══██║██╔══██║██║╚██╗██║██║  ██║██║     ██╔══╝  ██╔══██╗
# ███████╗██║███████║   ██║   ███████╗██║ ╚████║███████╗██║  ██║    ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗███████╗██║  ██║
# ╚══════╝╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝                                                                                                                            

    async def handle_listener(self, message):
        msg = message.content
        for trigger in listeners.keys():
            if str(trigger) in msg.lower().split(' '):
                response = listeners.get(trigger)
                ws = bot._ws
                await ws.send_privmsg(channel, f'/me {response}')
                return
        return

        
bot = Bot()
bot.run()


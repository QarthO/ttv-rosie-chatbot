import yaml
from twitchio.ext import commands
import datetime

irc_token = ''
client_id = ''
bot_nick = 'roseiol'
command_prefix = '!'
channel = 'roselol'

cmds = ''

with open('auth.yml') as f_auth, open('commands.yml') as f_commands:
    data = yaml.load(f_auth, Loader=yaml.FullLoader)
    irc_token = data.get('auth-id')
    client_id = data.get('client-id')
    data = yaml.load(f_commands, Loader=yaml.FullLoader)
    cmds = data.get('commands')
    
class Bot(commands.Bot):

    cmds_on_cooldown = dict()

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



bot = Bot()
bot.run()

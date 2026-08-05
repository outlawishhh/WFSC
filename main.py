import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import aiohttp

TOKEN = ""
WELCOME_CHANNEL_ID = 
ADMIN_ID = 
INTRO_CHANNEL_ID = 
RULES_CHANNEL_ID = 
BACKGROUND_URL = "https://raw.githubusercontent.com/outlawishhh/WFSC/refs/heads/main/image.png"

AVATAR_X = 412
AVATAR_Y = 270
TEXT_Y = 500
FONT_SIZE = 60

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="w", intents=intents)

activities = [
    discord.Activity(type=discord.ActivityType.watching, name="Watching over the AISC server"),
    discord.Activity(type=discord.ActivityType.playing, name="Welcoming new people")
]
current_activity = 0

@tasks.loop(seconds=10)
async def rotate_activity():
    global current_activity
    await bot.change_presence(activity=activities[current_activity])
    current_activity = (current_activity + 1) % len(activities)

def load_font(size):
    font_paths = [
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",  # Termux
        "arial.ttf",  # Windows
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    try:
        return ImageFont.load_default(size=size)
    except:
        return ImageFont.load_default()

async def create_welcome_card(member: discord.Member):
    async with aiohttp.ClientSession() as session:
        async with session.get(BACKGROUND_URL) as resp:
            background = Image.open(BytesIO(await resp.read()))
        
        async with session.get(str(member.display_avatar.with_size(256).with_format("png"))) as resp:
            avatar = Image.open(BytesIO(await resp.read())).resize((200, 200))
    
    mask = Image.new("L", (200, 200), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 200, 200), fill=255)
    
    avatar_with_border = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
    draw_border = ImageDraw.Draw(avatar_with_border)
    draw_border.ellipse((0, 0, 210, 210), fill=(255, 255, 255, 255))
    avatar_with_border.paste(avatar, (5, 5), mask)
    
    background = background.convert("RGBA")
    background.paste(avatar_with_border, (AVATAR_X, AVATAR_Y), avatar_with_border)
    
    draw = ImageDraw.Draw(background)
    font = load_font(FONT_SIZE)
    
    text = member.name
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (1024 - text_width) // 2
    draw.text((text_x, TEXT_Y), text, fill=(255, 255, 255), font=font)
    
    buffer = BytesIO()
    background.save(buffer, "PNG")
    buffer.seek(0)
    return buffer

@bot.event
async def on_ready():
    print(f'> Logged in as {bot.user}')
    rotate_activity.start()

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return
    
    card = await create_welcome_card(member)
    await channel.send(file=discord.File(card, "welcome.png"))
    
    message = (
        f"Welcome to the **official AISC server** {member.mention}! 🎉\n\n"
        "Please verify to access all channels.\n"
        f"Please introduce yourself in <#{INTRO_CHANNEL_ID}> (access will be granted after verification) and check out ⁠<id:customize> to get more roles.\n"
        f"Feel free to DM <@{ADMIN_ID}> for any queries.\n"
        f"Please remember this is a SFW community. Make sure to review our ⁠<#{RULES_CHANNEL_ID}>.\n\n"
        "Enjoy your stay here, and Keep AISC-ing! 🚀"
    )
    
    await channel.send(message)

@bot.command(name="test")
async def test(ctx):
    if ctx.author.id != ADMIN_ID:
        await ctx.send('❓ Error 404: dont even try bro')
        return
    
    card = await create_welcome_card(ctx.author)
    await ctx.send(file=discord.File(card, "welcome.png"))
    message = (
        f"Welcome to the **AISC server** {ctx.author.mention}! 🎉\n\n"
        "Please verify to access all channels.\n"
        f"Please introduce yourself in <#{INTRO_CHANNEL_ID}> (access will be granted after verification) and check out ⁠<id:customize> to get more roles.\n"
        f"Feel free to DM <@{ADMIN_ID}> for any queries.\n"
        f"Please remember this is a SFW community. Make sure to review our ⁠<#{RULES_CHANNEL_ID}>.\n\n"
        "Enjoy your stay here, and Keep AISC-ing! 🚀"
    )
    
    await ctx.send(message)

if __name__ == "__main__":
    bot.run(TOKEN)

# automated message on join (image + msg)
# wtest = test

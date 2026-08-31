import discord
from discord.ext import commands
from config import token  # Import the bot's token from configuration file
import re

intents = discord.Intents.default()
intents.members = True  # Allows the bot to work with users and ban them
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Regex untuk mendeteksi link iklan discord invite atau URL umum
LINK_IKLAN_REGEX = re.compile(
    r'(discord\.gg/|discord\.com/invite/|https?://[^\s]+)', 
    re.IGNORECASE
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# ================= TAMBAHAN FITUR AUTOMOD =================
@bot.event
async def on_message(message):
    # Mengabaikan pesan dari bot itu sendiri agar tidak terjadi loop
    if message.author.bot:
        return

    # 1. DETEKSI PESAN SUARA (VOICE MESSAGE)
    if message.flags.voice:
        try:
            # Mengirim peringatan ke chat sebelum memblokir
            await message.channel.send(f"⚠️ {message.author.mention} telah diblokir karena mengirim pesan suara.")
            # Melakukan Ban Otomatis
            await message.author.ban(reason="Automod: Mengirim pesan suara di ruang obrolan teks.")
            return # Keluar dari fungsi agar tidak mengecek iklan lagi
        except discord.Forbidden:
            await message.channel.send("❌ Gagal memblokir pengguna. Periksa posisi role atau izin bot Anda.")
        except discord.HTTPException:
            pass

    # 2. DETEKSI IKLAN / TAUTAN (LINK)
    if LINK_IKLAN_REGEX.search(message.content):
        try:
            # Hapus pesan iklan terlebih dahulu agar tidak dilihat member lain
            await message.delete()
            # Beri tahu di chat
            await message.channel.send(f"⚠️ {message.author.mention} telah diblokir karena mengirim tautan iklan.")
            # Melakukan Ban Otomatis
            await message.author.ban(reason="Automod: Mengirim link iklan/tautan terlarang.")
            return # Keluar dari fungsi
        except discord.Forbidden:
            await message.channel.send("❌ Gagal menghapus pesan atau memproses ban. Periksa izin bot Anda.")
        except discord.HTTPException:
            pass

    # WAJIB: Memastikan command teks (!start, !ban) di bawah ini tetap berfungsi
    await bot.process_commands(message)
# ==========================================================

@bot.command()
async def start(ctx):
    await ctx.send("Hi! I'm a chat manager bot!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("It is not possible to ban a user with equal or higher rank!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"User {member.name} was banned.")
    else:
        await ctx.send("This command should point to the user you want to ban. For example: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have sufficient permissions to execute this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found.")

bot.run(token)

import discord  # Mengimpor pustaka Discord agar dapat bekerja dengan API Discord
from discord.ext import commands  # Mengimpor modul perintah dari discord.ext untuk membuat perintah bot
from config import token  # Impor token bot dari file konfigurasi

intents = discord.Intents.default()  # Membuat objek maksud untuk menentukan maksud bot
intents.members = True  # Mengatur bendera yang memungkinkan bot untuk bekerja dengan pengguna dan melarang mereka
intents.message_content = True  # Mengatur bendera yang memungkinkan bot bekerja dengan isi pesan

bot = commands.Bot(command_prefix='!', intents=intents)  # Buat instance bot dengan awalan perintah "!" dan berikan objek intents ke bot tersebut

@bot.event  # Menentukan peristiwa yang akan dipicu setiap kali bot berhasil diluncurkan
async def on_ready():
    print(f'Masuk sebagai {bot.user.name}')  # Menampilkan pesan di konsol tentang keberhasilan masuk ke Discord

@bot.command()  # Tentukan perintah "start" yang akan dipanggil setiap kali pengguna memasukkan "!start"
async def start(ctx):
    await ctx.send("Hai! saya adalah Bot manajer!")  # Mengirim pesan kembali ke ruang obrolan

@bot.command()  # Mendefinisikan perintah "ban" yang mengharuskan pengguna untuk memiliki hak pelarangan
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:  # Memeriksa apakah perintah tersebut menentukan pengguna yang harus diblokir
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Tidak mungkin untuk memblokir pengguna dengan peringkat yang sama atau lebih tinggi!")
        else:
            await ctx.guild.ban(member)  # Melarang pengguna dari server
            await ctx.send(f"Pengguna {member.name} dilarang.")  # Mengirim pesan tentang pemblokiran yang berhasil
    else:
        await ctx.send("Perintah ini harus mengarah ke pengguna yang ingin Anda blokir. Sebagai contoh: `!ban @user`")

@ban.error  # Tentukan handler kesalahan untuk perintah "ban"
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Kalian tidak memiliki izin yang cukup untuk menjalankan perintah ini.")  # Mengirim pesan yang menginformasikan pengguna tentang kesalahan hak akses
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Pengguna tidak ditemukan.")  # Mengirim pesan kesalahan jika pengguna yang ditentukan tidak ditemukan

bot.run(token)  # Meluncurkan bot, menggunakan token untuk autentikasi

# Discord Key Bot V2
# Requiere: pip install -U discord.py

import discord, json, os
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

TOKEN="MTUxMDE2NDU2Mzg2ODM4NTMwMA.G6_9ee.oA2z9j4yM9611Yip0qKAIbpbQtvtDcv4LPOFv4"
OWNER_ID=753059936916865095

IOS_VIDEO="https://youtu.be/gnOnVJ9U7iI"
IOS_WEB="https://freeproxy.drakonett.store/"
PC_VIDEO="https://youtu.be/7gicOGdgvQw"
PC_WEB="https://discord.gg/fwERC5umyR"

CLAIMS="claims.json"
ADMINS="admins.json"
BANNER="banner.json"

intents=discord.Intents.default()
bot=commands.Bot(command_prefix="!",intents=intents)

def load(path,default):
    if not os.path.exists(path):
        return default
    with open(path,"r",encoding="utf8") as f:
        return json.load(f)

def save(path,data):
    with open(path,"w",encoding="utf8") as f:
        json.dump(data,f,indent=4)

def is_admin(uid):
    admins=load(ADMINS,[])
    return uid==OWNER_ID or uid in admins

def pop_key(file):
    if not os.path.exists(file): return None
    with open(file,"r",encoding="utf8") as f:
        data=[x.strip() for x in f if x.strip()]
    if not data: return None
    key=data.pop(0)
    with open(file,"w",encoding="utf8") as f:
        f.write("\n".join(data))
    return key

class ClaimView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def claim(self,interaction,kind):
        claims=load(CLAIMS,{})

        uid=str(interaction.user.id)

        if uid in claims:
            last=datetime.fromisoformat(claims[uid])
            remain=timedelta(days=7)-(datetime.utcnow()-last)
            if remain.total_seconds()>0:
                await interaction.response.send_message(
                    f"Debes esperar {remain.days} días.",
                    ephemeral=True
                )
                return

        if kind=="ios":
            key=pop_key("keys.txt")
            video=IOS_VIDEO
            web=IOS_WEB
            product="iOS Proxy 1D"
        else:
            key=pop_key("keysv2.txt")
            video=PC_VIDEO
            web=PC_WEB
            product="Panel PC 1D"

        if not key:
            await interaction.response.send_message("Sin stock.",ephemeral=True)
            return

        claims[uid]=datetime.utcnow().isoformat()
        save(CLAIMS,claims)

        embed=discord.Embed(title="🎁 Key Reclamada",color=0xff0000)
        embed.add_field(name="Producto",value=product,inline=False)
        embed.add_field(name="Key",value=f"`{key}`",inline=False)
        embed.add_field(name="Video",value=video,inline=False)
        embed.add_field(name="Activación",value=web,inline=False)
        embed.set_footer(text="Copyright © Drako.NET")

        await interaction.user.send(embed=embed)
        await interaction.response.send_message("Revisa tus DMs.",ephemeral=True)

    @discord.ui.button(
    label="🍏 iOS Proxy 1D",
    style=discord.ButtonStyle.success,
    custom_id="claim_ios"
)
    async def ios(self,i,b):
        await self.claim(i,"ios")

    @discord.ui.button(
    label="🖥️ Panel PC 1D",
    style=discord.ButtonStyle.primary,
    custom_id="claim_pc"
)
    async def pc(self,i,b):
        await self.claim(i,"pc")

@bot.event
async def on_ready():
    bot.add_view(ClaimView())
    await bot.tree.sync()
    print("Ready")

@bot.tree.command(name="panel")
async def panel(interaction:discord.Interaction):
    if not is_admin(interaction.user.id):
        return await interaction.response.send_message("Sin permisos.",ephemeral=True)

    e = discord.Embed(
    title="🎁 Reclama tu Key",
    description=(
        "🚀 **Acceso Gratuito a Nuestros Productos Premium**\n\n"
        "Reclama una licencia de prueba de 1 día para conocer nuestros servicios.\n\n"
        "📦 Productos disponibles:\n"
        "🍏 iOS Proxy 1D\n"
        "🖥️ Panel PC 1D\n\n"
        "📋 Condiciones:\n"
        "• 1 licencia gratuita por usuario cada 7 días.\n"
        "• Entrega automática mediante mensaje privado.\n"
        "• Incluye guía de instalación y enlace de activación.\n"
        "• Las licencias están sujetas a disponibilidad de stock.\n\n"
        "Selecciona uno de los botones inferiores para comenzar."
    ),
    color=0xff0000
)
    banner=load(BANNER,{"url":""})
    if banner.get("url"):
        e.set_image(url=banner["url"])
    e.set_footer(text="Copyright © Drako.NET")
    await interaction.channel.send(embed=e,view=ClaimView())
    await interaction.response.send_message("Panel enviado.",ephemeral=True)


BANNER="banner.json"

@bot.tree.command(name="setbanner")
async def setbanner(interaction:discord.Interaction,url:str):
    if not is_admin(interaction.user.id):
        return await interaction.response.send_message("Sin permisos.",ephemeral=True)
    save(BANNER,{"url":url})
    await interaction.response.send_message("Banner actualizado.",ephemeral=True)

@bot.tree.command(name="addkey")
async def addkey(interaction:discord.Interaction,tipo:str,key:str):
    if not is_admin(interaction.user.id):
        return await interaction.response.send_message("Sin permisos.",ephemeral=True)
    archivo="keys.txt" if tipo.lower()=="ios" else "keysv2.txt"
    with open(archivo,"a",encoding="utf8") as f:
        f.write(key+"\n")
    await interaction.response.send_message("Key agregada.",ephemeral=True)

@bot.tree.command(name="addkeys")
async def addkeys(interaction:discord.Interaction,tipo:str,keys:str):
    if not is_admin(interaction.user.id):
        return await interaction.response.send_message("Sin permisos.",ephemeral=True)

    if tipo.lower()=="ios":
        archivo="keys.txt"
    elif tipo.lower()=="pc":
        archivo="keysv2.txt"
    else:
        return await interaction.response.send_message("Usa ios o pc.",ephemeral=True)

    lista=[x.strip() for x in keys.split("\n") if x.strip()]
    with open(archivo,"a",encoding="utf8") as f:
        for k in lista:
            f.write(k+"\n")

    await interaction.response.send_message(f"Se agregaron {len(lista)} keys.",ephemeral=True)

@bot.tree.command(name="stock")
async def stock(interaction:discord.Interaction):
    ios=sum(1 for _ in open("keys.txt",encoding="utf8")) if os.path.exists("keys.txt") else 0
    pc=sum(1 for _ in open("keysv2.txt",encoding="utf8")) if os.path.exists("keysv2.txt") else 0
    await interaction.response.send_message(f"iOS: {ios}\nPC: {pc}",ephemeral=True)

@bot.tree.command(name="addadmin")
async def addadmin(interaction:discord.Interaction,user:discord.Member):
    if interaction.user.id!=OWNER_ID:
        return await interaction.response.send_message("Solo owner.",ephemeral=True)

    admins=load(ADMINS,[])
    if user.id not in admins:
        admins.append(user.id)
    save(ADMINS,admins)
    await interaction.response.send_message("Admin agregado.",ephemeral=True)

@bot.tree.command(name="removeadmin")
async def removeadmin(interaction:discord.Interaction,user:discord.Member):
    if interaction.user.id!=OWNER_ID:
        return
    admins=load(ADMINS,[])
    if user.id in admins:
        admins.remove(user.id)
    save(ADMINS,admins)
    await interaction.response.send_message("Admin eliminado.",ephemeral=True)

@bot.tree.command(name="resetuser")
async def resetuser(interaction:discord.Interaction,user:discord.Member):
    if not is_admin(interaction.user.id):
        return
    claims=load(CLAIMS,{})
    claims.pop(str(user.id),None)
    save(CLAIMS,claims)
    await interaction.response.send_message("Cooldown reiniciado.",ephemeral=True)

bot.run(TOKEN)

import discord
from discord import ui
from discord.ext import commands
from discord import app_commands
import os
import random
import backpack #This is another file in the project and a resource for the bot
Puan = 0
Vakit = 0
gkat= 1
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık!')

@bot.command()
async def yardim(ctx):
    await ctx.send(f'# KOMUTLAR:\n- "yardim": Komut listesini gösterir. \n- "help": Komut listesini İngilizce gösterir. \n- "bilgi": İklim değişikliği hakkında rastgele bilgi verir. \n- "oyun": İklim değişikliği ödevi oyununu açar.')

@bot.command()
async def help(ctx):
    await ctx.send(f'# COMMANDS:\n- "yardim": Shows command list in Turkish. \n- "help": Shows command list. \n- "bilgi": Provides random information about climate change in Turkish. \n- "oyun": Opens the Climate Change Homework Game in Turkish.')
@bot.command()
async def bilgi(ctx):
    await ctx.send(random.choice(backpack.Bilgiler))


class startView(ui.View):
    @ui.button(label="Tamam.", style=discord.ButtonStyle.green, emoji="✅")
    async def tamam(self, interaction: discord.Interaction, button: ui.Button):
        start_embed = discord.Embed(
            title="1. adım; araştırma",
            description="ne kadar araştırma yapacağını seç",
            color=0x00ff00
        )

        await interaction.response.edit_message(          
            embed=start_embed,
            view=view2()                          
        )        



class view2(ui.View):
    
    @ui.button(label="Yarım saat", style=discord.ButtonStyle.grey, emoji="🕒")
    async def yarim_saat(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_saat(interaction, kat=0.5, vakit_degisim = -1 )

    @ui.button(label="1 saat", style=discord.ButtonStyle.gray, emoji="🕒")
    async def bir_saat(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_saat(interaction, kat=1, vakit_degisim=-2)

    @ui.button(label="2 saat", style=discord.ButtonStyle.grey, emoji="🕒")
    async def iki_saat(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_saat(interaction, kat=2, vakit_degisim=-4)

    @ui.button(label="3 saat", style=discord.ButtonStyle.danger, emoji="🕒")
    async def uc_saat(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_saat(interaction, kat=3, vakit_degisim=-6)

   
    async def isle_saat(self, interaction: discord.Interaction, kat: float, vakit_degisim: int):
        global Vakit
        global gkat
        gkat = kat                     
        Vakit = Vakit + vakit_degisim   
        saatEmbed=discord.Embed(
            title="2. adım; sayfa sayısı",
            description="kaç sayfa kullanacağını seç, daha fazla sayfa = daha fazla vakit"
        )    
        await interaction.response.edit_message(         
            embed=saatEmbed,
            view = view3()                         
        )
class view3(ui.View):
    @ui.button(label="1 sayfa", style=discord.ButtonStyle.gray, emoji="📄")
    async def sayfa1(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_sayfa(interaction, puan_degisim= 5, vakit_degisim = -3 )
    
    @ui.button(label="2 sayfa", style=discord.ButtonStyle.danger, emoji="📄")
    async def sayfa2(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_sayfa(interaction, puan_degisim= 10, vakit_degisim = -6 )
    
    @ui.button(label="3 sayfa", style=discord.ButtonStyle.blurple, emoji="📄")
    async def sayfa3(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_sayfa(interaction, puan_degisim= 25, vakit_degisim = -8 )

    async def isle_sayfa(self, interaction: discord.Interaction, puan_degisim: int, vakit_degisim: int):
        
        global Puan
        global Vakit
        Vakit = Vakit + vakit_degisim
        Puan =Puan + puan_degisim 
          
        sayfaEmbed=discord.Embed(
            title="3. adım; yazı güzelliği",
            description="yazın okunursa daha fazla puan alırsın ama güzel yazmak zaman gerektirir"
        )    
        await interaction.response.edit_message(          
            embed=sayfaEmbed,
            view = view4()                         
        )
class view4(ui.View):
    @ui.button(label="Güzel", style=discord.ButtonStyle.gray, emoji="⏫")
    async def good(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_yg(interaction, puan_degisim= 25, vakit_degisim = -5 )
    
    @ui.button(label="Orta", style=discord.ButtonStyle.gray, emoji="🔼")
    async def med(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_yg(interaction, puan_degisim= 5, vakit_degisim = -2 )
    
    @ui.button(label="Kötü", style=discord.ButtonStyle.grey, emoji="🔽")
    async def bad(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_yg(interaction, puan_degisim= -5, vakit_degisim = 1 )
    

    async def isle_yg(self, interaction: discord.Interaction, puan_degisim: int, vakit_degisim: int):
        global Puan, Vakit
        
        Vakit += vakit_degisim
        Puan = Puan + puan_degisim 

        if Vakit <= 0:
            await show_sonuc(interaction)
            return  

        ygEmbed = discord.Embed(
            title="4. adım; renk sayısı",
            description="kaç farklı renk kullanacağını seç, daha fazla renk ödevin güzelliğini arttırır.",
            color=0x00ff00
        )
        
        await interaction.response.edit_message(embed=ygEmbed, view=view5())
   
        

class view5(ui.View):
    @ui.button(label="3 renk", style=discord.ButtonStyle.grey, emoji="🔴")
    async def renk3(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_rs(interaction, puan_degisim= 5, vakit_degisim = -1 )
    
    @ui.button(label="5 renk", style=discord.ButtonStyle.red, emoji="🟢")
    async def renk5(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_rs(interaction, puan_degisim= 10, vakit_degisim = -1 )
    
    @ui.button(label="7 renk", style=discord.ButtonStyle.blurple, emoji="🟣")
    async def renk7(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_rs(interaction, puan_degisim= 15, vakit_degisim = -2 )
    

    async def isle_rs(self, interaction: discord.Interaction, puan_degisim: int, vakit_degisim: int):
        global Puan, Vakit
        
        Vakit += vakit_degisim
        Puan = Puan + puan_degisim

        if Vakit <= 0:
            await show_sonuc(interaction)
            return

        rsEmbed = discord.Embed(
            title="5. adım; görsel sayısı",
            description="kaç tane görsel kullanacağını seç, daha fazla görsel ödevin kalitesini arttırır (bir yere kadar).",
            color=0x00ff00
        )
        
        await interaction.response.edit_message(embed=rsEmbed, view=view6())

class view6(ui.View):
    @ui.button(label="1 görsel", style=discord.ButtonStyle.grey, emoji="📷")
    async def foto1(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_gs(interaction, puan_degisim= 5, vakit_degisim = -1 )
    
    @ui.button(label="2 görsel", style=discord.ButtonStyle.gray, emoji="📷")
    async def foto2(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_gs(interaction, puan_degisim= 8, vakit_degisim = -1 )
    
    @ui.button(label="3 görsel", style=discord.ButtonStyle.green, emoji="📷")
    async def foto3(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_gs(interaction, puan_degisim= 10, vakit_degisim = -2 )

    @ui.button(label="4 görsel", style=discord.ButtonStyle.gray, emoji="📷")
    async def foto4(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_gs(interaction, puan_degisim= 15, vakit_degisim = -2 )
    
    @ui.button(label="5 görsel", style=discord.ButtonStyle.grey, emoji="📷")
    async def foto5(self, interaction: discord.Interaction, button: ui.Button):
        await self.isle_gs(interaction, puan_degisim= 14, vakit_degisim = -3 )
    

    async def isle_gs(self, interaction: discord.Interaction,  puan_degisim: int, vakit_degisim: int):
        global Puan, Vakit, gkat
        Vakit += vakit_degisim
        Puan = Puan + puan_degisim

        await show_sonuc(interaction)


async def show_sonuc(interaction: discord.Interaction):
    global Puan, gkat, final_puan
    final_puan = Puan * gkat
    if final_puan > 100:
        final_puan = 100
    sonEmbed = discord.Embed(
            title="🎯 SONUÇ",
            description=f"Vaktin doldu veya yapabileceğin ekleme kalmadı.\n\n"
                        f"**Toplam Puanın:** `{final_puan}`\n"
                        f"İklim değişikliği hakkında bilgi için **-bilgi** yazabilirsin")
    await interaction.response.edit_message(embed=sonEmbed, view=None)

    

        

@bot.command()
async def oyun(ctx):
    global Puan
    global Vakit
    Puan= 0
    Vakit= 20
    view = startView()
    embed = discord.Embed (title="Okulda Coğrafya'dan proje ödevialdın!(yaşasın!(iklim değişikliği ile ilgili tabi ki))" , description= "Ödevi tam puan alarak tamamlamaya çalış. Zaman unsurunu unutma.")
    await ctx.send(embed=embed, view=view)
bot.run(backpack.TOKEN1)

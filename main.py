#This code and description is written by Hoplin
#This code is written with API version 1.0.0(Rewirte-V)
#No matter to use it as non-commercial.

# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-
import discord
import asyncio
import os
from discord.ext import commands
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
from webserver import keep_alive


client = discord.Client() # Create Instance of Client. This Client is discord server's connection to Discord Room

# for lolplayersearch
tierScore = {
    'default' : 0,
    'iron' : 1,
    'bronze' : 2,
    'silver' : 3,
    'gold' : 4,
    'platinum' : 5,
    'diamond' : 6,
    'master' : 7,
    'grandmaster' : 8,
    'challenger' : 9
}
def tierCompare(solorank,flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2
warnings.filterwarnings(action='ignore')
bot = commands.Bot(command_prefix='.')

opggsummonersearch = 'https://www.op.gg/summoner/userName='


'''
Simple Introduction about asyncio
asyncio : Asynchronous I/O. It is a module for asynchronous programming and allows CPU operations to be handled in parallel with I/O.
async def (func name)(parameters): -> This type of asynchronous function or method is called Native Co-Rutine.
- await : you can use await keyword only in Native Co-Rutine
async def add(a,b):
    print("add {0} + {1}".format(a,b))
    await asyncio.sleep(1.0)
    return a + b
async def print_add(a,b):
    result = await add(a,b)
    print("print_add : {0} + {1} = {2}".format(a,b,result))
loop = asyncio.get_event_loop()
loop.run_until_complete(print_add(1,2))
loop.close()
'''



def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>','',str(htmls[a]),0).strip()
    return htmls

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    print("{0.user} LOL Bot Ready!".format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game("??? ?????? ??????"))


@bot.command()
async def test(ctx,arg):
    await ctx.send(arg)





#????????? ????????? ???????????????.

@client.event
async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)
    print(message.content)
    if message.author == client.user:
        return

    if message.content == ".help" or message.content == ".?????????":
        embed = discord.Embed(title="EMTRAY ?????? ???????????????!", description="??? ???????????? ???????????? ??? ????????? ?????? ???????????? ???????????? ????????????. ???????????? ?????? ????????? ?????? ???????????? `.help commands` ?????? `.????????? ?????????` ??? ??????????????????.", color=0x0285FF)
        embed.add_field(name="`?????????`",
                                value="`.???`  `.??????`  `.w`  `.?????????`", inline=False)
        embed.add_field(name="??? ????????????",
                                value="https://discord.com/api/oauth2/authorize?client_id=836446578301599815&permissions=8&scope=bot", inline=False)
        embed.add_field(name="EMTRAY ???????????? ??????",
                                value="https://discord.gg/ub8mf3hBaF", inline=False)
        embed.set_footer(text='EMTRAY BOT BY EMTRAY#0002',
                         icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/1385730/1a4d95bb4c09c9c8f1b421cdc2713c9a752cc8c1.gif')
        await message.channel.send("", embed=embed)

    if message.content == ".help commands" or message.content == ".????????? ?????????":
        embed = discord.Embed(title="EMTRAY ????????? ???????????? ?????? ???????????????.", description="", color=0x0285FF)
        embed.add_field(name="`.???`  `.??????`  `.w`",
                                value=".??? <????????? ??????> , .?????? <????????? ??????> ?????? .w <????????? ??????> ??? ????????? ?????????????????? ????????? ???????????? ??? ????????????!", inline=False)
        embed.add_field(name="`.?????????`",
                                value="????????? ????????? ?????? ??? ????????????!", inline=False)
        embed.set_footer(text='EMTRAY BOT BY EMTRAY#0002',
                         icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/1385730/1a4d95bb4c09c9c8f1b421cdc2713c9a752cc8c1.gif')
        await message.channel.send("", embed=embed)

    if message.content.startswith(".??????") or message.content.startswith(".???") or message.content.startswith(".w"):
        try:
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="????????? ????????? ??????????????????", description="", color=0x0285FF)
                embed.add_field(name="Please enter summoner name",
                                value=".??? <????????? ??????> ?????? .?????? <????????? ??????>", inline=False)
                embed.set_footer(text='EMTRAY BOT BY EMTRAY#0002',
                                 icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/1385730/1a4d95bb4c09c9c8f1b421cdc2713c9a752cc8c1.gif')
                await message.channel.send("", embed=embed)
            else:
                playerNickname = ''.join((message.content).split(' ')[1:])
                # Open URL
                checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
                bs = BeautifulSoup(checkURLBool, 'html.parser')

                # ???????????? ????????? ?????? '?image=q_auto&v=1'???????????????

                # Patch Note 20200503??????
                # Medal = bs.find('div', {'class': 'ContentWrap tabItems'}) ????????? ?????????????????????.
                # PC??? ????????? ?????? ?????? OS???????????? ????????? ContentWrap tabItems??? ??????????????? ?????????

                Medal = bs.find('div', {'class': 'SideContent'})
                RankMedal = Medal.findAll('img', {'src': re.compile('\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
                # Variable RankMedal's index 0 : Solo Rank
                # Variable RankMedal's index 1 : Flexible 5v5 rank

                # for mostUsedChampion
                mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})

                # ??????, ?????? ?????? ????????? ????????????????????? -> ????????? ????????? ????????? ??????. ??? ????????? ????????? ????????? ?????? ????????? ??????.

                # Scrape Summoner's Rank information
                # [Solorank,Solorank Tier]
                solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
                # [Solorank LeaguePoint, Solorank W, Solorank L, Solorank Winratio]
                solorank_Point_and_winratio = deleteTags(
                    bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))
                # [Flex 5:5 Rank,Flexrank Tier,Flextier leaguepoint + W/L,Flextier win ratio]
                flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
                    'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                              'sub-tier__gray-text'}}))
                # ['Flextier W/L]
                flexrank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'sub-tier__gray-text'}}))

                # embed.set_imag()??? ????????? ???????????? ??????.

                # ??????, ?????? ?????? ?????? ??????????????? ?????? -> ????????? ????????? ?????? X
                if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                    embed = discord.Embed(title=playerNickname + "?????? ???????????????.", description="", color=0x0285FF)
                    embed.add_field(name="op.gg?????? ????????? ????????? ???????????????.", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                    embed.set_image(url='https:' + RankMedal[0]['src'])
                    embed.set_thumbnail(url="https://d1506sp6x4e9z7.cloudfront.net/gamasutra/uploads/1035771.png")
                    embed.set_footer(text='EMTRAY LOL BY EMTRAY#0002',
                                     icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/1385730/1a4d95bb4c09c9c8f1b421cdc2713c9a752cc8c1.gif')
                    await message.channel.send("", embed=embed)

                # ???????????? ????????? ????????????
                elif len(solorank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]
                    embed = discord.Embed(title=playerNickname + "?????? ???????????????.", description="", color=0x0285FF)
                    embed.add_field(name="op.gg?????? ????????? ????????? ???????????????.", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_image(url='https:' + RankMedal[1]['src'])
                    embed.set_thumbnail(url="https://d1506sp6x4e9z7.cloudfront.net/gamasutra/uploads/1035771.png")
                    embed.set_footer(text='EMTRAY LOL BY EMTRAY#0002',
                                     icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/1385730/1a4d95bb4c09c9c8f1b421cdc2713c9a752cc8c1.gif')
                    await message.channel.send("", embed=embed)

                # ???????????? ????????? ????????????
                elif len(flexrank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    embed = discord.Embed(title=playerNickname + "?????? ???????????????.", description="", color=0x0285FF)
                    embed.add_field(name="op.gg?????? ????????? ????????? ???????????????.", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + "WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_image(url='https:' + RankMedal[0]['src'])
                    embed.set_thumbnail(url="https://d1506sp6x4e9z7.cloudfront.net/gamasutra/uploads/1035771.png")
                    embed.set_footer(text='EMTRAY BOT BY EMTRAY#0002',
                                     icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/1385730/1a4d95bb4c09c9c8f1b421cdc2713c9a752cc8c1.gif')
                    await message.channel.send("", embed=embed)
                # ????????? ????????? ?????? ?????? ???????????????
                else:
                    # ??? ?????? ????????? thumbnail??? ??????
                    solorankmedal = RankMedal[0]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')
                    flexrankmedal = RankMedal[1]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')

                    # Make State
                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
                    embed = discord.Embed(title=playerNickname + "?????? ???????????????.", description="", color=0x0285FF)
                    embed.add_field(name="op.gg?????? ????????? ????????? ???????????????.", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url="https://d1506sp6x4e9z7.cloudfront.net/gamasutra/uploads/1035771.png")
                    if cmpTier == 0:
                        embed.set_image(url='https:' + RankMedal[0]['src'])
                    elif cmpTier == 1:
                        embed.set_image(url='https:' + RankMedal[1]['src'])
                    else:
                        if solorankmedal[1] > flexrankmedal[1]:
                            embed.set_image(url='https:' + RankMedal[0]['src'])
                        elif solorankmedal[1] < flexrankmedal[1]:
                            embed.set_image(url='https:' + RankMedal[0]['src'])
                        else:
                            embed.set_image(url='https:' + RankMedal[0]['src'])

                    embed.set_footer(text='EMTRAY LOL BOT BY EMTRAY#0002',
                                     icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/1385730/1a4d95bb4c09c9c8f1b421cdc2713c9a752cc8c1.gif')
                    await message.channel.send("", embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="??????????????? ??????????????????.", description="", color=0xFF0000)
            embed.add_field(name="", value="????????? ????????? ?????????????????????.", inline=False)
            await message.channel.send("Wrong Summoner Nickname")

        except UnicodeEncodeError as e:
            embed = discord.Embed(title="??????????????? ??????????????????.", description="", color=0xFF0000)
            embed.add_field(name="???", value="????????? ????????? ?????????????????????.", inline=False)
            await message.channel.send("Wrong Summoner Nickname", embed=embed)

        except AttributeError as e:
            embed = discord.Embed(title="???????????? ?????? ?????????", description="", color=0xFF0000)
            embed.add_field(name="?????? ???????????? ???????????? ???????????? ????????????.", value="????????? ????????? ??????????????????", inline=False)
            embed.set_footer(text='EMTRAY BOT BY EMTRAY#0002',
                             icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/1385730/1a4d95bb4c09c9c8f1b421cdc2713c9a752cc8c1.gif')
            await message.channel.send("Error : Non existing Summoner ", embed=embed)

    if message.content.startswith(".?????????"):
        # ??????????????? ????????? ???????????? ???????????????"
        covidSite = "http://ncov.mohw.go.kr/index.jsp"
        covidNotice = "http://ncov.mohw.go.kr"
        html = urlopen(covidSite)
        bs = BeautifulSoup(html, 'html.parser')
        latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
        statisticalNumbers = bs.findAll('span', {'class': 'num'})
        beforedayNumbers = bs.findAll('span', {'class': 'before'})

        #?????? ????????? ??? ????????????
        briefTasks = []
        mainbrief = bs.findAll('a',{'href' : re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
        for brf in mainbrief:
            container = []
            container.append(brf.text)
            container.append(covidNotice + brf['href'])
            briefTasks.append(container)
        print(briefTasks)

        # ????????????
        statNum = []
        # ???????????? ??????
        beforeNum = []
        for num in range(7):
            statNum.append(statisticalNumbers[num].text)
        for num in range(4):
            beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

        totalPeopletoInt = statNum[0].split(')')[-1].split(',')
        tpInt = ''.join(totalPeopletoInt)
        lethatRate = round((int(statNum[3]) / int(tpInt)) * 100, 2)
        embed = discord.Embed(title="Covid-19 Virus Korea Status", description="",color=0x5CD1E5)
        embed.add_field(name="Data source : Ministry of Health and Welfare of Korea", value="http://ncov.mohw.go.kr/index.jsp", inline=False)
        embed.add_field(name="Latest data refred time",value="?????? ????????? " + latestupdateTime[0] + "??? " + latestupdateTime[1] + "??? "+latestupdateTime[2] +" ???????????????.", inline=False)
        embed.add_field(name="????????????(??????)", value=statNum[0].split(')')[-1]+"("+beforeNum[0]+")",inline=True)
        embed.add_field(name="????????????(????????????)", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
        embed.add_field(name="?????????(?????? ???)", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
        embed.add_field(name="??????", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
        embed.add_field(name="???????????????", value=statNum[6], inline=True)
        embed.add_field(name="?????????", value=str(lethatRate) + " %",inline=True)
        embed.add_field(name="- ?????? ????????? 1 : " + briefTasks[0][0],value="Link : " + briefTasks[0][1],inline=False)
        embed.add_field(name="- ?????? ????????? 2 : " + briefTasks[1][0], value="Link : " + briefTasks[1][1], inline=False)
        embed.set_thumbnail(url="https://wikis.krsocsci.org/images/7/79/%EB%8C%80%ED%95%9C%EC%99%95%EA%B5%AD_%ED%83%9C%EA%B7%B9%EA%B8%B0.jpg")
        embed.set_footer(text='EMTRAY BOT BY EMTRAY#0002',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("s", embed=embed)


keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)

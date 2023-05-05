import json
from lib.types.error import *
import typing
import discord
from datetime import datetime as dt
from lib.connections import *
from lib.misc import *

class SupportUnit:
    def __init__(self, op_id: str, op_skill: int, op_module: int | None = None) -> None:
        self.ID: str = op_id
        self.SKILL: int = op_skill
        self.MODULE: int | None = op_module

    def createEmbed(self, profileUrl:str|None=None, profileName:str|None=None) -> discord.Embed:
        emb:discord.Embed = discord.Embed(
            color=discord.Colour.random(),
            title=getOperatorNameFromId(self.ID),
            timestamp=dt.now(),
            fields=[
                discord.EmbedField(name="skill".upper(), value=str(self.SKILL), inline=True),
                discord.EmbedField(name="module".upper(), value=str(self.MODULE) if self.MODULE != None else "N/A", inline=True)
            ]
        )
        emb.set_footer(text="Fetched from Krooster API v1")
        emb.set_thumbnail(url=getRoute(key="op_thumbnail_265", data={"char_id":self.ID}))
        # if profileUrl != None:
        authorDta:dict[str, str] = {
            "name": profileName if profileName != None else ""
        }
        if profileUrl != None: authorDta["url"] = profileUrl
        emb.set_author(**authorDta)
        return emb

    def __str__(self) -> str:
        return f"{getOperatorNameFromId(self.ID)} {self.SKILL} {self.MODULE}" if self.MODULE != None else f"{getOperatorNameFromId(self.ID)} {self.SKILL}"

    def __json__(self) -> dict[str, str | int | None]:
        return {
            "id": self.ID,
            "skill": self.SKILL,
            "module": self.MODULE,
        }


def getOperatorNameFromId(id:str | None) -> str:
    dta:dict[str, dict[str, str]] = dict(json.load(open("./data/operators.json", encoding="utf-8")))
    return dta.get(str(id), {}).get("name", f"<{id}>")

class Operator:
    def __init__(self, id: str, owned: bool, favourite: bool, potential: int, elite: int, level: int, rank: int, masteries: list[int], modules: list[int], skin: str | None, users: typing.Any = None) -> None:
        self.ID: str = id
        self.owned: bool = owned
        self.favourite: bool = favourite
        self.potential: int = potential
        self.elite: int = elite
        self.level: int = level
        self.rank: int = rank
        self.masteries: list[int] = masteries
        self.modules: list[int] = modules
        self.skin: str | None = skin
        self.users: typing.Any = users

    def createEmbed(self, profileUrl:str|None=None, profileName:str|None=None) -> discord.Embed:
        opName:str = getOperatorNameFromId(self.ID)
        emb:discord.Embed = discord.Embed(
            color=discord.Colour.from_rgb(*textToColor(opName)),
            title=opName,
            timestamp=dt.now(),
            fields=[
                discord.EmbedField(name="owned".upper(), value=str(self.owned), inline=True),
                discord.EmbedField(name="favourite".upper(), value=str(self.favourite), inline=True),
                discord.EmbedField(name="potential".upper(), value=str(self.potential), inline=True),
                discord.EmbedField(name="elite".upper(), value=str(self.elite), inline=True),
                discord.EmbedField(name="level".upper(), value=str(self.level), inline=True),
                discord.EmbedField(name="rank".upper(), value=str(self.rank), inline=True),
                discord.EmbedField(name="masteries".upper(), value="\n".join([f"S{m+1}M{self.masteries[m]}" for m in range(len(self.masteries))]) if len(self.masteries) > 0 else "N/A", inline=True),
                discord.EmbedField(name="modules".upper(), value="\n".join([str(m) for m in self.modules]) if len(self.modules) > 0 else "N/A", inline=True),
                discord.EmbedField(name="skin".upper(), value=str(self.skin) if self.skin != None else "N/A", inline=True),
                discord.EmbedField(name="users".upper(), value=str(self.users) if self.users != None else "N/A", inline=True)
            ]
        )
        emb.set_footer(text="Fetched from Krooster API v1")
        emb.set_thumbnail(url=getRoute(key="op_thumbnail_265", data={"char_id":self.ID}))
        authorDta:dict[str, str] = {
            "name": profileName if profileName != None else ""
        }
        if profileUrl != None: authorDta["url"] = profileUrl
        emb.set_author(**authorDta)
        return emb
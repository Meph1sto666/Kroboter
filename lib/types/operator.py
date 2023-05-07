import json
from lib.types.error import *
import typing
import discord
from datetime import datetime as dt
from lib.connections import *
from lib.misc import *
"""
class SupportUnit:
    def __init__(self, op_id: str, op_skill: int, op_module: int | None = None) -> None:
        self.id: str = op_id
        self.SKILL: int = op_skill
        self.MODULE: int | None = op_module

    def createEmbed(self, profileUrl:str|None=None, profileName:str|None=None) -> discord.Embed:
        emb:discord.Embed = discord.Embed(
            color=discord.Colour.random(),
            title=getOperatorNameFromId(self.id),
            timestamp=dt.now(),
            fields=[
                discord.EmbedField(name="skill".upper(), value=str(self.SKILL), inline=True),
                discord.EmbedField(name="module".upper(), value=str(self.MODULE) if self.MODULE != None else "N/A", inline=True)
            ]
        )
        emb.set_footer(text="Fetched from Krooster API v1")
        emb.set_thumbnail(url=getRoute(key="op_thumbnail_265", data={"char_id":self.id}))
        # if profileUrl != None:
        authorDta:dict[str, str] = {
            "name": profileName if profileName != None else ""
        }
        if profileUrl != None: authorDta["url"] = profileUrl
        emb.set_author(**authorDta)
        return emb

    def __str__(self) -> str:
        return f"{getOperatorNameFromId(self.id)} {self.SKILL} {self.MODULE}" if self.MODULE != None else f"{getOperatorNameFromId(self.id)} {self.SKILL}"

    def __json__(self) -> dict[str, str | int | None]:
        return {
            "id": self.id,
            "skill": self.SKILL,
            "module": self.MODULE,
        }
"""

def getOperatorNameById(id:str | None) -> str:
    dta:dict[str, dict[str, str]] = dict(json.load(open("./data/operators.json", encoding="utf-8")))
    return dta.get(str(id), {}).get("name", f"<{id}>")
def getOperatorRarityById(id:str | None) -> int:
    dta:dict[str, dict[str, int]] = dict(json.load(open("./data/operators.json", encoding="utf-8")))
    return dta.get(str(id), {}).get("rarity", -1)
def getRarityColor(rarity:int) -> tuple[int, int, int]:
    dta:dict[str,str] = dict(json.load(open("./data/raritycolors.json", encoding="utf-8")))
    return hexToRgb(dta.get(str(rarity), "#FF0000"))

class Operator:
    """Represents an `Operator` object

        Attributes
        ----------
        id (:class:`str`):
            Id of the operator.
        owned (:class:`bool`):
            True if the operator is owned by the user.
        favourite (:class:`bool`):
            True if the user has marked the operator as favourite.
        potential (:class:`int`):
            Potential of the operator.
        elite (:class:`int`):
            Operator elite level.
        level (:class:`int`):
            Operator level.
        rank (:class:`int`):
            Operator skill level.
        masteries (:class:`list[int]`):
            Operator skill masteries (array length corresponding to operator skill amount).
        masteries (:class:`list[int]`):
            Operator modules. Empty if the op does not have any modules
        skin (:class:`str | None`):
            None if no skin is selected.
    """
    def __init__(self, id: str, owned: bool, favourite: bool, potential: int, elite: int, level: int, rank: int, masteries: list[int], modules: list[int], skin: str | None, users: typing.Any = None) -> None:
        """_summary_

        Args:
            id (str): _description_
            owned (bool): _description_
            favourite (bool): _description_
            potential (int): _description_
            elite (int): _description_
            level (int): _description_
            rank (int): _description_
            masteries (list[int]): _description_
            modules (list[int]): _description_
            skin (str | None): _description_
            users (typing.Any, optional): _description_. Defaults to None.
        """
        self.id: str = id
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
        opName:str = getOperatorNameById(self.id)
        emb:discord.Embed = discord.Embed(
            color=discord.Colour.from_rgb(*getRarityColor(getOperatorRarityById(self.id))),
            title=opName + " :hearts:" if self.favourite else opName,
            timestamp=dt.now(),
            fields=[
                discord.EmbedField(name="elite".upper(), value=str(self.elite), inline=True),
                discord.EmbedField(name="level".upper(), value=str(self.level), inline=True),
                discord.EmbedField(name="potential".upper(), value=str(self.potential), inline=True),
                discord.EmbedField(name="skills".upper(), value="".join([f"S{m+1} M{self.masteries[m]}\n" if self.masteries[m] > 0 else "" for m in range(len(self.masteries))])
                    if not all([m==0 for m in self.masteries]) > 0 else str(self.rank), inline=True),
            ]
        )
        emb.add_field(name="modules".upper(), value="".join([f"M{m+1} L{str(self.modules[m])}\n" for m in range(len(self.modules))]), inline=True) if sum(self.modules) > 0 else None
        emb.set_footer(text="Fetched from Krooster API v1")
        emb.set_thumbnail(url=getRoute(key="op_thumbnail_265", data={"char_id":self.skin if self.skin!=None else self.id}))
        authorDta:dict[str, str] = {"name": profileName if profileName != None else ""}
        if profileUrl != None: authorDta["url"] = profileUrl
        emb.set_author(**authorDta)
        return emb
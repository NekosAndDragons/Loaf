from enum import Enum
import secrets
import discord

class AnalysisState(Enum):
    OK = 0        
    SPAM = 1
    RAID = 2    

""" Analyses messages in order to perform certain actions.
In some cases should be extended in pair with ServerState.
"""
class ServerKeeper():
    def __init__(self, serverState):
        self.serverState = serverState
        self.warnedDueToSpam = []
        self.warnedDueToRaid = []

    async def performAction(self, message):
        state = self.__analyseState()
        if state == AnalysisState.OK:
            return
        elif state == AnalysisState.SPAM:
            author = message.author
            if author.name not in self.warnedDueToSpam:
                self.warnedDueToSpam.append(author.name)
                await author.send("Hello there! Be careful - sending too many messages on public channels makes it less readable.")
                await message.channel.send(secrets.choice(spamWarns))
        elif state == AnalysisState.RAID:
            if author.name not in self.warnedDueToRaid:
                self.warnedDueToRaid.append(author.name)
                await message.author.send("You have been warned. Maybe try to rest a little?")
                membership = discord.utils.get(message.guild.roles, name="Member")
                await membership.delete()

    def __analyseState(self):
        state = self.serverState
        if state.lastAuthorCounter >= 20 and state.lastAuthor in self.warnedDueToSpam:
            return AnalysisState.RAID
        if state.lastAuthorCounter >= 10: 
            return AnalysisState.SPAM
        
        return AnalysisState.OK

spamWarns = [
    'Woah so many messages! <:scared:863844217624199198>',
    'Slow down or my fur will be a mess! <:nightmare:916985709259259964>',
    'Do I smell fish? Or maybe just a little bit of spam? <:why:942083877537714217>',
    'Congratulations! You managed to wake me up, human... <:evil:915342939322994699>'
]
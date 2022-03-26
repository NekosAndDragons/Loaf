import modules.about as about
import modules.duel as duel
import modules.fate as fate
import modules.help as help
import modules.lure as lure
import utils.serverState as serverState
import utils.serverKeeper as serverKeeper
from utils.logger import logging as LOG
import re

""" Maintains the context. Extending existing or adding new modules should take place here.
Available modules for Loaf 2.0: About, Duel, Fate, Help, Lure.
"""
class Context():
    def __init__(self):
        self.applicationState = serverState.ServerState()
        self.applicationKeeper = serverKeeper.ServerKeeper(self.applicationState)
        self.about = about.About()
        self.duel = duel.Duel()
        self.fate = fate.Fate()
        self.help = help.Help()
        self.lure = lure.Lure()
        self.context = [self.about, self.duel, self.fate, self.help, self.lure]
        self.properties = loadProperties("src/utils/regex.properties")
        LOG.info('Bot-context with {0} modules has been created!'.format(len(self.context)))

    async def processMessage(self, message):
        await self.__updateApplicationState(message)
        await self.__keep(message)
        await self.__dispatchMessage(message)

    async def __updateApplicationState(self, message):
        await self.applicationState.updateState(message)

    async def __keep(self, message):
        await self.applicationKeeper.performAction(message)

    async def __dispatchMessage(self, message):
        LOG.info(message.content)
        targetModule = self.__determineModule(message.content)

        if targetModule == 'about': 
            await self.about.execute(message)
        if targetModule == 'duel':
            await self.duel.execute(message)
        if targetModule ==  'fate':
            await self.fate.execute(message)
        if targetModule ==  'help':
            await self.help.execute(message)
        if targetModule ==  'lure':
            await self.lure.execute(message)

    def __determineModule(self, text):
        targetModule = None
        for property in self.properties:
            regex = self.properties[property]
            if re.match(regex, text):
                targetModule =  property.split('.')[0]
                break
        return targetModule
        
def loadProperties(filePath, separator='=', commentChar='#'):
    properties = {}
    with open(filePath, "rt") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith(commentChar):
                splittedLine = line.split(separator)
                key = splittedLine[0].strip()
                value = separator.join(splittedLine[1:]).strip().strip('"')
                properties[key] = value
    LOG.info('Loaded {0} properties: {1}'.format(len(properties), properties))
    return properties
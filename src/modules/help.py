from enum import Enum
from utils.logger import logging as LOG

class Options(Enum):
    ABOUT = "about"       
    DUEL = "duel"
    FATE = "fate"
    HELP = "help"
    LURE = "lure"

class Help():
    def __init__(self):
        self.moduleOptions = [option.value for option in Options]
        LOG.info('Help-module has been established.')

    async def execute(self, message):
        command = self.__determineCommand(message)
        result = "Hmm, I've never heard about this command... maybe you made a typo?"
        if command == Options.HELP:
            result = self.getInfoForHelpModule()
        if command == Options.ABOUT:
            result = self.getInfoForAboutModule()
        if command == Options.DUEL:
            result = self.getInfoForDuelModule()
        if command == Options.FATE:
            result = self.getInfoForFateModule()
        if command == Options.LURE:
            result = self.getInfoForLureModule()
        await message.channel.send(result)

    def getInfoForHelpModule(self):
        formattedCommands = ', '.join('**{0}**'.format(option) for option in self.moduleOptions)
        return "There are available {0} categories of commands at the moment: {1}.\nIf you'd like to learn more about any of them, simply use **$help:[category]**.".format(len(self.moduleOptions), formattedCommands)

    def getInfoForAboutModule(self):
        return "By using **$about:[user]** command, you might learn something interesting about others. If you want to take a peek into the list of available users, simply use **$about**. Who knows, maybe you'll be able to solve a few mysteries with it?"

    def getInfoForDuelModule(self):
        return "If you wish to challenge others, feel free to use **$duel:[@user]**. Your enemy will have 5 minutes to accept your challenge, by responding with **$duel**. After that time, the queue will be released. Keep in mind, that dueling might take a while. Because of that, a channel called <#806464059389640715> has been created."

    def getInfoForFateModule(self):
        return "Would you like me to become a diviner? If you responded with yes, feel free to use **$fate:[@user]** and I will tell you what's awaiting both of you in the future! The outcome is guaranteed as long as you can provide some proper food, hehehehe."

    def getInfoForLureModule(self):
        return "Hehehe... this one is a little tricky. All I can say now, is that I'm certainly gonna respond to some messages you're about to send!"

    def __determineCommand(self, message):
        text = message.content.split(':')
        if len(text) > 1:
            text[1] = text[1].lower()

        if len(text) == 1 or text[1] == Options.HELP.value:
            return Options.HELP
        if text[1] == Options.ABOUT.value:
            return Options.ABOUT
        if text[1] == Options.DUEL.value:
            return Options.DUEL
        if text[1] == Options.LURE.value:
            return Options.LURE
        if text[1] == Options.FATE.value:
            return Options.FATE
        return None
        
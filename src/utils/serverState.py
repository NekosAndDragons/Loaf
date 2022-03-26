from datetime import datetime

""" Holds the exendable state of the server. 
Should not perform any actions on the contained data to avoid risk of corrputing it.
"""
class ServerState():
    def __init__(self):
        self.lastAuthor = None
        self.lastAuthorCounter = 0
        self.firstMessageTime = None
        self.lastMessageTime = None
        self.totalMessageLength = 0

    async def updateState(self, message):
        if self.lastAuthor != message.author.name:
            self.lastAuthor = message.author.name
            self.lastAuthorCounter = 1
            self.firstMessageTime = datetime.now()
            self.lastMessageTime = datetime.now()
            self.totalMessageLength = len(message.content)
        else:
            self.lastAuthorCounter = self.lastAuthorCounter + 1
            self.lastMessageTime = datetime.now()
            self.totalMessageLength = self.totalMessageLength + len(message.content)

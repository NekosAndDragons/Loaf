import secrets
from utils.logger import logging as LOG

class Lure():
    def __init__(self):
        self.responses = lureResponses
        LOG.info('Lure-module has been established.')

    async def execute(self, message):
        await message.channel.send(secrets.choice(lureResponses))

lureResponses = [
  "Someone called me?", 
  "Meow?", 
  "OwO", 
  "How can I be at service?",
  "Who dares summoning me?",
  "Did you say psps?"
  ]

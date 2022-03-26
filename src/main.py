import discord
import keep_alive
from context import Context
from utils.logger import logging as LOG
import sys
import os

sys.path.insert(0, 'src/')
context = Context()
client = discord.Client()

@client.event
async def on_ready():
  LOG.info('Application {0.user} has started.'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  LOG.info('[{0.author}]> {0.content}'.format(message))
  await context.processMessage(message)

keep_alive.keep_alive()
client.run(os.environ['TOKEN'])
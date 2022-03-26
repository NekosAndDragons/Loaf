from utils.logger import logging as LOG
from utils import utils

class Fate():
  def __init__(self):
    self.responses = fateResponses
    LOG.info('Fate-module has been established.')

  async def execute(self, message):
    person = utils.getAnnotatedUser(message)
    author = message.author.name
    if person == author:
      await message.channel.send('Ekhm... are you planning on staying single forever?')
    else:
      index = (ord(person[0]) + ord(author[0])) % len(fateResponses)
      result = "About " + author + " and " + person + ":\n" + fateResponses[index]
      await message.channel.send(result)

fateResponses = [
  "You're definitely BFFs!", 
  "You two should play more games together.", 
  "Your fate is to fight forever for dominance!", 
  "I think you two should watch something together!", 
  "It is rather... complicated?", 
  "Even I can't tell the future for you two..."
  "One of you will receive huge success. The other one - even greater!"
  "You should send more memes to each other!"
]

import random
import secrets
from enum import Enum
from utils.logger import logging as LOG
from utils import utils

class Command(Enum):
    ATTACK = "attack"
    DEFENCE = "defence"
    DODGE = "dodge"
    FEED = "feed"
    PET = "pet"
    BOOP = "boop"
    BONK = "bonk"
    STATS = "stats"
    ACCEPT = "accept"
    DECLINE = "decline"
    FINISH = "finish"

class Error(Enum):
    DUELING_SELF = 0
    DUELING_LOAF = 1
    DUELING_COFFEE = 2

class DuelState(Enum):
    IDLE = 0        # no duels - module is available
    INIT = 1        # P1 initialized a duel
    STARTED = 2     # P2 accepted a duel

class Duel():
  def __init__(self):
    self.__initializeModule()
    LOG.info('Duel-module has been established.')

  async def execute(self, message):
    result = self.__determineCommand(message)
    if(isinstance(result, Error)):
      await self.__processError(message, result)
    elif(isinstance(result, DuelState)):
      await self.__processDuelState(message, result)
    elif(isinstance(result, Command)):
      await self.__processCommand(message, result)
    else:
      LOG.error('Something weird has happened. Result: {0}, message: {1}'.format(result, message.content))

  async def __processCommand(self, message, command):
    attacker = self.__defineAttacker(message.author.name)
    target = self.__defineTarget(message.author.name)

    if attacker.name != self.next:
      await message.channel.send("It's not your turn now!")
      return

    if command == Command.ATTACK:
      await self.__executeAttack(attacker, target, message)
    elif command == Command.DEFENCE:
      await self.__executeDefence(attacker, target, message)
    elif command == Command.DODGE:
      await self.__executeDodge(attacker, target, message)
    elif command == Command.FEED:
      await self.__executeFeed(attacker, target, message)
    elif command == Command.PET:
      await self.__executePet(attacker, target, message)
    elif command == Command.BOOP:
      await self.__executeBoop(attacker, target, message)
    elif command == Command.BONK:
      await self.__executeBonk(attacker, target, message)
    elif command == Command.STATS:
      await self.__executeStats(attacker, target, message)
    elif command == Command.ACCEPT:
      await self.__executeAccept(attacker, target, message)
    elif command == Command.DECLINE:
      await self.__executeDecline(attacker, target, message)
    elif command == Command.FINISH:
      await self.__executeFinish(attacker, target, message)
    else:
      await message.channel.send('I am confusion...')

  async def __processDuelState(self, message, state):
    if state == DuelState.INIT:
      self.playerOneName = message.author.name
      self.playerTwoName = utils.getAnnotatedUser(message)
      self.playerOneRole = self.__determineRole(message.author.roles)
      await message.channel.send("I wonder if " + self.playerTwoName + " is up to the challenge...")
      await message.mentions[0].send("Hello there! It seems, that {0} is challenging you for a duel in <#806464059389640715>.".format(message.author.name))
      self.duelState = DuelState.INIT
    elif state == DuelState.STARTED:
      self.playerTwoRole = self.__determineRole(message.author.roles)
      self.__initializeDuel()
      await message.channel.send(self.__getDuelRules())
      await message.channel.send(self.__getDuelHeader())
      self.duelState == DuelState.STARTED

  async def __processError(self, message, error):
    if error == Error.DUELING_SELF:
      await message.channel.send("Whatever you're trying to achieve...\nI would rather say it's some sort of masochism.")
    elif error == Error.DUELING_LOAF:
      await message.channel.send("*very fast paw attack*\nCongratulations! You lost. What were you expecting?\nHonestly...")
    elif error == Error.DUELING_COFFEE:
      await message.channel.send("Umm... I would rather avoid challenging him.\nIf you want to live, that is.")
    else:
      await message.channel.send("An unexpected error has occured!")

  def __initializeDuel(self):
    self.playerOne = Player(self.playerOneName, self.playerOneRole)
    self.playerTwo = Player(self.playerTwoName, self.playerTwoRole)
    self.next = secrets.choice([self.playerOneName, self.playerTwoName])

  def __initializeModule(self):
    self.playerOne = None
    self.playerTwo = None
    self.playerOneName = None
    self.playerTwoName = None
    self.playerOneRole = None
    self.playerTwoRole = None
    self.duelState = DuelState.IDLE
    self.next = None

  def __defineAttacker(self, attacker):
    return self.playerOne if attacker == self.playerOneName else self.playerTwo

  def __defineTarget(self, attacker):
    return self.playerTwo if attacker == self.playerOneName else self.playerOne
    
  def __determineCommand(self, message):
    author = message.author.name
    text = message.content.split(':')
    if len(text) > 1:
      annotatedUser = utils.getAnnotatedUser(message)
      if author == annotatedUser:
        return Error.DUELING_SELF
      if annotatedUser == "Loaf":
        return Error.DUELING_LOAF
      if annotatedUser == "Coffee":
        return Error.DUELING_COFFEE

      if self.duelState == DuelState.IDLE:
        return DuelState.INIT
      elif self.duelState == DuelState.INIT and self.playerOneName == annotatedUser and self.playerTwoName == author:
        return DuelState.STARTED
    else:
      text = message.content[1:]
      if text == Command.ATTACK.value:
        return Command.ATTACK
      if text == Command.DEFENCE.value:
        return Command.DEFENCE
      if text == Command.DODGE.value:
        return Command.DODGE
      if text == Command.FEED.value:
        return Command.FEED
      if text == Command.PET.value:
        return Command.PET
      if text == Command.BOOP.value:
        return Command.BOOP
      if text == Command.BONK.value:
        return Command.BONK
      if text == Command.STATS.value:
        return Command.STATS
      if text == Command.ACCEPT.value:
        return Command.ACCEPT
      if text == Command.DECLINE.value:
        return Command.DECLINE
      if text == Command.FINISH.value:
        return Command.FINISH
    return None

  def __getDuelRules(self):
    quotes = [
      'Fate is a whimsical thing - and so am I.',
      'Well well well well, well well well...',
      'What is love? Sorry, that was a strange think to ask.',
      'Did you know, that "I am" is the shortest complete sentence in the English language?',
      'EEEEERIKA~!'
    ]

    return '''
  Here's a little tutorial:

  $attack: deal damage to your enemy!
  $defence: boost your defence!
  $dodge: focus on dodging attacks!
  $pet: who knows what future might bring?
  $feed: do it when you're wounded, and I'll do my best to share good vibes with you!
  $bonk: ah, the ultimate high-risk move. Use only with caution!
  $stats: displays your statistics! Does not end your turn, so you may do it whenever you want. But don't spam it, okay?
  $finish: ends the duel immidiatly.

  Okay then, if everything's clear - show me your determination!
    /\\\_/\\
  (   𝕠.𝕠   ) {0} {1} goes first.
  ( |         | )
  '''.format(secrets.choice(quotes), self.next)

  def __getDuelHeader(self):
    return "Duel between [{0}] {1} and [{2}] {3} has begun!\nOnly booping is forbidden!\nGood luck!".format(self.playerOneRole, self.playerOneName, self.playerTwoRole, self.playerTwoName)

  async def __executeAttack(self, attacker, target, message):
    dodge = True if random.randint(0, 100) <= (target.dodge) else False
    if dodge:
      self.__next()
      await message.channel.send("Woah! It seems like your enemy dodged your attack!")
    else:
      critical = 1.5 if random.randint(0, 100) <= (attacker.critical) else 1
      damage = int((random.randint(1, 5) + attacker.attack) * critical * (1 - target.defence / 100))

      result = ""
      if critical == 1.5:
        result = "Critical hit!\n"

      target.hp = int(target.hp - damage,)
      result = result + "{0} deals {1} damage to {2}! {2} has {3}hp left!\n".format(attacker.name, damage, target.name, target.hp)
      if target.hp <= 0:
        result = result + "Actually it seems like {0} has lost.\nCongratulations {1}, you're the winner!".format(target.name, attacker.name)
        await self.__executeFinish(attacker, target, message)

      self.__next()
      await message.channel.send(result)
        
  async def __executeDefence(self, attacker, target, message):
    defence = random.randint(6, 8)
    attacker.defence = attacker.defence + defence
    self.__next()
    await message.channel.send("{0} decides to stay still and observe surroundings! You gain +{1}% defence!".format(attacker.name, defence))

  async def __executeDodge(self, attacker, target, message):
    dodge = random.randint(5, 8)
    attacker.dodge = attacker.dodge + dodge
    self.__next()
    await message.channel.send("{0} decides to focus on avoiding attacks this time! You gain +{1}% dodge.".format(attacker.name, dodge))

  async def __executeFeed(self, attacker, target, message):
    if attacker.hp >= statistics[attacker.role]["HP"]:
      attacker.critical = attacker.critical + 7
      attacker.dodge = attacker.dodge + 5
      self.__next()
      await message.channel.send("Eating too much will make Loaf too loafy. It appreciates your effort and eats anyway.\nYour next attack won’t miss for sure!\nCritical + 7%\nDodge +5%")
    else:
      heal = random.randint(5, 25)
      attacker.hp = attacker.hp + heal
      self.__next()
      await message.channel.send("Loaf likes to eat... like any other creature. You restore {0}hp thanks to vibrations he makes!".format(heal))

  async def __executePet(self, attacker, target, message):
    result = "Loaf is very pleased by your actions."
    if attacker.role == 'Neko':
      result = "Loaf loves having fun with other cats. It’s very happy!"
    elif attacker.role == 'Dragon':
      result = "Loaf is a little bit intimidated, but it enjoys the big hand petting it!"
    elif attacker.role == 'Avali':
      result = "Loaf approaches the friendly looking Avali and purrs loudly."
    elif attacker.role == 'Fox':
      result = "Loaf detects cat’s software on dog’s hardware. It is a little confused but purrs happily!"

    attackBoost = random.randint(4, 7)
    criticalBoost = random.randint(3, 5)
    attacker.attack = attacker.attack + attackBoost
    attacker.critical = attacker.critical + criticalBoost
    result = result + "\nYour attack has increased by {0} and your critical hit chance by {1}% which is nice!".format(attackBoost, criticalBoost)
    self.__next()
    await message.channel.send(result)

  async def __executeBonk(self, attacker, target, message):
    isBonkSuccessful = True if random.randint(1, 100) <= 50 else False
    if isBonkSuccessful:
      damage = int((attacker.attack + random.randint(1, 10)) * 2 * (1 - target.defence / 100))
      target.hp = target.hp - damage
      self.__next()
      result = "What a magnificent bonk! Your oponent takes {0}hp damage and goes to the horny jail!\nAs a Neko, I am quite impressed.\n{1} has {2}hp left!".format(damage, target.name, target.hp)

      if target.hp <= 0:
        result = result + "\nActually it seems like {0} has lost.\nCongratulations {1}, you're the winner!".format(target.name, attacker.name)
        await self.__executeFinish()
      await message.channel.send(result)
    else:
      heal = random.randint(10, 20)
      target.hp = target.hp + heal
      self.__next()
      await message.channel.send("{0} finds your action pretty kinky! He gains {1}hp and stares at you!\nI’d run if I were you...".format(target.name, heal))

  async def __executeBoop(self, attacker, target, message):
    attacker.hp = attacker.hp - 5
    self.__next()
    await message.channel.send("*sudden attack* Uh... I warned you that booping is forbidden!\nLoaf deals 5 damage to you... and you lose your precious turn.\nGood job, you played yourself!")

  async def __executeStats(self, attacker, target, message):
    await message.channel.send(attacker.getStats())

  async def __executeAccept(self, attacker, target, message):
    # TODO
    pass

  async def __executeDecline(self, attacker, target, message):
    # TODO
    pass

  async def __executeFinish(self, attacker, target, message):
    self.__initializeModule()
    await message.channel.send("Everything's has an end. I hope to see you again in the battlefield!")

  def __next(self):
    self.next = (self.playerOneName if self.next == self.playerTwoName else self.playerTwoName)

  def __determineRole(self, roles):
    role = "Animal"
    roleNames = [role.name for role in roles]
    for availableRole in self.__getAvailableRoles():
      if availableRole in roleNames:
        role = availableRole
        break
    return role

  def __getAvailableRoles(self):
    return statistics.keys()

statistics = {
  "Fox":          {"HP": 90,  "Attack": 9,  "Defence": 20, "Dodge": 10, "Critical": 10},
  "Neko":         {"HP": 85,  "Attack": 10, "Defence": 18, "Dodge": 12, "Critical": 14},
  "Bunny":        {"HP": 75,  "Attack": 7,  "Defence": 8,  "Dodge": 20, "Critical": 8},
  "Avali":        {"HP": 95,  "Attack": 8,  "Defence": 22, "Dodge": 8,  "Critical": 8},
  "Animal":       {"HP": 100, "Attack": 10, "Defence": 5,  "Dodge": 5,  "Critical": 5},
  "Dragon":       {"HP": 115, "Attack": 13, "Defence": 30, "Dodge": 7,  "Critical": 5},
  "Wolf Dragon":  {"HP": 110, "Attack": 15, "Defence": 22, "Dodge": 3,  "Critical": 7},
  "Avali Dragon": {"HP": 125, "Attack": 12, "Defence": 20, "Dodge": 8,  "Critical": 4},
}

class Player:
  defenceCounter = 0
  dodgeCounter = 0
  petCounter = 0
  feedCounter = 0
  statCounter = 0
  isBonkAvailable = True
  
  def __init__(self, name, role):
    self.name = name
    self.role = role
    classStatistics = statistics[role]
    self.hp = classStatistics["HP"]
    self.attack = classStatistics["Attack"]
    self.defence = classStatistics["Defence"]
    self.dodge = classStatistics["Dodge"]
    self.critical = classStatistics["Critical"]

  def getStats(self):
    return "=== {0}'s statistics ===\nHP: {1}\nAttack: {2}\nDefence: {3}%\nDodge: {4}%\nCritical: {5}%\n".format(self.name, self.hp, self.attack, self.defence, self.dodge, self.critical)

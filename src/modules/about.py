from utils.logger import logging as LOG
from utils import utils
from enum import Enum

class Options(Enum):
    INFO = "info"       
    PERFORM = "perform"

class About():
  def __init__(self):
    self.responses = responses;
    self.usersExcludedFromAboutModule = ["Loaf"]
    LOG.info('About-module has been established')

  async def execute(self, message):
    command = self.__determineCommand(message)
    result = "Hmm, I've never heard about this command... maybe you made a typo?"
    if command == Options.INFO:
      result = self.__getAvailableOptions()
    else:
      mentionedPerson = utils.getMentionedUser(message.content)
      result = self.__prepareMessage(mentionedPerson)
    await message.channel.send(result)

  def __getAvailableOptions(self):
    keys = sorted(responses.keys())
    result = 'List of memorized users:\n'
    for i in range(0, len(keys)):
        if keys[i] in self.usersExcludedFromAboutModule:
            continue
        result = result + f"[{i}] " + keys[i] + "\n"
    result = result + '\n';
    result = result + "Is the anyone missing? Use @Bug annotation to let the administrator know!"
    return result

  def __prepareMessage(self, person):
      if person in responses.keys():
          global currentResponseValue, currentResponseKey
          if person != currentResponseKey or currentResponseValue == None or len(responses[person]) <= (currentResponseValue + 1):
              currentResponseValue = 0
          else:
              currentResponseValue = currentResponseValue + 1
          currentResponseKey = person
          return responses[person][currentResponseValue]

      return "Hmm... I don't know this nickname. You should use one of the registered nickname available under **$about**."

  def __determineCommand(self, message):
    text = message.content.split(':')
    if len(text) == 1:
        return Options.INFO

    return Options.PERFORM

responses = {
  "Shaiameow": [
    "Ah, my beloved creator. He feeds and pets me every single day!", 
    "Calls himself a Neko. I’m pretty sure he loves petting too.", 
    "Well, he is basically a weeb.",
    "Sun and Moon..."],
  "Crimm": [
    "Ah, yes. He always drinks tea and eats biscuits at 5 o’clock. Noblesse Oblige.", 
    "Pretty good car racer. Did he learn all his tricks playing Rocket League?", 
    "He is bound to this place, just like me - and you.",
    "He has a very nice guitar!"],
  "Tiffanbrill": [
    "He eats lots of pizza and only drinks coffee! I hope it's not the one with ananas!", 
    "Definitely a wholesome dragon~", 
    "He is... very... innocent. In a way!",
    "Plays MMORPGs. I bet he has a dragon mount."],
  "Zenedy": [
    "Proszę daj mi kawę! Proszę!", 
    "He is a Neko - just like me! He meows and purrs a lot and I appreciate it.", 
    "He has a nice motocycle. It purrs loudly~",
    "He takes care of many bunbuns and cavias. That's so nice!"],
  "Papi": [
    "Ah yes, the developing guitarist!", 
    "Some people call him Wolfy. But those are considered his special friends~", 
    "Proud owner of many cats and dogs. Is there anything greater to achieve?",
    "Do not ask him about Phasmophobia..."],
  "Swedboi": [
    "He is… lewd~ but also has pretty long, tempting neck!", 
    "Wholesome soul. I like him. I know he loves cats like me. Who would not?", 
    "The greatest fencer on the server!",
    "Has a good taste in anime!"],
  "Skimbo": [
    "He might be a dragon, but I know he loves cats. He also has a few of us!", 
    "Deoxyribonucleic acid.", 
    "I’m pretty sure he’s into trains. But how does it work exactly?", 
    "The greatest artist of all on this server. There is a rapidly developing competition though!"],
  "Ekairim": [
    "He definitely has the best hat out there!",
    "I think he is a big fan of snakes~",
    "He didn't really want me to mention him! Because of that I wanted to do it even more! Nyaahahaha~",
  ],
  "Aultori": [
    "Plays a lot of Monster Hunter World. But shouldn't killing the dragons there be against the rules?",
    "Owner of the almighty Dragon.",
    "Beans!",
  ],
  "Iamlogan": [
    "Hmm... he is a little bit... I don't know... sus?",
    "Tends to fall asleep on the voice chat from time to time. But I look over him.",
    "He enjoys meowing. A lot! I consider it a good feature.",
  ],
  "Mawterwelon": [
    "Toaster straight from the Germany! What a wonderful quality!",
    "Er hat eine tolle Kaffeemaschine! Oh sorry I forgot to use English again...",
    "He slurps others more often than I lick myself! I mean cleaning purposes of course.",
  ],
  "Tib": [
    "He’s developing his drawing skills. I can’t wait to see more!", 
    "Proud citizen of Austria.", 
    "He’s a player of Rocket League too! Pretty good though."],
  "Intet": [
    "This one can be generous!", 
    "Proud ciziten of Switzerland.", 
    "I love talking to him and lying on his laps!"],
  "Zeican": [
    "He has lots of interessting avatars in VRChat!", 
    "I like him, because he is very friendly. And has a nice keyboard!", 
    "He definitely enjoys challenges! I love watching him when he streams games."],
  "Roadie": [
    "He loves birds. I love them too... to some extent~", 
    "He possesses the best Avali among them all - according to what my creator says.", 
    "You know what? He is CUTE. Didn't expect that, huh? Hahaha!"],
  "Steam": [
    "I don’t have an access to NSFW stuff, but I know he is suspiciously active in there…", 
    "His animated emojis are adorable!", 
    "Competes with someone else for the most lewd person here~"],
  "Keloid": [
    "келоид? Он велик! I mean meow!", 
    "Very generous... and kind. Pretty rare, isn't it?", 
    "He cares about others more than you think."],
  "Memphis": [
    "Protogen associated with the Umbrella Corporation. Suspicious if you ask me.", 
    "He is smart. And funny! He also knows some Polish, although he comes from Czech Republic!", 
    "Knows a lot about buses and trains. Just like few other people here, hmm..."],
  "Voseno": [
    "He is developing many talents at the same time! Playing music, drawing, programming...", 
    "Ah yes, he might have some baguettes.", 
    "Proud owner of a cat - may it live long!"],
  "Sean": [
    "He knows a few languages, that's for sure!", 
    "He travels a lot. Who knows, maybe he will visit you next time?", 
    "A huge fan of broccoli! Kinda suspicious..."],
  "Loaf": [
    "What? You want to know something about me?", 
    "That won't work. I am a mysterious Neko, you know?", 
    "Meow meow meow meow~"],
}

currentResponseKey=None
currentResponseValue=None
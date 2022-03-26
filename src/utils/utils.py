""" Extracts username from the message.
Example: $about:User ---> User
"""
def getMentionedUser(message):
  return (message).split(":")[1].lower().capitalize()

""" Extracts username from the annotation.
Example: $about:@User ---> User
"""
def getAnnotatedUser(message):
  return message.mentions[0].name
  
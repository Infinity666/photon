
from photon import Photon

photon = Photon('mail.sample.yaml')

settings = photon.settings.get['mail']

mail = photon.mail_handler(
    to=settings['recipient'],
    sender=settings['sender'],
    subject=settings['subject'],
    punchline=settings['punchline'],
    add_meta=True
)

###
# Shows the message source so far
print(mail.text)

###
# Add some more text (do this as often as you like):
mail.text = '''
Dear Sir or Madam,
bla bla

No, that's too formal..
'''

###
# Guess what happens here:
mail.send

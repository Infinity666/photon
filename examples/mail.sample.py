
from photon import Photon

p = Photon(config='mail.sample.yaml')

s = p.settings.get['mail']

mail = p.mail_handler(
    s['recipient'],
    sender=s['sender'],
    subject=s['subject'],
    punchline=s['punchline'],
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

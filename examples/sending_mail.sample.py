
from photon import Photon

p = Photon(config='sending_mail.sample.yaml')

s = p.settings.get['mail']

mail = p.new_mail(
    s['recipient'],
    sender=s['sender'],
    subject=s['subject'],
    punchline=s['punchline'],
    add_meta=True
)

print(mail.text)

mail.text = '''
Dear Sir or Madam,
bla bla

No, that's too formal..

'''

mail.send()

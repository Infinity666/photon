
from pprint import pprint
from photon import Photon

p = Photon('ping.sample.yaml')

s = p.settings.get['hosts']

ping = p.ping_handler()


###
# Let's start of with localhost to demonstrate the handling of the probe-function:

a = s['addresses'][0]
ping.probe = a

if ping.probe[a]['up']:
    print('%s is reachable - %s ms rtt in average' %(a, ping.probe[a]['rtt']['avg']))
else:
    print('%s could not be reached!' %(a))

pprint(ping.probe)

print()


###
# You can also pass a complete list to probe.
# The status per host will be overwritten with new information if it encounters the same host again:

ping.probe = s['addresses']
pprint(ping.probe)

print('These are the statistics so far:')
pprint(ping.status)

print()


###
# Another round of pings to demonstrate the handling of the status-function:

ping.probe = s['urls']

if ping.status['ratio'] <= 0.75:
    print('more than three quarters of all addresses are not reachable!!1!')

print('The statistics have changed now:')
pprint(ping.status)

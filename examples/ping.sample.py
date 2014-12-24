
from pprint import pprint
from photon import Photon

photon = Photon('ping.sample.yaml')

hosts = photon.settings.get['hosts']

ping = photon.ping_handler()

###
# Let's start off with localhost to demonstrate the handling of the probe-function:

pprint(hosts)

a = hosts['addresses'][0]
ping.probe = a

if ping.probe[a]['up']:
    print('%s is reachable - %s ms rtt in average' %(a, ping.probe[a]['rtt']['avg']))
else:
    print('%s could not be reached!' %(a))

pprint(ping.probe)

print('-' * 8)


###
# You can also pass a complete list to probe. This will be faster, because the list is processed in parallel.
# The status per host will be overwritten with new information if it encounters the same host again:

ping.probe = hosts['addresses']
pprint(ping.probe)

print('These are the statistics so far:')
pprint(ping.status)

print('-' * 8)


###
# Another round of pings to demonstrate the handling of the status-function:

ping.probe = hosts['urls']

if ping.status['ratio'] <= 0.75:
    print('more than three quarters of all addresses are not reachable!!1!')

print('The statistics have changed now:')
pprint(ping.status)

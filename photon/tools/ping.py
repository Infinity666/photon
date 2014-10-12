
class Ping(object):

    def __init__(self, m, net_if=None):

        super().__init__()

        from ..photon import check_m

        self.m = check_m(m)
        self.__net_if = net_if
        self.__p = dict()

    @property
    def probe(self):

        return self.__p

    @probe.setter
    def probe(self, hosts):

        from re import findall as _findall, search as _search
        from ..util.structures import to_list

        nif = '-I %s' %(self.__net_if) if self.__net_if else ''
        for host in to_list(hosts):
            ping = self.m(
                'trying to reach %s' %(host),
                cmdd=dict(cmd='ping -c 5 %s %s' %(nif, host)),
                critical=False,
                verbose=False
            )

            up = True if ping.get('returncode') == 0 else False
            self.__p[host] = {'up': up}

            if up:
                p = ping.get('out')

                loss = _search('(?P<loss>[\d.]+)[%] packet loss\n', p)
                ms = _findall('time=([\d.]*) ms\n', p)
                rtt = _search('(?P<min>[\d.]+)/(?P<avg>[\d.]+)/(?P<max>[\d.]+)/(?P<stddev>[\d.]+) ms', p)

                self.__p[host].update(dict(ms=ms, loss=loss.group('loss'), rtt=rtt.groupdict()))

    @property
    def status(self):

        num=len(self.probe)
        up=len([h for h in self.probe if self.probe[h]['up']])
        ratio=up/num

        return dict(num=num, up=up, down=num-up, ratio=ratio)

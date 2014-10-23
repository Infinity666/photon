
class Ping(object):
    '''
    The Ping tool helps to send pings, returning detailed results each probe, and calculates a summary of all probes.

    :param six: Either use ``ping`` or ``ping6``
    :param net_if: Specify network interface to send pings from
    :param num: How many pings to send each probe
    '''

    def __init__(self, m, six=False, net_if=None, num=5):
        super().__init__()

        from ..photon import check_m

        self.m = check_m(m)
        self.__six = six
        self.__net_if = net_if
        if num < 1: num = 1
        self.__num = num
        self.__p = dict()

        self.m('ping tool startup done', more=dict(six=self.__six, net_if=self.__net_if, num=self.__num), verbose=False)

    @property
    def probe(self):
        '''
        :param hosts: One or a list of hosts (URLs, IP-addresses)
        :returns: A dictionary with all hosts probed as keys specified as following:

        * 'up': ``True`` or ``False`` depending if ping was successful
        * 'loss': The packet loss as list (if 'up')
        * 'ms': A list of times each packet sent (if 'up')
        * 'rtt': A dictionary with the fields *avg*, *min*, *max* & *stddev* (if 'up')
        '''

        return self.__p

    @probe.setter
    def probe(self, hosts):
        '''
        .. seealso:: :attr:`probe`
        '''

        from re import findall as _findall, search as _search
        from ..util.structures import to_list

        pingc = 'ping6' if self.__six else 'ping'
        nif = '-I %s' %(self.__net_if) if self.__net_if else ''
        for host in to_list(hosts):
            ping = self.m(
                'trying to reach %s' %(host),
                cmdd=dict(cmd='%s -c %d %s %s' %(pingc, self.__num, nif, host)),
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

                if loss: loss = loss.group('loss')
                self.__p[host].update(dict(ms=ms, loss=loss, rtt=rtt.groupdict()))

    @property
    def status(self):
        '''
        :returns: A dictionary with the following:

        * 'num': Total number of hosts already probed
        * 'up': Number of hosts up
        * 'down': Number of hosts down
        * 'ratio': Ratio between 'up'/'down' as float

        Ratio:

        * ``100%`` up == `1.0`
        * ``10%`` up == `0.1`
        * ``0%`` up == `0.0`
        '''


        num=len(self.probe)
        up=len([h for h in self.probe if self.probe[h]['up']])
        ratio=up/num

        return dict(num=num, up=up, down=num-up, ratio=ratio)

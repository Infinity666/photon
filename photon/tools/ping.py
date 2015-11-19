from multiprocessing import cpu_count as _cpu_count
from multiprocessing.dummy import Pool as _Pool
from re import findall as _findall
from re import search as _search

from photon.photon import check_m
from photon.util.structures import to_list

rxlss = '(?P<loss>[\d.]+)[%] packet loss\n'
rxmst = 'time=([\d.]*) ms\n'
rxrtt = '(?P<min>[\d.]+)/(?P<avg>[\d.]+)/(?P<max>[\d.]+)/(?P<stddev>[\d.]+) ms'


class Ping(object):
    '''
    The Ping tool helps to send pings, returning detailed results each probe,
    and calculates a summary of all probes.

    :param six:
        Either use ``ping`` or ``ping6``
    :param net_if:
        Specify network interface to send pings from
    :param num:
        How many pings to send each probe
    :param packetsize:
        Specifies the number of data bytes to be sent
    :param max_pool_size:
        Hosts passed to :func:`probe` in form of a list,
        will be processed in parallel.
        Specify the maximum size of the thread pool workers here.
        If skipped, the number of current CPUs is used
    '''

    def __init__(self, m, six=False, net_if=None, num=5,
                 packetsize=None, max_pool_size=None):
        super().__init__()

        self.m = check_m(m)
        self.__ping_cmd = 'ping6' if six else 'ping'
        self.__net_if = '-I %s' % (net_if) if net_if else ''

        if not num:
            num = 1
        self.__num = '-c %d' % (num)

        if not packetsize:
            packetsize = ''
        if packetsize and packetsize > 1:
            packetsize = '-s %s' % (packetsize)
        self.__packetsize = packetsize

        if not max_pool_size:
            max_pool_size = _cpu_count()
        if max_pool_size < 1:
            max_pool_size = 1
        self.__max_pool_size = max_pool_size

        self.__probe_results = dict()

        self.m(
            'ping tool startup done',
            more=dict(
                pingc=self.__ping_cmd,
                net_if=self.__net_if,
                num=self.__num
            ),
            verbose=False
        )

    @property
    def probe(self):
        '''
        :param hosts:
            One or a list of hosts (URLs, IP-addresses) to send pings to

            * If you need to check multiple hosts, it is best \
            to pass them together as a list.

            * This will probe all hosts in parallel, \
            with ``max_pool_size`` workers.

        :returns:
            A dictionary with all hosts probed as keys specified as following:

        * 'up': ``True`` or ``False`` depending if ping was successful
        * 'loss': The packet loss as list (if 'up')
        * 'ms': A list of times each packet sent (if 'up')
        * 'rtt': A dictionary with the fields \
        *avg*, *min*, *max* & *stddev* (if 'up')
        '''

        return self.__probe_results

    @probe.setter
    def probe(self, hosts):
        '''
        .. seealso:: :attr:`probe`
        '''

        def __send_probe(host):
            ping = self.m(
                '',
                cmdd=dict(
                    cmd=' '.join([
                        self.__ping_cmd,
                        self.__num,
                        self.__net_if,
                        self.__packetsize,
                        host
                    ])
                ),
                critical=False,
                verbose=False
            )

            up = True if ping.get('returncode') == 0 else False
            self.__probe_results[host] = {'up': up}

            if up:
                p = ping.get('out')

                loss = _search(rxlss, p)
                ms = _findall(rxmst, p)
                rtt = _search(rxrtt, p)

                if loss:
                    loss = loss.group('loss')
                self.__probe_results[host].update(dict(
                    ms=ms,
                    loss=loss,
                    rtt=rtt.groupdict()
                ))

        hosts = to_list(hosts)
        pool_size = (
            len(hosts)
            if len(hosts) <= self.__max_pool_size else
            self.__max_pool_size
        )

        pool = _Pool(pool_size)
        pool.map(__send_probe, hosts)
        pool.close()
        pool.join()

    @property
    def status(self):
        '''
        :returns:
            A dictionary with the following:

        * 'num': Total number of hosts already probed
        * 'up': Number of hosts up
        * 'down': Number of hosts down
        * 'ratio': Ratio between 'up'/'down' as float

        Ratio:

        * ``100%`` up == `1.0`
        * ``10%`` up == `0.1`
        * ``0%`` up == `0.0`
        '''

        num = len(self.probe)
        up = len([h for h in self.probe if self.probe[h]['up']])
        ratio = up/num if num != 0 else 0  # over 9000!

        return dict(num=num, up=up, down=num-up, ratio=ratio)

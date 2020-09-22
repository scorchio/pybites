from dateutil.parser import parse
from operator import itemgetter

MAC1 = """
reboot    ~                         Wed Apr 10 22:39
reboot    ~                         Wed Mar 27 16:24
reboot    ~                         Wed Mar 27 15:01
reboot    ~                         Sun Mar  3 14:51
reboot    ~                         Sun Feb 17 11:36
reboot    ~                         Thu Jan 17 21:54
reboot    ~                         Mon Jan 14 09:25
"""


def calc_max_uptime(reboots):
    """Parse the passed in reboots output,
       extracting the datetimes.

       Calculate the highest uptime between reboots =
       highest diff between extracted reboot datetimes.

       Return a tuple of this max uptime in days (int) and the
       date (str) this record was hit.

       For the output above it would be (30, '2019-02-17'),
       but we use different outputs in the tests as well ...
    """
    reboot_times = []
    for line in reboots.splitlines():
        if 'reboot' in line:
            reboot_time = line.split('~')[1].strip()
            reboot_times.append(parse(reboot_time))

    uptimes = []
    for idx, reboot_time in enumerate(reboot_times[:-1]):
        diff = reboot_time - reboot_times[idx+1]
        uptimes.append((diff, reboot_time))

    top_uptime = max(uptimes, key=itemgetter(0))
    
    return (top_uptime[0].days, top_uptime[1].strftime('%Y-%m-%d'))

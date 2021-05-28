from urllib.request import urlopen
from Location import Location
from json import load

knownId = {}


def ipInfo(addr):
    url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    data = load(res)

    return data['city'], data['country']


def checkIp(sid, location):
    global knownId
    if sid not in knownId:
        knownId.update({sid: Location(location)})
        return location, 'Unknown id :: '+sid
    if knownId[sid].isLocationKnown(location) is False:
        return location, 'Unknown location'
    return location, 'OK'


def handleNewIp(sid, ip):
    infos = ipInfo(ip)
    if infos == '':
        raise ValueError('cannot retrieve ip location')
    return checkIp(sid, infos)


if __name__ == "__main__":
    ips = ["185.223.151.250", "185.223.151.250",
           "185.223.20.250", "185.223.151.250", "185.100.151.250"]

    for ip in ips:
        print("from "+ip, end=" :: ")
        print(handleNewIp('wow such id', ip))

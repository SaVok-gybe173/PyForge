import socks
import socket
import time
import requests
from bs4 import BeautifulSoup
import subprocess
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
# pip install requests beautifulsoup4 pysocks


def get_proxies(limit=20):
    try:
        r = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all', timeout=10)
        lines = [l.strip() for l in r.text.split('\n') if ':' in l]
        return [(l.split(':')[0], int(l.split(':')[1])) for l in lines[:limit]]
    except:
        return [('185.217.124.170', 1080), ('45.79.241.240', 1080)]

def check_proxies(target, proxies, port=80, timeout=5):
    def test(p):
        ip, pr = p
        start = time.time()
        try:
            s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            s.set_proxy(socks.SOCKS5, ip, pr, rdns=True)
            s.settimeout(timeout)
            s.connect((target, port))
            lat = round((time.time() - start) * 1000, 2)
            s.close()
            return p, {'status': 'ok', 'latency': lat}
        except:
            return p, {'status': 'fail', 'latency': None}
    res = {}
    with ThreadPoolExecutor(max_workers=min(len(proxies), 20)) as ex:
        for f in as_completed([ex.submit(test, pr) for pr in proxies]):
            p, r = f.result()
            res[p] = r
    return res


def check_proxies_(target, proxies, port=80, timeout=5):
    """
    Для каждого прокси (ip, port) пытается установить TCP-соединение через SOCKS5
    к target_ip:port. Возвращает словарь:
    {
        (proxy_ip, proxy_port): {
            'status': 'success' | 'failed',
            'latency_ms': float | None,
            'error': str | None
        }
    }
    """
    def test(p):
        ip,pr=p; start=time.time()
        try:
            s=socks.socksocket(socket.AF_INET,socket.SOCK_STREAM)
            s.set_proxy(socks.SOCKS5,ip,pr,rdns=True)
            s.settimeout(timeout)
            s.connect((target,port))
            lat=(time.time()-start)*1000
            s.close()
            return p,{'status':'ok','latency':round(lat,2)}
        except:
            return p,{'status':'fail','latency':None}
    res={}
    with ThreadPoolExecutor(max_workers=min(len(proxies),20)) as ex:
        for p,r in as_completed([ex.submit(test, pr) for pr in proxies]):
            res[p]=r
    return res

def ping(ip, port=None, timeout=3):
    """Возвращает задержку в мс или None."""
    if port is None:
        try:
            param = '-n' if sys.platform == 'win32' else '-c'
            out = subprocess.check_output(['ping', param, '1', ip], timeout=timeout, stderr=subprocess.DEVNULL)
            text = out.decode('cp866' if sys.platform == 'win32' else 'utf-8', errors='ignore')
            # Ищем "время=28мс" или "time=28 ms"
            m = re.search(r'(?:время|time)[=: ](\d+\.?\d*)', text, re.I)
            return float(m.group(1)) if m else None
        except:
            return None
    else:
        t = time.time()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((ip, port))
            sock.close()
            return round((time.time() - t) * 1000, 2)
        except:
            return None

def init(ip, port):
    socks.set_default_proxy(socks.SOCKS5, ip, port, rdns=True)
    socket.socket = socks.socksocket

def init_ip_proxies(target, proxies):
    if not ping(target):
        working = sorted(
        [(p, info['latency']) for p, info in check_proxies(target, proxies, port=80, timeout=5).items() if info['status'] == 'ok'],
        key=lambda x: x[1])
        if working:
            socket_copy = socket.socket
            (ip, port), latency = working[0]
            init(ip, port)
            try:
                requests.get('https://api.ipify.org', timeout=10)
            except Exception as e:
                socket.socket = socket_copy
                return False
        return False


    return True

if __name__ == '__main__':
    import sys

    # 1. Получаем список прокси (первые 5)
    proxies = get_proxies(limit=5)
    print(f"Получено прокси: {proxies}")

    # 2. Проверяем, какие из них могут соединиться с 195.208.119.133:80
    target = '195.208.119.133'  # IP из вашего вопроса
    results = check_proxies(target, proxies, port=80, timeout=5)

    print("\nРезультаты проверки:")
    for (ip, port), info in results.items():
        if info['status'] == 'success':
            print(f"✓ {ip}:{port} -> задержка {info['latency_ms']} мс")
        else:
            print(f"✗ {ip}:{port} -> ошибка: {info['error']}")

    # 3. Пинг до целевого IP (TCP на порт 80 и ICMP)
    print(f"\nTCP ping до {target}:80 = {ping(target, port=80)} мс")
    print(f"ICMP ping до {target} = {ping(target)} мс")
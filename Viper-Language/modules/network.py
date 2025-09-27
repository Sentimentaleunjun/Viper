import socket

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

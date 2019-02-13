import hashlib


def hashencrypt(source):
    m = hashlib.md5()
    m.update(source.encode())
    return m.hexdigest()
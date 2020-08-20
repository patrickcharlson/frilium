import hashlib


def get_hash(bytes_iter):
    assert not isinstance(
        bytes_iter, (str, bytes))

    md5 = hashlib.md5()

    for b in bytes_iter:
        md5.update(b)

    return md5.hexdigest()

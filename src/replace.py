from src.regex import single_byte, multi_byte


def range_matcher(lower, higher):
    return lambda chr: chr >= lower and chr <= higher


def matcher(match):
    return lambda chr: chr == match


def range(str):
    """Turns a string into a character matcher

    input \uD80A matches only that number
    input \uD80A\uD80B matches either the first or the last
    input \uD80A-\uD80B matches including the the first and last
    input \uD80A\uD80C-\uD80D matches the first char and the range for the
        second chars
    """
    str_len = len(str)
    str_pos = 0
    res = []
    while str_pos < str_len:
        if str_pos < str_len - 1 and str[str_pos + 1] == '-':
            res.append(range_matcher(ord(str[str_pos]), ord(str[str_pos + 2])))
            str_pos += 3
        else:
            res.append(matcher(ord(str[str_pos])))
            str_pos += 1
    if len(res) == 1:
        return res[0]

    def chk(chr):
        return next(filter(lambda fn: fn(chr), res), None) is not None

    return chk


def mb_range(tuple):
    lower, higher = tuple
    return range(lower), range(higher)


single = range(single_byte)
multi = list(map(mb_range, multi_byte))


def read(b, i):
    return b[i] | b[i + 1] << 8


def multi_match(num):
    for lower, higher in multi:
        match = lower(num)
        if match:
            return higher
    return None


def replace(str):
    b = str.encode('utf-16-le')
    b_pos = 0
    b_len = len(b)
    res = []
    while b_pos < b_len:
        byte_16 = read(b, b_pos)
        b_pos += 2
        if byte_16 == 32:  # ' ' to '-'
            res.append(45)
            res.append(0)
            continue
        if single(byte_16):
            # remove single match characters
            continue
        matcher = multi_match(byte_16)
        if matcher is not None:
            if b_pos == b_len:
                break
            next = read(b, b_pos)
            if matcher(next):
                b_pos += 2
                continue
        # append characters that match neighter 16 nor 32
        res.append(byte_16 & 0xff)
        res.append(byte_16 >> 8)

    return bytes(res).decode('utf-16-le')

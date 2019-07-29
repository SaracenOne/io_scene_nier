import struct

class Float:
    """
    halftofloat - author fpmurphy from
    http://forums.devshed.com/python-programming-11
    /converting-half-precision-floating-point-numbers-from-hexidecimal-to-decimal-576842.html
    """ 
    @staticmethod
    def HalfToFloat(h):
        s = int((h >> 15) & 0x00000001) # sign
        e = int((h >> 10) & 0x0000001f) # exponent
        f = int(h & 0x000003ff) # fraction

        if e == 0:
            if f == 0:
                return int(s << 31)
            else:
                while not (f & 0x00000400):
                    f <<= 1
                    e -= 1
                e += 1
                f &= ~0x00000400
        elif e == 31:
            if f == 0:
                return int((s << 31) | 0x7f800000)
            else:
                return int((s << 31) | 0x7f800000 | (f << 13))

        e = e + (127 -15)
        f = f << 13
        return int((s << 31) | (e << 23) | f)

    @staticmethod
    def ConvertHalf2Float(h):
        id = Float.HalfToFloat(h)
        str = struct.pack('I',id)
        return struct.unpack('f', str)[0]
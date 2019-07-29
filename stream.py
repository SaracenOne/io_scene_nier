import struct

class Stream:
    SEEK_ABS = 0
    SEEK_REL = 1
    SEEK_END = 2

    @staticmethod
    def ReadCString(f):
        buf = b''
        while(True):
            char = struct.unpack('c', f.read(1))[0]
            if char == b'\x00':
                break
            else:
                buf += char
        return buf.decode('ascii')

    @staticmethod
    def ReadFixedString(f, len):
        buf = f.read(len)
        if not buf:
            return ""

        return buf.decode('ascii')

    @staticmethod
    def Read8SInteger(f):
        buf = f.read(1)
        if not buf:
            return 0
        return struct.unpack('b', buf)[0]

    @staticmethod
    def Read8UInteger(f):
        buf = f.read(1)
        if not buf:
            return 0
        return struct.unpack('B', buf)[0]

    @staticmethod
    def Read16SIntegerBE(f):
        buf = f.read(2)
        if not buf:
            return 0
        return struct.unpack('>h', buf)[0]

    @staticmethod
    def Read16UIntegerBE(f):
        buf = f.read(2)
        if not buf:
            return 0
        return struct.unpack('>H', buf)[0]


    @staticmethod
    def Read32SIntegerBE(f):
        buf = f.read(4)
        if not buf:
            return 0
        return struct.unpack('>i', buf)[0]

    @staticmethod
    def Read32UIntegerBE(f):
        buf = f.read(4)
        if not buf:
            return 0
        return struct.unpack('>I', buf)[0]

    @staticmethod
    def Read32SIntegerBEArray(f, count):
        array = []
        for i in range(count):
            array.append(Stream.Read32SIntegerBE(f))

        return array

    @staticmethod
    def Read32UIntegerBEArray(f, count):
        array = []
        for i in range(count):
            array.append(Stream.Read32UIntegerBE(f))

        return array

    @staticmethod
    def Read32FloatBE(f):
        buf = f.read(4)
        if not buf:
            return 0
        return struct.unpack('>f', buf)[0]

    @staticmethod
    def Read32FloatBEArray(f, count):
        array = []
        for i in range(count):
            array.append(Stream.Read32FloatBE(f))

        return array

    @staticmethod
    def SeekAlign(f, pad):
        if f.tell() % pad == 0:
            return
        abs_offset = (f.tell() // pad + 1) * pad
        f.seek(abs_offset, Stream.SEEK_ABS)

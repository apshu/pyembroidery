from .ReadHelper import signed8, read_int_8, read_int_24be
from .EmbThread import EmbThread


def read(f, out, settings=None):
    f.seek(0x20E, 0)
    while True:
        if read_int_8(f) == 0x45:
            thread = EmbThread()
            thread.color = read_int_24be(f)
            read_int_8(f)  # Should be 0x20 " "
            out.add_thread(thread)
        else:
            break
    f.seek(0x600, 0)

    count = 0
    while True:

        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        x = byte[0]
        y = byte[1]
        ctrl = byte[2]
        if ctrl == 0x80:
            out.stitch(signed8(x), -signed8(y))
        elif ctrl == 0x81:
            if count > 1:
                out.color_change()
        elif ctrl == 0x90:
            if x == 0 and y == 0:
                out.trim()
            else:
                out.move(signed8(x), -signed8(y))
        elif ctrl == 0x8F:
            out.end()
            return
        count += 1
    out.end()
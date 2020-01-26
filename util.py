import struct
import imghdr
from fpdf import FPDF


def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0)  # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception:  # IGNORE:W0703
                return
        else:
            return
        return width, height

# >>> pdf = FPDF()
# >>> pdf.add_page()
# >>> pdf.image('2.jpg',0,0,210,297)
# >>> pdf.output('hello5.pdf',"F")


def make_pdf(filename, imagelist):
    pdf = FPDF('P', 'mm', (210, 297))
    # imagelist is the list with all image filenames
    for imagename in imagelist:
        size = get_image_size(imagename)
        # print size
        if size[0] < size[1]:
            pdf.add_page('P')
            pdf.image(imagename, 0, 0, 210, 297)
        else:
            pdf.add_page('L')
            pdf.image(imagename, 0, 0, 297, 210)
    pdf.output(filename+".pdf", "F")

import os

crcTable = [0x0000,0xC0C1,0xC181,0x0140,0xC301,0x03C0,0x0280,0xC241,0xC601,0x06C0,0x0780,0xC741,0x0500,0xC5C1,0xC481,0x0440,0xCC01,0x0CC0,0x0D80,0xCD41,0x0F00,0xCFC1,0xCE81,0x0E40,0x0A00,0xCAC1,0xCB81,0x0B40,0xC901,0x09C0,0x0880,0xC841,0xD801,0x18C0,0x1980,0xD941,0x1B00,0xDBC1,0xDA81,0x1A40,0x1E00,0xDEC1,0xDF81,0x1F40,0xDD01,0x1DC0,0x1C80,0xDC41,0x1400,0xD4C1,0xD581,0x1540,0xD701,0x17C0,0x1680,0xD641,0xD201,0x12C0,0x1380,0xD341,0x1100,0xD1C1,0xD081,0x1040,0xF001,0x30C0,0x3180,0xF141,0x3300,0xF3C1,0xF281,0x3240,0x3600,0xF6C1,0xF781,0x3740,0xF501,0x35C0,0x3480,0xF441,0x3C00,0xFCC1,0xFD81,0x3D40,0xFF01,0x3FC0,0x3E80,0xFE41,0xFA01,0x3AC0,0x3B80,0xFB41,0x3900,0xF9C1,0xF881,0x3840,0x2800,0xE8C1,0xE981,0x2940,0xEB01,0x2BC0,0x2A80,0xEA41,0xEE01,0x2EC0,0x2F80,0xEF41,0x2D00,0xEDC1,0xEC81,0x2C40,0xE401,0x24C0,0x2580,0xE541,0x2700,0xE7C1,0xE681,0x2640,0x2200,0xE2C1,0xE381,0x2340,0xE101,0x21C0,0x2080,0xE041,0xA001,0x60C0,0x6180,0xA141,0x6300,0xA3C1,0xA281,0x6240,0x6600,0xA6C1,0xA781,0x6740,0xA501,0x65C0,0x6480,0xA441,0x6C00,0xACC1,0xAD81,0x6D40,0xAF01,0x6FC0,0x6E80,0xAE41,0xAA01,0x6AC0,0x6B80,0xAB41,0x6900,0xA9C1,0xA881,0x6840,0x7800,0xB8C1,0xB981,0x7940,0xBB01,0x7BC0,0x7A80,0xBA41,0xBE01,0x7EC0,0x7F80,0xBF41,0x7D00,0xBDC1,0xBC81,0x7C40,0xB401,0x74C0,0x7580,0xB541,0x7700,0xB7C1,0xB681,0x7640,0x7200,0xB2C1,0xB381,0x7340,0xB101,0x71C0,0x7080,0xB041,0x5000,0x90C1,0x9181,0x5140,0x9301,0x53C0,0x5280,0x9241,0x9601,0x56C0,0x5780,0x9741,0x5500,0x95C1,0x9481,0x5440,0x9C01,0x5CC0,0x5D80,0x9D41,0x5F00,0x9FC1,0x9E81,0x5E40,0x5A00,0x9AC1,0x9B81,0x5B40,0x9901,0x59C0,0x5880,0x9841,0x8801,0x48C0,0x4980,0x8941,0x4B00,0x8BC1,0x8A81,0x4A40,0x4E00,0x8EC1,0x8F81,0x4F40,0x8D01,0x4DC0,0x4C80,0x8C41,0x4400,0x84C1,0x8581,0x4540,0x8701,0x47C0,0x4680,0x8641,0x8201,0x42C0,0x4380,0x8341,0x4100,0x81C1,0x8081,0x4040]

template = str()
with open('config.txt', 'r') as f:
    for line in f.readlines():
        key, value = line.split('=')
        if key == 'template':
            template = value.strip()

config_file = '{}.fwd'.format(template)

offset = 0
gamepath_length = 0
banner_start_location = 0
with open('data/{}'.format(config_file), 'r') as f:
    for line in f.readlines():
        key, value = line.split('=')
        if key == 'gamepath_location':
            offset = int(value, 16)
        elif key == 'gamepath_length':
            gamepath_length = int(value)
        elif key == 'banner_location':
            banner_start_location = int(value, 16)

titles = dict()
with open('title.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        key, value = line.split('\t')
        titles[key] = value.replace('\\n', '\n').strip()


# default returned value is array
# If second param is True then returning single value
def crc16(in_data, to_int=False):
    crc = [0xff, 0xff]
    for datum in in_data:
        ncrc = crcTable[(crc[0] ^ datum)]
        crc[0] = (ncrc & 0x00FF) ^ crc[1]
        crc[1] = ncrc >> 8
    if to_int:
        return crc[0]*256 + crc[1]
    return crc


def get_length_bytes(path, start, length):
    header = bytes()
    with open(path, 'rb') as f:
        f.seek(start)
        for i in range(0, length):
            header += f.read(1)
    return header


def get_bytes(path, start, end):
    header = bytes()
    with open(path, 'rb') as f:
        f.seek(start)
        for i in range(0, end + 0x1 - start):
            header += f.read(1)
    return header


def bytes_to_hex_string(values):
    hex_string = '0x'
    for i in range(0, len(values)):
        temp2 = hex(temp[i]).replace('0x', '')
        if len(temp2) == 1:
            temp2 = '0{}'.format(temp2)
        hex_string += temp2
    return hex_string


for file in os.listdir('Games'):
    dat_name = str()    # datName
    game_path = str()   # gamePath
    custom_tid = str()  # customTID
    mode = str()        # mode
    game_title = str()  # gameTitle

    # find title
    release_num = file.split('-')[0].strip()
    title = titles.get(release_num)
    if not title:
        print('Cannot found title in text. {}'.format(file))
        continue

    # parseDatName
    nombre = file.upper().replace('.NDS', '')
    six = str()
    for i in range(0, len(nombre)):
        c = nombre[i]
        if 'A' <= c <= 'Z' or '0' < c <= '9':
            six += c
    while len(six) < 6:
        six += '0'
    dat_name = six[0:6]
    game_path = 'Games/{}'.format(file)

    # setCustomTID
    header = get_bytes(game_path, 0x0C, 0x0F)
    for new_char in header:
        if new_char < 0:
            new_char = new_char & 0xff
        custom_tid += chr(new_char)

    # setMode
    header = get_bytes(game_path, 0x12, 0x12)
    mode = 'NTR' if header[0] == 0 else 'TWL'

    # setGameTitle
    header = get_bytes(game_path, 0x00, 0x0B)
    for new_char in header:
        if new_char < 0:
            new_char = new_char & 0xff
        game_title += chr(new_char)

    # copyROMHeaderToTemplate
    rom_header = bytearray(get_bytes(game_path, 0x0, 0x11))
    with open('data/{}.nds'.format(template), 'rb') as f:
        template_bytes = bytearray(f.read())
    for i in range(0, len(rom_header)):
        template_bytes[i] = rom_header[i]

    # writeGameTitle
    game_title_bytes = game_title.encode('utf-8')
    for i in range(0x0, 0xC):
        template_bytes[i] = game_title_bytes[i]

    # writeReverseTID
    counter = 0
    temp = bytearray(get_bytes(game_path, 0x0C, 0x0F))
    temp.reverse()
    for i in range(0x230, 0x230 + 0x4):
        template_bytes[i] = temp[counter]
        counter += 1

    # banner copy
    temp = bytearray(get_bytes(game_path, 0x68, 0x68 + 0x03))
    temp.reverse()
    banner_location = int(bytes_to_hex_string(temp), 0)
    banner_bytes = bytearray(get_length_bytes(game_path, banner_location, 0x23C0))

    counter = 0
    start_init = banner_start_location
    while counter < 0x23C0:
        try:
            template_bytes[start_init] = banner_bytes[counter]
        except IndexError:
            template_bytes[start_init] = 0
        counter += 1
        start_init += 1

    # banner text
    start_init = banner_start_location + 0x240
    banner_name = bytearray(title.encode('utf-16le'))
    for _ in range(0, 8):
        for i in range(0, 0x100):
            try:
                template_bytes[start_init] = banner_name[i]
            except IndexError:
                template_bytes[start_init] = 0
            start_init += 1

    # banner crc16
    data = template_bytes[banner_start_location + 0x20:banner_start_location + 0x83F + 0x01]
    crc = crc16(data, True).to_bytes(2, byteorder="big")
    template_bytes[banner_start_location+0x02] = crc[0]
    template_bytes[banner_start_location+0x03] = crc[1]

    data = template_bytes[banner_start_location + 0x20:banner_start_location + 0x93F + 0x01]
    crc = crc16(data, True).to_bytes(2, byteorder="big")
    template_bytes[banner_start_location+0x04] = crc[0]
    template_bytes[banner_start_location+0x05] = crc[1]

    data = template_bytes[banner_start_location + 0x20:banner_start_location + 0xA3F + 0x01]
    crc = crc16(data, True).to_bytes(2, byteorder="big")
    template_bytes[banner_start_location+0x06] = crc[0]
    template_bytes[banner_start_location+0x07] = crc[1]

    data = template_bytes[banner_start_location + 0x1240:banner_start_location + 0x23BF + 0x01]
    crc = crc16(data, True).to_bytes(2, byteorder="big")
    template_bytes[banner_start_location+0x08] = crc[0]
    template_bytes[banner_start_location+0x09] = crc[1]

    # writeGamePath
    counter = 0
    offset_counter = offset
    game_path_bytes = game_path.encode('utf-8')
    while counter < gamepath_length:
        try:
            template_bytes[offset_counter] = game_path_bytes[counter]
        except IndexError:
            template_bytes[offset_counter] = 0
        counter += 1
        offset_counter += 1

    # generateCIA
    data = template_bytes[0x0:0x15E]
    crc = crc16(data, True).to_bytes(2, byteorder="big")
    template_bytes[0x15E] = crc[0]
    template_bytes[0x15F] = crc[1]
    file_name = 'output/{}.nds'.format(file[0:-4])
    with open(file_name, 'wb') as f:
        f.write(template_bytes)
    os.system('data\\make_cia.exe --srl="{}"'.format(file_name))
    os.remove(file_name)

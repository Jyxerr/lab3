import math
from struct import pack

with open ('test', 'wb') as file_bmp:

    width = 512
    height = 512

    file_bmp.write(b'BM')
    file_bmp.write(pack('<L2HL', 0, 0, 0, 62))
    # We wrote BITMAPFILEHEADER in our file

    file_bmp.write(pack('<3L2H6L', 40, width, height, 1, 1, 0, 0, 0, 0, 0, 0))
    # We wrote BITMAPINFOHEADER in our file

    file_bmp.write(pack('<2L',
                        int.from_bytes(b'\xff\xff\xff', byteorder='little'),
                        int.from_bytes(b'\x00\00\xff', byteorder='little')))
    # We wrote Color Pallet

    plane = []

    for i in range(width):
        plane.append([])
        for j in range(height):
            plane[i].append(0)
    # Plane filled with zeros

    t = 0

    while t < 2 * math.pi + math.pi / 2500:
        x = math.sin(3 * t + math.pi / 2)
        y = math.sin(2 * t)

        if x >= -255/256 and y >= -255/256:
            plane[255+round(256.*x)][255+round(256.*y)] = 1
        # We wrote x,y on our plane

        t += math.pi / 2500

    byte_in_decimal = 0
    power_of_two = 7

    for i in range(height):
        for j in range(width):
            if power_of_two == 0:
                byte_in_decimal += plane[j][i]
                file_bmp.write((byte_in_decimal).to_bytes(1, 'little'))
                # We wrote byte in bmp file

                byte_in_decimal = 0
                power_of_two = 7
                # We returned the counters to their original position

            else:
                byte_in_decimal += plane[j][i]*pow(2, power_of_two)
                power_of_two -= 1
                # Finding the byte value in decimal form

with open('test', 'rb') as file_bmp:
    with open('chart.bmp', 'wb') as picture:
        bmp_internals = file_bmp.read()
        picture.write(bmp_internals)
        # We drawn bmp picture




import math
from struct import pack

with open ('chart.bmp', 'wb') as file_bmp:

    width = 512
    height = 512

    # Writing BITMAPFILEHEADER in our file
    file_bmp.write(b'BM')
    file_bmp.write(pack('<L2HL', 0, 0, 0, 62))

    # Writing BITMAPINFOHEADER in our file
    file_bmp.write(pack('<3L2H6L', 40, width, height, 1, 1, 0, 0, 0, 0, 0, 0))

    # Writing Color Pallet
    file_bmp.write(pack('<2L',
                        int.from_bytes(b'\xff\xff\xff', byteorder='little'),
                        int.from_bytes(b'\x00\00\xff', byteorder='little')))

    plane = []

    # Filling plane with zeros
    for i in range(width):
        plane.append([])
        for j in range(height):
            plane[i].append(0)

    t = 0
    # We use 256 cells in table for '+', 1 cell to '0' and 255 for '-'
    # so minimum '-' coordinate = -255/256
    minimal_coordinate = -255/256
    points_interval = math.pi/2500

    while t < 2 * math.pi + points_interval:
        x = math.sin(3*t + math.pi/2)
        y = math.sin(2*t)

        # Writing x,y on our plane
        if x >= minimal_coordinate and y >= minimal_coordinate:
            plane[255 + round(256.*x)][255 + round(256.*y)] = 1

        t += points_interval

    byte_in_decimal = 0
    power_of_two = 7

    for i in range(height):
        for j in range(width):
            if power_of_two == 0:
                # Writing byte in bmp file
                byte_in_decimal += plane[j][i]
                file_bmp.write((byte_in_decimal).to_bytes(1, 'little'))

                # Returning the counters to their original position
                byte_in_decimal = 0
                power_of_two = 7

            else:
                # Finding the byte value in decimal form
                byte_in_decimal += plane[j][i] * pow(2, power_of_two)
                power_of_two -= 1
                


# args:
# 1 - Arquivo a ser escondido
# 2 - Resolucao X do arquivo final
# 3 - Resolucao Y do arquivo final
# 4 - Resolucao Z do arquivo final
# 5 - Caminho para as fatias (lembre de sempre terminar em /)

import json
from sys import argv
from random import randrange,seed
from PIL import Image
import bitarray
import struct

seed("Secomp")

# Preparando Informacao - pt1

print("Convertendo arquivo para array de bits....",end='')

bits = bitarray.bitarray()

voxel_map = {}

with open(argv[1], 'rb') as file:
    bits.fromfile(file)

print('ok')

# Preparando Informacao - pt2

print('convertendo array de bits para string de ints...',end='')

bigstring = ""
for i in range(0,len(bits),8):
    if(len(bits[i * 8:i * 8 + 8])):
        bigstring += str(int(bits[i*8:i*8+8].to01(), 2))
    
print("ok")
# Preparando Informacao - pt2

intial_x, initial_y, initial_z = 0, 0, 0

x_max, y_max, z_max = int(argv[2]), int(argv[3]), int(argv[4])
print("gerando mapa de voxels...",end='')

def check_next(x, y, z):
    return (x, y, z) in voxel_map.keys()


def set_next(x, y, z, b, nx, ny, nz):
    #print(x, y, x, '->', nx, ny, nz)
    voxel_map.update({(x, y, z): [b, (nx, ny, nz)]})


def set_bit(v, index, x):
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask         # If x was True, set the bit indicated by the mask.
    return v            # Return the result, we're done.


next_x, next_y, next_z = 0, 0, 1
bit_count = 0
for i in bigstring:
    bit_count+=1
    last_x, last_y, last_z = next_x, next_y, next_z
    continua = True
    while continua:
        next_x = randrange(0, x_max) % 256
        next_y = randrange(0, y_max) % 256
        next_z = randrange(1, z_max) % 256
        if next_z == 0:
            next_z += randrange(1,240)
        continua = check_next(next_x, next_y, next_z)
    set_next(last_x, last_y, last_z, int(i), next_x, next_y, next_z)
    print('\r' + str((bit_count / len(bigstring)) * 100) + ' % ',end='')
print('                           ')
print('ok')

# Armazenando Informacao

print('salvando informacoes no paralelepipedo')

path = argv[5]
end_path = argv[6]
def set_voxel(x, y, z, next_x, next_y, sb):
    with Image.open(path + str(z) + '.png',mode="r") as hyperplane:
        map2d = hyperplane.load()
        map2d[x, y] = (next_x, next_y, sb)
        hyperplane.save(end_path + str(z) + '.png','PNG')

count = 0
for index in voxel_map:
    count += 1
    print('\r'+str(count/(len(voxel_map))*100),end='')
    set_voxel(index[0], index[1], index[2], voxel_map[index][1][0], voxel_map[index][1][1], voxel_map[index][0])

print('ok')

'''
Esse programa foi desenvolvido pela dubpla: Victor Guerra Veloso(2658) e Athena Sarantôpoulos()
'''

from assembler import *
texto = readFile("meu.asm")
print (decodeAsm(texto))
#writeFile("meu.bin",texto)

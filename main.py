'''
Esse programa foi desenvolvido pela dubpla: Victor Guerra Veloso(2658) e Athena Sarantôpoulos()
'''
from assembler import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("ArquivoDeEntrada", help="Caminho/Nome do arquivo assembly a ser montado")
parser.add_argument("-o", "--output", type=str, help="Nome do arquivo de saída")
args = parser.parse_args()
texto = readFile(args.ArquivoDeEntrada)
texto = decodeAsm(texto)
if args.output:
    writeFile(args.output,texto)
else:
    writeFile("output.bin",texto)

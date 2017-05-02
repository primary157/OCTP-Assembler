#!/usr/bin/env python
#-*-coding: utf-8-*-
'''
Esse programa foi desenvolvido pela dubpla: Victor Guerra Veloso(2658) e Athena Sarantôpoulos(2652).
'''
def readFile(filename):
    text_file = []  #array de strings
    with open(filename,'r') as f:   #abre arquivo em modo leitura
        text_file = f.readlines() #le linhas separando-as em strings de um array
    return text_file    #retorna array
def writeFile(filename,text_file):
    with open(filename,'w') as f:   #abre arquivo em modo escrita
        f.writelines(text_file)           #escreve texto no arquivo
def convertToBin(value):
    if value[:1] == '-':
        if value[:3] == '-0x':
            return ('-'+str(bin(int(value[2:],16)))[3:])
        elif value[:3] == '-0b':
            return ('-'+value[3:])
        elif value[:3] == '-00':
            return ('-'+str(bin(int(value[2:],8)))[3:])
        else:
            return ('-'+str(bin(int(value)))[3:])
    if value[:2] == '0x':
        return str(bin(int(value[2:],16)))[2:]
    elif value[:2] == '0b':
        return value[2:]
    elif value[:2] == '00':
        return str(bin(int(value[2:],8)))[2:]
    else:
        return str(bin(int(value)))[2:]
'''
Deve ser capaz de ler as pseudointruçoes:

move(moving) reg,reg OK
multi(multiplicacao imediata) reg, reg, num
blt(branch on less than) reg, reg, TAG 
bgt(branch on greater than) reg, reg , TAG   
ble(branch on less than or equal) reg, reg, TAG
bge(branch on greater than or equal) reg, reg, TAG 
sge(set if greater or equal) reg, reg, TAG 
sgt(set greater than) reg, reg, TAG 
clear(limpa) reg 
neg(negative) reg,reg 
not(negaçao) reg, reg 
ror(rotacao direita) reg, reg, num 
rol(rotacao esquerda) reg, reg, num 

Deve ser capaz de ler as instruções:
    add reg,reg,reg
    add reg, reg, reg
    add reg, reg,reg
    add reg,reg, reg
    add reg,reg,reg
    sub reg,reg,reg
    addi reg,reg,num
    lw reg,num(reg)
    sw reg,num(reg)
    lw rd, const(rt)
    sw rt, const(rd)
    beq reg, reg, TAG
    bne reg, reg, TAG





Precisa ser compativel com instruções R:
meaning    op  rs  rt  rd  shamt   funct
bitsnum    6   5   5   5   5       6
Precisa ser compatível com instruções I:
meaning    op  rt  rd  const/address
bitsnum    6   5   5   16
Precisa ser compatível com instruções J:
meaning    op  const/address
bitsnum    6   26




'''

def decodeAsm(text_file):
    r_instructions = {
            "add": {
                    'funct' : '32',
                    'regs': ('rs','rt','rd')
                },
            "sub":{
                    'funct' : '34',
                    'regs': ('rs','rt','rd')
                },
            "and":{
                    'funct' : '36',
                    'regs': ('rs','rt','rd')
                },
            "or":{
                    'funct' : '37',
                    'regs': ('rs','rt','rd')
                },
            "nor":{
                    'funct' : '39',
                    'regs': ('rs','rt','rd')
                },
            "sll":{
                    'funct' : '0',
                    'regs': ('rt','rd','shamt')
                },
            "srl":{
                    'funct' : '2',
                    'regs': ('rt','rd','shamt')
                },
            "slt":{
                    'funct' : '42',
                    'regs': ('rs','rt','rd')
                },
            "jr":{
                    'funct' : '8',
                    'regs': ('rs')
                }
            }
    rotulo = {}
    pseudo_instructions = [
            "move",
            "inc",
            "multi",
            "blt",
            "bgt",
            "ble",
            "bge",
            "sge",
            "sgt",
            "clear",
            "neg",
            "not",
            "ror",
            "rol",
            "subi",
            ]
    i_instructions = {
                'addi' : '8',
                'andi': '12',
                'ori': '13',
                'lw': '35',
                'sw': '43',
                'beq': '4',
                'bne': '5'
            }
    j_instructions = {
            'j' : '2',
            'jal': '3'
            }
    registers = {
            '$zero' : '0',
            '$v0' : '2',
            '$v1' : '3',
            '$a0' : '4',
            '$a1' : '5',
            '$a2' : '6',
            '$a3' : '7',
            '$t0' : '8',
            '$t1' : '9',
            '$t2' : '10',
            '$t3' : '11',
            '$t4' : '12',
            '$t5' : '13',
            '$t6' : '14',
            '$t7' : '15',
            '$s0' : '16',
            '$s1' : '17',
            '$s2' : '18',
            '$s3' : '19',
            '$s4' : '20',
            '$s5' : '21',
            '$s6' : '22',
            '$s7' : '23',
            '$t8' : '24',
            '$t9' : '25',
            '$gp' : '28',
            '$sp' : '29',
            '$fp' : '30',
            '$ra' : '31'
            }
    output = ""
    n_linha = 0
    real_text_file = []
    for line in text_file:
        n_linha += 1
        pega_rotulo = line.split(':',1)
        try:
            line = pega_rotulo[1]
            rotulo[pega_rotulo[0]] = n_linha;
        except IndexError:
            real_text_file.append(line)
        else:
            real_text_file.append(pega_rotulo[1].lstrip(' '))
    '''
LOOP:add $s0,$s1,$s2
     bne $s0,$s1,LOOP
pega_rotulo = LOOP
rotulo["LOOP"] = 1



    '''
    n_linha = 0
    for line in real_text_file:
        n_linha += 1
        instruction = line.split(' ',1)
        instruction[1] = "".join(instruction[1].split(' '))
        repeticoes = 1
        if instruction[0] in pseudo_instructions:
            if instruction[0] == pseudo_instructions[0]:
                instruction[0] = 'add'
                regs = instruction[1].split(',')
                instruction[1] = regs[0] + ',$zero,' + regs[1]
                repeticoes = 1
                #converte move em add
            elif instruction[0] == pseudo_instructions[1]:
                instruction[0] = 'add'
                regs = instruction[1].split(',')
                instruction[1] = regs[0] + ',$zero,' + '1'
                repeticoes = 1
                #converte inc em add
            elif instruction[0] == pseudo_instructions[2]:
                instruction[0] = 'sll'
                regs = instruction[1].split(',')
                instruction[1] = regs[0] + "," + regs[1] + "," + str(int(regs[2])*2)
                repeticoes = 1
                #converte multi em sll
            elif instruction[0] == pseudo_instructions[3]:
                instruction[0] = 'slt'
                regs = instruction[1].split(',')
                instruction[1] = "$t7," + regs[0] + "," + regs[1]
                instruction.append('bne')
                instruction.append('$t7,$zero,' + regs[2])
                repeticoes = 2
                #converte blt em slt e bne
            elif instruction[0] == pseudo_instructions[4]:
                instruction[0] = 'slt'
                regs = instruction[1].split(',')
                instruction[1] = regs[0] + "," + regs[1] + "," + regs[2]
                instruction.append('bne')
                instruction.append(regs[0] + ',$zero,' + regs[2])
                repeticoes = 2
                #converte bgt em slt e bne
            elif instruction[0] == pseudo_instructions[5]:
                instruction[0] = 'slt'
                regs = instruction[1].split(',')
                instruction[1] = regs[0] + "," + regs[1] + "," + regs[2]
                instruction.append('beq')
                instruction.append(regs[0] + ',$zero,' + regs[2])
                repeticoes = 2
                #converte ble em slt e beq
            elif instruction[0] == pseudo_instructions[6]:
                instruction[0] = 'slt'
                regs = instruction[1].split(',')
                instruction[1] = regs[0] + "," + regs[1] + "," + regs[2]
                instruction.append('beq')
                instruction.append(regs[0] + ',$zero,' + regs[2])
                #converte bge em slt e beq
            elif instruction[0] == pseudo_instructions[7]:
                instruction[0] = 'slt'
                regs = instruction[1].split(',')
                instruction[1] = regs[0] + "," + regs[1] + "," + regs[2]
                instruction.append('beq')
                instruction.append(regs[0] + ',$zero,' + regs[2])
                repeticoes = 2
                #converte sge em slt e beq
            elif instruction[0] == pseudo_instructions[8]:
                instruction[0] = 'slt'
                regs = instruction[1].split(',')
                instruction[1] = regs[0] + "," + regs[1] + "," + regs[2]
                #converte sgt em slt
            elif instruction[0] == pseudo_instructions[9]:
                 instruction[0] = 'add'
                 regs = instruction[1].split(',')
                 instruction[1] = regs[0] + ',$zero,$zero'
                 repeticoes = 1
                 #clear
            elif instruction[0] == pseudo_instructions[10]:
                 instruction[0] = 'sub'
                 regs = instruction[1].split(',')
                 instruction[1] = regs[0] + ',$zero,' + regs[1]
                 repeticoes = 1
                 #converte neg em sub
            elif instruction[0] == pseudo_instructions[11]:
                 instruction[0] = 'add'
                 regs = instruction[1].split(',')
                 instruction[1] = regs[0] + ',' + regs[1] + ',$zero'
                 repeticoes = 1
                 #converte not em nor
            elif instruction[0] == pseudo_instructions[12]:
                 instruction[0] = 'sll'
                 regs = instruction[1].split(',')
                 instruction[1] = regs[0] + "," + regs[1] + "," + regs[2]
                 instruction.append('srl')
                 instruction.append(regs[0] + "," + regs[1] + "," + regs[2])
                 instruction.append('or')
                 instruction.append(regs[0] + "," + regs[1] + "," + regs[2])
                 repeticoes = 3
                 #converte ror em sll srl e or
            elif instruction[0] == pseudo_instructions[13]:
                instruction[0] = 'srl'
                regs = instruction[1].split(',')
                instruction[1] = regs[0] + "," + regs[1] + "," + regs[2]
                instruction.append('sll')
                instruction.append(regs[0] + "," + regs[1] + "," + regs[2])
                instruction.append('or')
                instruction.append(regs[0] + "," + regs[1] + "," + regs[2])
                repeticoes = 3
                #converte ror em srl sll e or
            elif instruction[0] == pseudo_instructions[14]:
                 instruction[0] = 'addi'
                 regs = instruction[1].split(',')
                 instruction[1] = regs[0] + ',$zero, -' + regs[1]
                 repeticoes = 1
        for i in range(0,repeticoes):
            instruction[0+(i*2)] = "".join(instruction[0+(i*2)].split(' ')) #tira os espaços
            instruction[1+(i*2)] = instruction[1+(i*2)].rstrip('\n')        #tira os \n's
            if instruction[0+(i*2)] in j_instructions:        #instruction[x] vai virar instruction[x+(i*2)]
                #instrucao do tipo j
                opcode = convertToBin(j_instructions[instruction[0+(i*2)]])
                address = convertToBin(str(rotulo[instruction[1+(i*2)]])) #endereço é o rotulo convertido em texto binario
                output += opcode.zfill(6) + address.zfill(26) #saida recebe strings com tamanhos fixos completados com 0
            elif instruction[0+(i*2)] in i_instructions:
                #instrucao do tipo i
                opcode = convertToBin(i_instructions[instruction[0+(i*2)]])
                regs = instruction[1+(i*2)].split(',')
                regs[-1] = regs[-1].rstrip('\n')
                output += opcode.zfill(6)
                if instruction[0+(i*2)] == 'lw':
                    output += convertToBin(registers[regs[1].split('(',1)[1].rstrip(')\n')]).zfill(5)  #rt Entrada
                    output += convertToBin(registers[regs[0]]).zfill(5)                                #rd Saida
                    output += convertToBin(regs[1].split('(',1)[0]).zfill(16)                          #const  offset
                elif instruction[0+(i*2)] == 'sw':
                    output += convertToBin(registers[regs[0]]).zfill(5)                                 #rt Entrada
                    output += convertToBin(registers[regs[1].split('(',1)[1].rstrip(')\n')]).zfill(5)   #rd Saida
                    output += convertToBin(regs[1].split('(',1)[0]).zfill(16)                           #const  offset
                else:
                    for j in regs:
                        if j in registers:
                            output += convertToBin(registers[j]).zfill(5)
                        else:
                            if instruction[0+(i*2)] == 'bne' or  instruction[0+(i*2)] == 'beq': #se j é rótulo
                                j = rotulo[j]-(n_linha+i)                                       #j vira um numero referente a distancia da linha atual
                            output += convertToBin(str(j)).zfill(16)
            elif instruction[0+(i*2)] in r_instructions:
                #instrucao do tipo r
                regs = instruction[1+(i*2)].split(',')
                regs[-1] = regs[-1].rstrip('\n')
                #opcode é sempre 0 nas instrucoes do tipo r
                output += "0".zfill(6)
                jafoi = {
                        'rs': False,
                        'rt': False,
                        'rd': False,
                        'shamt': False
                        }
                for j in range(4):
                    if not jafoi['rs']:
                        if 'rs' in r_instructions[instruction[0+(i*2)]]['regs']:
                            output += convertToBin(registers[regs[j]]).zfill(5)
                            jafoi['rs'] = True
                            continue
                        else:
                            output += "0".zfill(5)
                            jafoi['rs'] = True
                    if not jafoi['rt']:
                        if 'rt' in r_instructions[instruction[0+(i*2)]]['regs']:
                            output += convertToBin(registers[regs[j]]).zfill(5)
                            jafoi['rt'] = True
                            continue
                        else:
                            output += "0".zfill(5)
                            jafoi['rt'] = True
                    if not jafoi['rd']:
                        if 'rd' in r_instructions[instruction[0+(i*2)]]['regs']:
                            output += convertToBin(registers[regs[j]]).zfill(5)
                            jafoi['rd'] = True
                            continue
                        else:
                            output += "0".zfill(5)
                            jafoi['rd'] = True
                    if not jafoi['shamt']:
                        if 'shamt' in r_instructions[instruction[0+(i*2)]]['regs']:
                            output += convertToBin(regs[j]).zfill(5)
                            jafoi['shamt'] = True
                            continue
                        else:
                            output += "0".zfill(5)
                            jafoi['shamt'] = True
                output += convertToBin(r_instructions[instruction[0+(i*2)]]['funct']).zfill(6)
            else:
                print("Tem algo errado filho!")
                return  "Montagem Falhou!\n"
            output += '\n'  #fim de uma instrução
    return output

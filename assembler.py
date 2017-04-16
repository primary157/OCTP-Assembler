'''
Esse programa foi desenvolvido pela dubpla: Victor Guerra Veloso(2658) e Athena Sarantôpoulos().
'''
def readFile(filename):
    text_file = []  #array de strings
    with open(filename,'r') as f:   #abre arquivo em modo leitura
        text_file = f.readlines() #le linhas separando-as em strings de um array
    return text_file    #retorna array
def writeFile(filename,text_file):
    text = '\n'.join(text_file) #junta todas as strings como sendo um texto de varias linhas
    with open(filename,'w') as f:   #abre arquivo em modo escrita
        f.write(text)           #escreve texto no arquivo
def convertToBin(value):    
    if value[:2] == '0x':
        return str(bin(int(value[2:],16)))[2:]
    elif value[:2] == '0b':
        return value[2:]
    elif value[:2] == '00':
        return str(bin(int(value[2:],8)))[2:]
    else:
        return str(bin(int(value)))[2:]
'''
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
    for line in text_file:
        instruction = line.split(' ',1)
        if instruction[0] in j_instructions:
            #instrucao do tipo j
            opcode = convertToBin(j_instructions[instruction[0]])
            address = convertToBin(instruction[1].rstrip('\n')) #endereço é o valor seguinte ao opcode convertido em texto binario
            output += opcode.zfill(6) + " " + address.zfill(26) #saida recebe strings com tamanhos fixos completados com 0
        elif instruction[0] in i_instructions:
            #instrucao do tipo i
            opcode = convertToBin(i_instructions[instruction[0]])
            regs = instruction[1].split(',')
            regs[-1] = regs[-1].rstrip('\n')
            output += opcode.zfill(6) + " "
            if instruction[0] in ('andi','addi','ori'):
                for j in regs:
                    if j in registers:
                        output += convertToBin(registers[j]).zfill(5)
                    else:
                        output += convertToBin(str(j)).zfill(16)
                    output += " "
            elif instruction[0] == 'lw':
                output += convertToBin(registers[regs[1].split('(',1)[1].rstrip(')\n')]).zfill(5) + " "  #rt Entrada
                output += convertToBin(registers[regs[0]]).zfill(5) + " "                                 #rd Saida
                output += convertToBin(regs[1].split('(',1)[0]).zfill(16) + " "                            #const  offset
            elif instruction[0] == 'sw':
                output += convertToBin(registers[regs[0]]).zfill(5) + " "                                 #rt Entrada
                output += convertToBin(registers[regs[1].split('(',1)[1].rstrip(')\n')]).zfill(5) + " "   #rd Saida
                output += convertToBin(regs[1].split('(',1)[0]).zfill(16) + " "                            #const  offset
            else:
                #TODO: beq e bne eh diferente TRATAR ISSO
                pass
        elif instruction[0] in r_instructions:
            #instrucao do tipo r
            regs = instruction[1].split(',')
            regs[-1] = regs[-1].rstrip('\n')
            #opcode é sempre 0 nas instrucoes do tipo r
            output += "0".zfill(6) + " "
            jafoi = {
                    'rs': False,
                    'rt': False,
                    'rd': False,
                    'shamt': False
                    }
            for j in range(4):
                if not jafoi['rs']:
                    if 'rs' in r_instructions[instruction[0]]['regs']:
                        output += convertToBin(registers[regs[j]]).zfill(5)
                        jafoi['rs'] = True
                        output += " "
                        continue
                    else:
                        output += "0".zfill(5)
                        jafoi['rs'] = True
                if not jafoi['rt']:
                    if 'rt' in r_instructions[instruction[0]]['regs']:
                        output += convertToBin(registers[regs[j]]).zfill(5)
                        jafoi['rt'] = True
                        output += " "
                        continue
                    else:
                        output += "0".zfill(5)
                        jafoi['rt'] = True
                if not jafoi['rd']:
                    if 'rd' in r_instructions[instruction[0]]['regs']:
                        output += convertToBin(registers[regs[j]]).zfill(5)
                        jafoi['rd'] = True
                        output += " "
                        continue
                    else:
                        output += "0".zfill(5)
                        jafoi['rd'] = True
                if not jafoi['shamt']:
                    if 'shamt' in r_instructions[instruction[0]]['regs']:
                        output += convertToBin(registers[regs[j]]).zfill(5)
                        jafoi['shamt'] = True
                        output += " "
                        continue
                    else:
                        output += "0".zfill(5)
                        jafoi['shamt'] = True
                output += " "
            output += convertToBin(r_instructions[instruction[0]]['funct']).zfill(6) + " "
        else:
            print("Tem algo errado filho!")
            return  "Montagem Falhou!\n"
        output += '\n'  #fim de uma instrução
    return output

lista_directivas = ['ORG', 'START', 'END', 'DC.B', 'DC.W',
                    'BSZ',   'ZMB', 'FCB', 'FCC', 'FILL',]

lista_mnemonicos = ['ABA', 'ADCA', 'ADCB', 'ADDA', 'ADDB',
                    'ADDD', 'ANDA', 'ANDB','BNE' , 'BEQ' , 
                    'LBNE', 'LBEQ', 'DBEQ','IBNE', 'LDAA',
                    'JMP']

lista_relativos = ['BNE', 'BEQ', 'LBNE', 'LBEQ', 'DBEQ', 'IBNE']

mne = {'ABA' : ('INH', '2', '18 06 '),
       'ADCA IMM' : ('IMM', '2', '89 '),
       'ADCA DIR' : ('DIR', '2', '99 '),
       'ADCA EXT' : ('EXT', '3', 'B9 '), 
       'ADCB IMM' : ('IMM', '2', 'C9 '),
       'ADCB DIR' : ('DIR', '2', 'D9 '),
       'ADCB EXT' : ('EXT', '3', 'F9 '),
       'ADDA IMM' : ('IMM', '2', '8B '),
       'ADDA DIR' : ('DIR', '2', '9B '),
       'ADDA EXT' : ('EXT', '3', 'BB '),
       'ADDB IMM' : ('IMM', '2', 'CB '),
       'ADDB DIR' : ('DIR', '2', 'DB '),
       'ADDB EXT' : ('EXT', '3', 'FB '),
       'ADDD IMM' : ('IMM', '3', 'C3 '),
       'ADDD DIR' : ('DIR', '2', 'D3 '),
       'ADDD EXT' : ('EXT', '3', 'F3 '),
       'ANDA IMM' : ('IMM', '2', '84 '),
       'ANDA DIR' : ('DIR', '2', '94 '),
       'ANDA EXT' : ('EXT', '3', 'B4 '),
       'ANDB IMM' : ('IMM', '2', 'C4 '),
       'BNE REL'  : ('REL', '2', '26 '),
       'BEQ REL'  : ('REL', '2', '27 '),
       'LBNE REL' : ('REL', '4', '1826 '),
       'LBEQ REL' : ('REL', '4', '1827 '),
       'DBEQ REL' : ('REL', '3', '04 '),
       'IBNE REL' : ('REL', '3', '04 '),
       'LDAA IMM' : ('IMM', '2', '86 '),
       'LDAA DIR' : ('DIR', '2', '96 '),
       'LDAA EXT' : ('EXT', '3', 'B6 '),
       'LDAA IDX1': ('IDX', '2', 'A6 '),
       'LDAA IDX21':('IDX', '3', 'A6 '),
       'LDAA IDX22':('IDX', '4', 'A6 '),
       'LDAA IDX3' :('IDX', '4', 'A6 '),
       'LDAA IDX5' :('IDX', '2', 'A6 '),
       'LDAA IDX6' :('IDX', '2', 'A6 '),
       'JMP EXT'   :('EXT', '3', '06 ')}


def conversor(cadena,posicion):
    #Hexadecimal a decimal
    if(cadena[posicion] == '$'):
        cadena = cadena[posicion+1:]
        numero = int(cadena,16)

    #Octal a decimal
    elif(cadena[posicion] == '@'):
        cadena = cadena[posicion+1:]
        numero = int(cadena,8)

    #Binario a decimal
    elif(cadena[posicion] == '%'):
        cadena = cadena[posicion+1:]
        numero = int(cadena,2)

    #Decimal
    elif(cadena[posicion] != ('%','@','$')):
            numero = int(cadena)

    return numero

def dir_ext(num_dec): 
    if(num_dec < 256):
        return True
    else:
        return False 

def num_hex(contador, base):
    #return hex(contador + base).split('x')[-1];
    return hex(((contador+base) + (1 << 16)) % (1 << 16)).split('x')[-1]

def signo(contador, base):
    cadena = hex(contador + base).split('x')[0]
    if(cadena[0] == "-"):
        return False
    else:
        return True

#Funcion minuendo
def fun_minuendo(lista): 
    min = 0
    
    if(lista[0] not in ('$','%','@','0','1','2','3','4','5','6','7','8','9')):
        
        archivo = open('etiquetas.tabsim', 'r')
        for linea in archivo:
            if lista in linea:
                min = conversor(linea.split(' ')[-1],0)       
        archivo.close()
    else:
        min = conversor(lista,0)
        
    return min

def dbeq_count(signo,registro):
    if(signo == True and registro == "A"):
        return 'A0 '
    
    elif(signo == False and registro == "A"):
        return '10 '
    
    elif(signo == True and registro == "B"):
        return '01 '

    elif(signo == False and registro == "B"):
        return '11 '

def relativo(lista,cont,modo):
    
    count_r = ""
   
    if(lista[0] not in ('DBEQ','IBNE')):
        minuendo = fun_minuendo(lista[1])
        
    else:
        minuendo = fun_minuendo(lista[2])
        
    #Saca el valor de la posicion siguiente
    aux = '$'+ str(num_hex(cont[0]+cont[1]+int(mne[modo][1]),0))
    sustraendo = conversor(aux,0)

    if ((minuendo-sustraendo) < -127 or (minuendo-sustraendo) > 128):
        return 'FDR'  
    else:
        res = num_hex(minuendo-sustraendo,0)
        if(lista[0] in ('DBEQ','IBNE')):
            sig = signo(minuendo-sustraendo,0)
            count_r = dbeq_count(sig,lista[1][0])

        elif True:
            pass
            

        res = res.zfill(4)

        if(lista[0] in ('BNE','BEQ', 'DBEQ', 'IBNE')):
            res = res[2:]
            return count_r + res
        else:
            return res

def cod_registros(registro):
    if  (registro == "X"):
        return '00'

    elif(registro == "Y"):
        return '01'

    if  (registro == "SP"):
        return '10'

    elif(registro == "PC"):
        return '11'

def cod_letras(letra):
    if(letra == 'A'):
        return '00'
    if(letra == 'B'):
        return '01'
    if(letra == 'D'):
        return '10'

def idx_1(num,registro):
    codigo = ""
    codigo = cod_registros(registro) + "0" + bin(num).split("b")[-1].zfill(5)
    return num_hex(int(codigo,2),0)

def idx_2(num,registro, byts):
    codigo = ""
    codigo += "111" + cod_registros(registro) + "0"

    if(byts == 2):
        codigo += "0"
    else:
        codigo += "1"

    if(num < 0):
        codigo += "1"
    else:
        codigo += "0"

    resultado = ""
    resultado += num_hex(int(codigo,2),0) + " "
    
    codigo = num_hex(num,0).zfill(byts)

    resultado += codigo

    return resultado
    
def idx_3(num,registro):
    
    resultado = ""
    aux = ""
    aux += '111' + cod_registros(registro) + '011 '
    resultado += num_hex(int(aux,2),0) + " "

    resultado += num_hex(int(num),0).zfill(4)

    return resultado

def idx_5(letra,registro):
    resultado = '111' + cod_registros(registro) + '1' + cod_letras(letra)
    resultado = num_hex(int(resultado,2),0)
    return resultado

def idx_6():
    pass

    

    
   
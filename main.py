import os
import re
from mnemonicos import *

def mnemonicos(cont, lista, linea, archivo_lst, bandera):
    if(len(lista) == 1):
            #Modo de direccionamiento inherente
            modo = lista[0]
            if bandera:
                num = str(num_hex(cont[0], cont[1])).zfill(4)
                cadena = num +'\t'+ linea +' \t\t' + mne[lista[0]][0] +'(LI = ' + mne[lista[0]][1] + ') '+ mne[modo][2]
                archivo_lst.write(cadena + '\n')
    else:
        #Modo de direccionamiento indexado
        if(',' in lista[1] and lista[0] not in lista_relativos):

            #FORMULA 3 Y 6
            if(lista[1][0] == '['):
                
                #FORMULA 6
                if(lista[1][1] in ('A','B','D')):
                    
                    modo = lista[0] + " IDX6"
                    #IMPRIMIR FUERA DE RANGO EN FORMULA 6
                    if(lista[1][1] != 'D'):

                        if bandera:
                            num = str(num_hex(cont[0], cont[1])).zfill(4)
                            cadena = num +'\t'+ linea +' \t' + mne[modo][0] +'(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + 'FDR'
                            archivo_lst.write(cadena + '\n')

                    else:
                        if bandera:
                            registro = lista[1].split(",")[-1]
                            aux = '111' + cod_registros(registro[:-1]) + '111'
                            aux = num_hex(int(aux,2),0)

                            num = str(num_hex(cont[0], cont[1])).zfill(4) 
                            cadena = num +'\t'+ linea +' \t' + mne[modo][0] +'(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + aux
                            archivo_lst.write(cadena + '\n')

                #FORMULA 3
                else:
                    modo = lista[0] + " IDX3"
                    if(lista[1][1] == '-'):
                        if bandera:
                            num = str(num_hex(cont[0], cont[1])).zfill(4)
                            cadena = num +'\t'+ linea +' \t' +  mne[modo][0] +'(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + 'FDR'
                            archivo_lst.write(cadena + '\n')
                    else:
                        if bandera:
                            registro = lista[1].split(",")
                            
                            aux = idx_3(registro[0][1:],registro[1][:-1])
                            num = str(num_hex(cont[0], cont[1])).zfill(4)
                            
                            cadena = num +'\t'+ linea +' \t' + mne[modo][0] +'(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + aux
                            archivo_lst.write(cadena + '\n')
            else:
                #FORMULA 5
                if(lista[1][0] in ('A', 'B', 'D')):
                    modo = lista[0] + ' IDX5'
                    
                    if bandera:
                        registro = lista[1].split(",")
                        aux = idx_5(registro[0],registro[1])
                        num = str(num_hex(cont[0], cont[1])).zfill(4)
                        
                        cadena = num +'\t'+ linea +' \t' + mne[modo][0] +'(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + aux
                        archivo_lst.write(cadena + '\n')
                
                #FORMULA 1 Y 2
                else:
                    numIdx = int(lista[1].split(",")[0])
                    registro = lista[1].split(",")[-1]
                        
                    #FORMULA 1
                    if(numIdx >= -16 and numIdx <= 15):
                            
                        modo = lista[0] + " IDX1"
                        if bandera:
                            cod = idx_1(numIdx,registro)
                            num = str(num_hex(cont[0], cont[1])).zfill(4)
                            cadena = num +'\t'+ linea +' \t' + mne[modo][0] +'(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + cod
                            archivo_lst.write(cadena + '\n')

                    #FORMULA 2
                    else:  
                        if(numIdx >= -256 and numIdx <= 255):
                            modo = lista[0] + " IDX21"
                            byts = 2
                        else:
                            modo = lista[0] + " IDX22"
                            byts = 4

                        if bandera:
                            cod = idx_2(numIdx,registro,byts)
                            num = str(num_hex(cont[0], cont[1])).zfill(4)
                            cadena = num +'\t'+ linea +' \t' + mne[modo][0] +'(LI = ' + mne[modo][1] + ') ' + mne[modo][2] + cod
                            archivo_lst.write(cadena + '\n')
               
        elif(lista[0] in lista_relativos):
            modo = lista[0] + ' REL'

            if bandera:
                res = relativo(lista,cont,modo)
                num = str(num_hex(cont[0], cont[1])).zfill(4)
                cadena = num +'\t'+ linea +' \t' + mne[modo][0] +'(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + str(res)
                archivo_lst.write(cadena + '\n')
        
        elif(lista[1][0] != '#'):
    
            #?_?
            num_dec = fun_minuendo(lista[1])
            
            ######################################
            #Modo de direcionamiento Directo
            if(dir_ext(num_dec) and lista[0] != 'JMP'):
                cod = str(num_hex(num_dec,0)).zfill(2)
        
                modo = lista[0] + ' DIR'
                if bandera:
                    num = str(num_hex(cont[0], cont[1])).zfill(4)
                    cadena = num +'\t'+ linea +' \t' + mne[modo][0] +'(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + cod
                    archivo_lst.write(cadena + '\n')
                        
            #Modo de direcionamiento Extendido
            else:
                cod = str(num_hex(num_dec,0)).zfill(4)
                modo = lista[0] + ' EXT'
                if bandera:
                    num = str(num_hex(cont[0], cont[1])).zfill(4)
                    cadena = num +'\t'+ linea +' \t' + mne[modo][0] +'(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + cod  
                    archivo_lst.write(cadena + '\n')
        else:
            #Modo de direcionamiento Inmediato
            num_dec = conversor(lista[1][1:],0)
            if lista[0] == 'ADDD':
                cod = str(num_hex(num_dec, 0)).zfill(4)
            else:
                cod = str(num_hex(num_dec,0)).zfill(2)
            modo = lista[0] + ' IMM'
            if bandera:
                num = str(num_hex(cont[0], cont[1])).zfill(4)
                cadena = num + '\t'+ linea + ' \t' + mne[modo][0] + '(LI = ' + mne[modo][1] + ') '+ mne[modo][2] + cod 
                archivo_lst.write(cadena + '\n')   

    cont[0] += int(mne[modo][1])

def directivas(cont, lista, linea,archivo_lst, archivo, bandera):

    if(not bandera):   
        if ('EQU' in linea ):
            num = str(num_hex(conversor(lista[2],0),0)).zfill(4)
            archivo_lst.write(lista[0] + ' $' + num + '\n')
            
        elif(len(lista) > 1 and (lista[1] in lista_mnemonicos or lista[1] in lista_directivas)):

            num = str(num_hex(cont[0], cont[1])).zfill(4)
            archivo_lst.write(lista[0] + ' $' + num + '\n')

            if (lista[1] in lista_mnemonicos):
                lista.pop(0)
                mnemonicos(cont, lista, linea, archivo_lst, bandera)
          
    if  ('ORG' in linea ):
        cont[1] = int(lista[-1][1:], 16)
        cont[0] = 0
        if bandera:
            archivo_lst.write('    \t' + linea + '\n')
        
    elif('END' in linea):  
        if bandera:
            archivo_lst.write("    \t" + linea + '\n')
            for aux in archivo:
                archivo_lst.write("    \t" + aux)

    elif('START' in linea):
        cont[0] = 0
        cont[1]= 0
        
        if bandera:
            archivo_lst.write("    \t" + linea + '\n')
    
    elif('DC.B' in linea or 'DC.W' in linea or 'FCB' in linea):

        if ('DC.B' in linea or 'FCB' in linea):
            dc = 2
        else:
            dc = 4

        num = str(num_hex(cont[0],cont[1])).zfill(4)

        if(len(lista)== 1):
            if bandera:
                archivo_lst.write(num + '\t' +linea+'\t\t' + ''.zfill(dc) +  '\n')
            
            cont[0] += 1 * int((dc/2))
        else:
            aux = lista[1].split(',')

            if bandera:
                archivo_lst.write(num + '\t' +linea+'\t')

                if(lista[1][0] in ('0','1','2','3','4','5','6','7','8','9')):
                    for i in aux:
                        archivo_lst.write(str(num_hex(int(i),0)).zfill(dc) + ' ')
                
                else:
                    for i in aux:
                        archivo_lst.write(str(num_hex(ord(i[-1]),0)).zfill(dc) + ' ')
                
                archivo_lst.write('\n')
            #######################################################################

            cont[0] += len(aux) * int((dc/2))
                    
    elif('BSZ' in linea or 'ZMB' in linea):
        aux = int(lista[1])
        num = str(num_hex(cont[0],cont[1])).zfill(4)
        cont[0]  += aux

        if bandera:
            archivo_lst.write(num + '\t' +linea+'\t\t')
            for i in range(aux):
                archivo_lst.write('00 ')
            
            archivo_lst.write('\n')
        ##########################################

    elif('FCC' in linea):
        aux = re.sub('/','',lista[1]) 
        num = str(num_hex(cont[0],cont[1])).zfill(4)
        cont[0]  += len(aux)

        if bandera:
            archivo_lst.write(num + '\t' +linea+'\t\t')
            for i in aux:
                archivo_lst.write(str(num_hex(ord(i),0)).zfill(2) + ' ')

            archivo_lst.write('\n')

    elif('FILL'in linea):
        aux = lista[1].split(',')
        num = str(num_hex(cont[0],cont[1])).zfill(4)
        cont[0] += int(aux[1])

        if bandera:
            archivo_lst.write(num + '\t' +linea+'\t')
            for i in range(int(aux[1])):
                archivo_lst.write(aux[0].zfill(2) + ' ')
            
            archivo_lst.write('\n')
        #############################################
        
    else:
        if bandera:
            if (len(lista) > 1 and lista[1] in lista_mnemonicos):
                lista.pop(0)
                mnemonicos(cont, lista, linea, archivo_lst, bandera)
            else:
                archivo_lst.write("    \t" + linea + '\n')
            #num = str(num_hex(cont[0],cont[1])).zfill(4)
            #archivo_lst.write(num+"\t" + linea + '\n')
            
def main(bandera):
    nombre = 'prueba12.asm'

    if os.path.exists(nombre):

        #contador del programa conformado por la base y el acumulador
        cont = [0,0] 
        archivo = open(nombre, 'r')
        if bandera:
            archivo_lst = open ('prueba.lst', 'w')
        else:
            archivo_lst = open('etiquetas.tabsim', 'w')

        for linea in archivo:
            linea = linea.replace(linea[len(linea)-1], "")
            lista = linea.split(" ")

            if (lista[0] in lista_mnemonicos):
                mnemonicos(cont, lista,linea,archivo_lst, bandera)
            else:
                directivas(cont, lista,linea,archivo_lst, archivo, bandera)

        archivo.close()
        archivo_lst.close()

#Ciclo para sacar las etiquetas
main(False)

#Ciclo para escribir en el archivo prueba.lst
main(True)
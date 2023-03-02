# -*- coding: utf-8 -*-
from Backend.Data_e_hora import difDayWeek,getDia


meses = {"janeiro":'01',
         "fevereiro":'02',
         'março':'03',
         'abril':'04',
         "maio":'05',
         'junho':'06',
         "julho":'07',
         "agosto":'08',
         "setembro":'09',
         "outubro":'10',
         "novembro":'11',
         "dezembro":'12'}

def tratamentoCompromisso(dia,horario):
    try:
        dia = tratamentoDia(dia)

    except Exception:
        return False,True

    try:
        hora = tratamentoHora(horario)

    except Exception:
        return True,False

    if '/' not in dia and isInt(dia) and len(dia) == 4:
        diaOUT = dia[:2]
        mes = dia[2:]
        dia = diaOUT + '/' + mes

    return dia,hora


def tratamentoDia(dia):
    try:
        dia = difDayWeek(dia) + int(getDia())
        if dia < 10:
            dia = '0' + str(dia)
        else:
            dia = str(dia)

    except Exception:
        teste = proximidade(dia)
        if teste == False:
            dia = dia.replace("de ","/")
            dia = dia.replace("do ","/")
            dia = dia.replace("dia","")
            dia = dia.replace("para o","")
            dia = dia.replace(" ","")
        else:
            dia = teste

    return validarDia(dia)

def correspondencia(string1,string2):
    string1 = string1.lower()
    string2 = string2.lower()
    return string1 == string2

def validarDia(dia):
    i = 0
    diaOut = ''
    if '/' in dia:
        while True:
            if dia[i] == '/':
                mesAno = obterMes(dia[i+1:])
                break
            diaOut += dia[i]
            i += 1

        if mesAno == False:
            return diaOut

        if int(diaOut) < 10:
            diaOut = '0' + diaOut

        return diaOut + mesAno

    else:
        if isInt(dia):
            return dia

        else:
            return False


def isInt(valor):
    try:
        str(int(valor))
        return True

    except Exception:
        return False

def proximidade(dia):
    if correspondencia(dia,"depois de amanhã"):
        diaOut = int(getDia()) + 2
        if diaOut < 10:
            diaOut = '0' + str(diaOut)

        return str(diaOut)

    elif correspondencia(dia,"amanhã"):
        diaOut = int(getDia()) + 1
        if diaOut < 10:
            diaOut = '0' + str(diaOut)

        return str(diaOut)

    elif correspondencia(dia,"hoje"):
        return getDia()

    else:
        return False

def obterMes(stringDia):
    stringMes = ''
    i = 0
    while True:
        if stringDia[i] == '/' or i == len(stringDia) - 1:
            if i == len(stringDia) - 1:
                stringMes += stringDia[i]
            break

        stringMes += stringDia[i]
        i+=1


    for c in meses:
        if correspondencia(stringMes,c) or stringMes == meses[c]:
            return stringDia.replace(stringMes,f'/{meses[c]}')

    return False


def tratamentoHora(hora):
    horaOut = ''
    flagTurno = False
    if ('tarde' in hora or 'noite' in hora):
        flagTurno = True
    if ' 'in hora:
        for c in hora:
            if (c == ':' or c == '0' or c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6'or c == '7'
            or c == '8' or c == '9'):
                horaOut += c

    else:
        horaOut = hora

    return verificacaoHora(horaOut,flagTurno)


def verificacaoHora(horario,flagTurno):
    if len(horario) == 4:
        return validaHora('0' + horario,flagTurno)
    elif len(horario)==2:
        return validaHora(horario + ":00",flagTurno)
    elif len(horario) == 1:
        return validaHora('0' + horario + ":00",flagTurno)
    else:
        return horario

def validaHora(horaFinal,flagTurno):
    if flagTurno:
        hora = int(horaFinal[:2])
        if hora<=12:
            hora = hora + 12
            horaFinal = horaFinal.replace(horaFinal[:2], "")
        else:
            horaFinal = horaFinal.replace(horaFinal[:2], "")
        return str(hora) + horaFinal

    else:
        return horaFinal
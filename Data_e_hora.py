# -*- coding: utf-8 -*-
from datetime import datetime

dic = {"segunda":0,
       "terça":1,
       "quarta":2,
       "quinta":3,
       "sexta":4,
       "sábado":5,
       "domingo":6}

def difDayWeek(diaDaSemana):
    diaDaSemana = diaDaSemana.replace(" ","")
    data = datetime.now()
    diaHJ = data.weekday()
    if "-feira" in diaDaSemana:
        if dic[diaDaSemana.replace("-feira", "").lower()] < diaHJ:
            return dic[diaDaSemana.replace("-feira", "").lower()] + 7 - diaHJ
        return dic[diaDaSemana.replace("-feira","").lower()] - diaHJ
    elif "feira" in diaDaSemana:
        if dic[diaDaSemana.replace("feira", "").lower()] < diaHJ:
            return dic[diaDaSemana.replace("feira", "").lower()] + 7 - diaHJ
        return dic[diaDaSemana.replace("feira", "").lower()] - diaHJ

    elif dic[diaDaSemana.lower()] < diaHJ:
        return dic[diaDaSemana.lower()] - diaHJ + 7

    return dic[diaDaSemana.lower()] - diaHJ

def getHora():
    data = datetime.now()
    return data.strftime('%H:%M')

def getData():
    data = datetime.now()
    return data.strftime('%d/%m/%Y')

def getMes():
    data = datetime.now()
    mes = str(data.month)
    if len(mes) == 1:
        return '0'+mes
    return mes

def getAno():
    data = datetime.now()
    return data.year

def getDia():
    data = datetime.now()
    dia = str(data.day)
    if len(dia) == 1:
        return '0' + dia
    return dia
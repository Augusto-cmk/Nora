from Backend.dicionario import criarDicionario
from Backend.Data_e_hora import getData,getHora,getDia,getAno,getMes

class agenda:

    def __init__(self):
        file = open("Backend/compromissos.ini", "r")
        self.leitura = file.readlines()
        self.dic = self.read()
        file.close()


    def write(self):
        file = open("Backend/compromissos.ini", "w")
        for value in self.dic:
            file.write(f"[{value}]\n")
            for compromisso in self.dic[value]:
                file.write(f"{compromisso}\n")

    def alterarCompromisso(self,data,novoDado,horario):
        self.dic[data] = novoDado + ' ' + horario

    def adicionarCompromisso(self,compromisso,hora,data=None):
        if data:
            if len(data) == 2:
                data = data + f'/{getMes()}/{getAno()}'

            elif len(data) <= 5:
                data = data + f'/{getAno()}'

            try:
                if self.verifyHour(data,hora):
                    self.dic[data].append(compromisso + " " + hora)
                    return True
                return False

            except Exception:
                if self.compareHour(hora,data):
                    self.dic[data] = list()
                    self.dic[data].append(compromisso + " "+ hora)
                    return True
                else:
                    return False
        else:
            try:
                if self.verifyHour(getData(),hora):
                    self.dic[getData()].append(compromisso + " " + hora)
                    return True
                return False

            except Exception:
                if self.compareHour(hora,getData()):
                    self.dic[getData()] = list()
                    self.dic[getData()].append(compromisso + " " + hora)
                    return True
                else:
                    return False

    def verifyHour(self,data,horario):
        if data == getData():
            compromissos = self.dic[data]
            for compromisso in compromissos:
                if horario in compromisso:
                    return False

            return self.compareHour(horario,data)
        else:
            compromissos = self.dic[data]
            for compromisso in compromissos:
                if horario in compromisso:
                    return False

            return True

    def compareHour(self,horario,data):
        dia = int(data[:2])
        mes = int(data[3:5])

        if dia == int(getDia()):
            if mes == int(getMes()):
                horas1 = horario[:2]
                minutos1 = horario[3:]

                horaAtual = getHora()
                horas = horaAtual[:2]
                minutos = horaAtual[3:]

                if horas1 == horas and int(minutos1) > int(minutos):
                    return True

                elif int(horas1) > int(horas):
                    return True

                else:
                    return False

            elif mes < int(getMes()):
                return False

            else:
                return True

        elif dia < int(getDia()):
            if mes > int(getMes()):
                return True

            return False

        else:
            return True


    def read(self):
        i = 0
        indices = list()
        respostas = list()
        compromissos = list()
        comeco = True
        for line in self.leitura:
            if '[' in line:
                if comeco == False:
                    respostas.append(compromissos)
                    compromissos = list()
                indice = line.replace("[", "")
                indice = indice.replace("]", "")
                indice = indice.replace("\n", "")
                indices.append(indice)
                comeco = False
            else:
                compromissos.append(line.replace("\n", ""))

            i += 1
        respostas.append(compromissos)
        try:
            return criarDicionario(indices,respostas)

        except Exception:
            return {}

    def delete(self,hour,data):
        compromissos = self.consulta(data)
        i = 0
        for comp in compromissos:
            if comp[1] == hour:
                del(self.dic[data][i])

            i += 1

        if len(self.dic[data]) == 0:
            del(self.dic[data])

    def consulta(self,data):
        if len(data)<=2:
            try:
                compromissos = self.dic[f'{data}/{getMes()}/{getAno()}']
                compromissosOUT = list()
                horario = None
                for compromisso in compromissos:
                    descricao = ''
                    compromisso = compromisso.split(' ')
                    i = 0
                    for palavra in compromisso:
                        if i < len(compromisso)-1:
                            descricao += palavra + " "
                        else:
                            horario = palavra
                        i += 1

                    compromissosOUT.append((descricao,horario))

                return compromissosOUT

            except Exception:
                return False

        elif len(data)<=5:
            try:
                compromissos = self.dic[f'{data}/{getAno()}']
                compromissosOUT = list()
                horario = None
                for compromisso in compromissos:
                    i = 0
                    descricao = ''
                    compromisso = compromisso.split(' ')
                    for palavra in compromisso:
                        if i < len(compromisso) - 1:
                            descricao += palavra + " "
                        else:
                            horario = palavra
                        i += 1

                    compromissosOUT.append((descricao, horario))

                return compromissosOUT

            except Exception:
                return False

        else:
            try:
                compromissos = self.dic[data]
                compromissosOUT = list()
                horario = None
                for compromisso in compromissos:
                    descricao = ''
                    compromisso = compromisso.split(' ')
                    i = 0
                    for palavra in compromisso:
                        if i < len(compromisso) - 1:
                            descricao += palavra + " "
                        else:
                            horario = palavra
                        i += 1

                    compromissosOUT.append((descricao, horario))

                return compromissosOUT

            except Exception:
                return False

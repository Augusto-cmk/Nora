from dicionario import criarDicionario
from Data_e_hora import getData,getHora,getDia,getAno,getMes
import sqlite3

class agenda: ## Passar para banco de dados

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

def transform(listWithTuple:tuple)->list:
    return [tupla[0] for tupla in listWithTuple]

class Banco_de_Dados:
    def __init__(self,nome:str):
        self.nome = nome
        self.conn = sqlite3.connect(f"{nome}.db")
        self.cmd = self.conn.cursor()
        self.__criar()


    def __criar(self):
        self.cmd.execute(
            """
            CREATE TABLE IF NOT EXISTS compromisso (
                    descricao varchar(100) not null,
                    data datetime,
                    hora varchar(6) not null
                );
            """
        )
        self.conn.commit()
        

    def inserirCompromisso(self,descricao:str,data:str,hora:str): ## Criar uma regra de negócio para inserir o compromisso
        try:
            self.cmd.execute(
                f"""
                    INSERT INTO compromisso(descricao,data,hora)
                    values(?,?,?);
                """,(descricao,data,hora,)
            )
            self.conn.commit()
            return True
        except Exception:
            return False

    
    def removerCompromisso(self,data:str,hora:str):
        try:
            self.cmd.execute(
                """
                    delete from compromisso where data = ? and hora = ?;
                """,(data,hora,)
            )
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def obterCompromissos(self,data:str):
        return self.cmd.execute(
            """
                SELECT descricao,hora from compromisso where data = ?;
            """,(data,)
        ).fetchall()


teste = Banco_de_Dados("Teste")
teste.inserirCompromisso("Comer carne","18/12/2000","10:15")
teste.inserirCompromisso("Comer doce","18/12/2000","10:16")
teste.inserirCompromisso("Andar","18/12/2000","10:17")
teste.inserirCompromisso("Nascer","18/12/2000","10:18")
teste.inserirCompromisso("Sentar","18/12/2000","10:19")
print(teste.obterCompromissos("18/12/2000"))
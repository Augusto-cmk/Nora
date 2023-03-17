from Backend.Data_e_hora import getData,getHora,getDia,getAno,getMes
import sqlite3

class agenda:

    def __init__(self):
        self.db = Banco_de_Dados("Compromissos")

    def alterarCompromisso(self,data,novoDado,horario):
        self.db.alterarCompromisso(data,horario,novoDado)
    
    def alterarData(self,data,novaData,horario):
        self.db.alterarData(data,horario,novaData)

    def alterarHora(self,data,novaHora,horario):
        self.db.alterarHora(data,horario,novaHora)

    def adicionarCompromisso(self,compromisso,hora,data=None):
        if data:
            if len(data) == 2:
                data = data + f'/{getMes()}/{getAno()}'

            elif len(data) <= 5:
                data = data + f'/{getAno()}'

            try:
                if self.__verifyHour(data,hora):
                    self.db.inserirCompromisso(compromisso,data,hora)
                    return True
                return False

            except Exception:
                if self.compareHour(hora,data):
                    self.db.inserirCompromisso(compromisso,data,hora)
                    return True
                else:
                    return False
        else:
            try:
                if self.__verifyHour(getData(),hora):
                    self.db.inserirCompromisso(compromisso,getData(),hora)
                    return True
                return False

            except Exception:
                if self.compareHour(hora,getData()):
                    self.db.inserirCompromisso(compromisso,getData(),hora)
                    return True
                else:
                    return False

    def __verifyHour(self,data,horario):
        if data == getData():
            compromissos = self.db.obterCompromissos(data)
            for compromisso in compromissos:
                if horario in compromisso:
                    return False

            return self.compareHour(horario,data)
        else:
            compromissos = self.db.obterCompromissos(data)
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
                return self.db.obterCompromissos(f'{data}/{getMes()}/{getAno()}')

            except Exception:
                return False

        elif len(data)<=5:
            try:
                return self.db.obterCompromissos(f'{data}/{getAno()}')

            except Exception:
                return False

        else:
            try:
                return self.db.obterCompromissos(data)

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
    
    def alterarCompromisso(self,data:str,hora:str,novaDescricao:str):
        self.cmd.execute(
            """
                UPDATE compromisso set descricao = ? where data = ? and hora = ?
            """,(novaDescricao,data,hora,)
        )
        self.conn.commit()
    
    def alterarHora(self,data:str,hora:str,newHora:str):
        self.cmd.execute(
            """
                UPDATE compromisso set hora = ? where hora = ? and data = ?
            """,(newHora,hora,data,)
        )
        self.conn.commit()
    
    def alterarData(self,data:str,hora:str,newData:str):
        self.cmd.execute(
            """
                UPDATE compromisso set data = ? where hora = ? and data = ?
            """,(newData,hora,data,)
        )
        self.conn.commit()
import sys
from Backend.conexao import test_conexao
from Backend.FalarOuvir import Comunication
from Backend.Data_e_hora import getData,getHora,getMes,getAno,getDia
from Backend.Calculadora import calculadora
from Backend.readCompromissos import agenda
from Backend.tratamento import tratamentoCompromisso,tratamentoHora
import wikipedia
import os
if test_conexao():
    import pywhatkit

# from spacy.cli import download
#
# download('en_core_web_sm')


class ENGSM:
    ISO_639_1 = 'en_core_web_sm'


class Nora:
    def __init__(self):
        self.comunicacao = Comunication()
        self.calcular = calculadora()
        self.perguntasPesquisa = ['o que é','qual é','quem é','o que significa','como fazer','quem foi']
        self.agenda = agenda()
        self.comunicacao.Falar("Olá, sistemas iniciados!")
        self.listaCompromissos = self.getCompromissoDoDia()
        print("Nora it's runing...")


    def getPositionPesquisa(self,valor):
        for i in range(len(self.perguntasPesquisa)):
            if valor == self.perguntasPesquisa[i]:
                return i
        return False


    def activate(self):
        if self.listaCompromissos != False:
            tam = len(self.listaCompromissos)
            i = 0
            while True:
                if i == tam:
                    break
                elif self.agenda.compareHour(self.listaCompromissos[i][1],getData()) == False:
                    self.comunicacao.Falar(f"Você perdeu o compromisso {self.listaCompromissos[i][0]} para as {self.listaCompromissos[i][1]}")
                    self.agenda.delete(self.listaCompromissos[i][1],getData())
                    del(self.listaCompromissos[i])
                    i -= 1
                    tam -= 1

                i += 1
        texto = self.comunicacao.listening(self.listaCompromissos)
        try:
            self.comandos(texto)
            self.activate()

        except Exception:
            self.activate()

    def comandos(self,texto):
        if texto[:29].lower() == 'finalizar compromissos do dia':
            self.listaCompromissos = list()
            try:
                del(self.agenda.dic[getData()])
                self.comunicacao.Falar("Compromissos do dia exlcuídos com sucesso!")
                self.agenda.write()
            except Exception:
                self.comunicacao.Falar("Você não possui compromissos para excluir!")

        elif texto[:21].lower() == 'finalizar compromisso':
            horario = self.comunicacao.addCompromisso("Qual o horário do compromisso ?")
            horario = tratamentoHora(horario)
            aux = None
            i = 0
            for compromisso in self.listaCompromissos:
                if compromisso[1] == horario:
                    self.listaCompromissos.remove(compromisso)
                    aux = compromisso[0]
                i += 1

            if aux != None:
                self.agenda.delete(horario, getData())
                self.comunicacao.Falar(f"Compromisso {aux} foi removido de sua agenda")
                self.agenda.write()
            else:
                self.comunicacao.Falar("Acho que não comrpreendi o horário dito ou o compromisso não existe mais")


        elif texto[:13].lower() == 'que horas são':
            self.comunicacao.Falar(getHora())

        elif texto[:14].lower() == 'que dia é hoje':
            self.comunicacao.Falar(f"Hoje é {getData()}")

        elif texto[:19].lower() == 'desligar computador':
            self.comunicacao.Falar("Estou encerrando o seu computador")
            os.system("shutdown /s /t 1")

        elif texto[:20].lower() == 'reiniciar computador':
            self.comunicacao.Falar("Estou reiniciando o seu computador")
            os.system("shutdown /r /t 1")

        elif texto[:26].lower() == 'adicionar compromisso':
            data = self.comunicacao.addCompromisso("Para qual dia deseja adicionar este compromisso ?")
            info = self.comunicacao.addCompromisso("Qual é o compromisso?")
            hora = self.comunicacao.addCompromisso("Qual o horário do compromisso ?")

            dia,hora = tratamentoCompromisso(data,hora)

            if dia == False:
                self.comunicacao.Falar("Os dados do dia estão incorretos, ou não consegui compreendê-los")
            elif hora == False:
                self.comunicacao.Falar("As horas passadas estão incorretas, ou não consegui compreendê-las")
            else:
                if self.agenda.adicionarCompromisso(info,hora,dia):
                    self.listaCompromissos = self.agenda.consulta(getDia())
                    self.comunicacao.Falar("Compromisso inserido com sucesso")
                    self.agenda.write()
                else:
                    self.comunicacao.Falar("Houve um erro ao inserir o compromisso! Tenha certeza que a data "
                                           "e o horário desejado esteja correto e o compromisso "
                                           "não esteja sendo marcado para antes de hoje, ou que o compromisso ja exista em sua agenda")


        elif texto[:25].lower() == 'o que você pode fazer':
            self.comunicacao.Falar("Eu consigo te dizer as horas, o dia de hoje e também posso desligar ou reiniciar seu computador se me for solicitado")
            self.comunicacao.Falar("Consigo tocar uma música por meio do comando tocar + o nome da música")
            self.comunicacao.Falar("Também consigo pesquisar conseitos por meio de algumas perguntas")
            self.comunicacao.Falar("Posso te dizer os compromissos do dia e adicionar novos")
            self.comunicacao.Falar("Além da capacidade de fazer contas como já deve saber")
            self.comunicacao.Falar("Caso queira consultar, foi exibido no meu terminal os comandos que consigo executar!")
            print("\t\t\t\t\t\t[Comandos nora]\n\n")
            print("- finalizar compromissos do dia\t\t [finaliza todos os compromissos do dia]\n\n")
            print("- finalizar compromisso\t\t [permite escolher um compromisso do dia para finalizar]\n\n")
            print("- que horas são\n\n")
            print("- que dia é hoje\n\n")
            print("- desligar computador\n\n")
            print("- reiniciar computador\n\n")
            print("- adicionar compromisso\t\t [permite adicionar novos compromissos]\n\n")
            print("- o que você pode fazer\t\t [te diz o que ela pode fazer]\n\n")
            print("- quanto é\t\t [dizer uma conta matemática posterior a frase do comando]\n\n")
            print("- finalizar assistência\t\t [encerra os serviços]\n\n")
            print("- tocar\t\t [dizer o nome de uma música após o comando tocar para que ela toque a música]\n\n")
            print("- ler compromissos do dia\t\t [executa uma leitura dos compromissos do dia]\n\n")
            print("- quais os meus compromissos para amanhã\t\t [executa uma leitura para os compromissos do dia seguinte]\n\n")
            print("- pesquisar conceitos por meio de palavras chave\t\t {'o que é','qual é','quem é','o que significa','como fazer','quem foi'}")

        elif texto[:8].lower() == 'quanto é':
            pergunta = texto[8:]
            if pergunta == ' ' or pergunta == '':
                self.comunicacao.Falar("Você não me informou nenhum número")
            else:
                self.comunicacao.Falar(f"O resultado é {self.calcular.tratarPergunta(texto[8:])}")

        elif texto[:21].lower() == 'finalizar assistência':
            self.agenda.write()
            self.comunicacao.Falar("Então vou dormir agora... Me acorde depois quando precisar de mim!")
            sys.exit(0)

        elif self.verificaPergunta(texto.lower()):
            wikipedia.set_lang('pt')
            try:
                self.comunicacao.Falar("vish... eu também não sei, mas vou pesquisar")
                resultado = wikipedia.summary(texto,2)
                self.comunicacao.Falar("Segundo a wikipedia")
                self.comunicacao.Falar(resultado)
            except Exception:
                self.comunicacao.Falar("Acho que não entendi o que você quis dizer")

        elif texto[:5].lower() == 'tocar':
            if texto[5:] == ' ' or texto[5:] == '':
                self.comunicacao.Falar("Você não me disse o nome da música, estilo ou autor")

            else:
                self.comunicacao.Falar("Pode deixar")
                pywhatkit.playonyt(texto[5:])

        elif texto[:23].lower() == 'ler compromissos do dia':
            self.lerCompromissosDoDia()

        elif texto[:40].lower() == 'quais os meus compromissos para amanhã':
            dia = int(getDia()) + 1
            if dia < 10:
                dia = '0' + str(dia)

            self.lerCompromissos(str(dia))
            
        else:
            self.comunicacao.Falar("Comando não existente")
            self.comunicacao.Falar("Caso queira consultar os comandos diga : o que você pode fazer")


    def getCompromissoDoDia(self):
        return self.agenda.consulta(getDia())


    def lerCompromissos(self,dia):
        lista = self.agenda.consulta(dia)
        if lista == False:
            self.comunicacao.Falar("Você não possui compromissos em sua agenda marcados para esse dia")

        else:
            self.comunicacao.Falar("Você possui os seguintes compromissos:")
            for compromisso in lista:
                self.comunicacao.Falar(f'{compromisso[0]} às {compromisso[1]}')

    def lerCompromissosDoDia(self):
        if self.listaCompromissos == False:
            self.comunicacao.Falar("Você não possui compromissos em sua agenda marcados para hoje")

        else:
            self.comunicacao.Falar("Você possui os seguintes compromissos:")
            for compromisso in self.listaCompromissos:
                self.comunicacao.Falar(f'{compromisso[0]} às {compromisso[1]}')

    def verificaPergunta(self,texto):
        for pergunta in self.perguntasPesquisa:
            if pergunta in texto and 'você' not in texto and 'criador' not in texto:
                return True
        return False



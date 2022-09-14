import sys

import pyttsx3
import speech_recognition as sr
from Backend.conexao import test_conexao
from Backend.Data_e_hora import getHora

class Comunication:
    def __init__(self):
        self.motor = pyttsx3.init()
        self.reconhecer = sr.Recognizer()

    def Falar(self,texto):
        self.motor.say(texto)
        self.motor.runAndWait()

    def addCompromisso(self,pergunta):
        with sr.Microphone() as microfone:
            self.reconhecer.adjust_for_ambient_noise(microfone)
            self.Falar(pergunta)
            audio = self.reconhecer.listen(microfone)
        try:
            texto = self.reconhecer.recognize_google(audio, language='pt-BR')
            return texto

        except sr.UnknownValueError:
            self.Falar('Não consegui entender o que você disse')
            return self.addCompromisso(pergunta)

    def addResposta(self,pergunta):
        with sr.Microphone() as microfone:
            self.reconhecer.adjust_for_ambient_noise(microfone)
            self.Falar(f'O que devo dizer quando você disser {pergunta} ?')
            audio = self.reconhecer.listen(microfone)
        try:
            texto = self.reconhecer.recognize_google(audio, language='pt-BR')
            return texto

        except sr.UnknownValueError:
            self.Falar('Não consegui entender o que você disse')
            return self.addResposta(pergunta)

    def getComando(self,compromissosdodia):
        with sr.Microphone() as microfone:
            self.reconhecer.adjust_for_ambient_noise(microfone)
            self.Falar('Diga')
            audio = self.reconhecer.listen(microfone)
        try:
            texto = self.reconhecer.recognize_google(audio, language='pt-BR')
            return texto

        except sr.UnknownValueError:
            self.Falar('Não consegui entender o que você disse')
            return self.listening(compromissosdodia)

    def listening(self,compromissosdodia):
        if test_conexao():
            with sr.Microphone() as microfone:
                self.reconhecer.adjust_for_ambient_noise(microfone, duration=1)
                return self.listen(microfone,compromissosdodia)

        else:
            self.Falar("Você não possui conexão com a internet, logo não consigo te ajudar")
            self.Falar("Estarei aqui ansiosa para poder te ajudar assim que possível!Até breve!")
            sys.exit(0)

    def falta10Min(self,horaCompromisso):
        hora1Aux = horaCompromisso[:2]
        minutos1Aux = horaCompromisso[3:]

        hora2 = getHora()

        hora2Aux = hora2[:2]
        minutos2Aux = hora2[3:]

        if hora1Aux == hora2Aux:
            if (int(minutos1Aux) - 10) == int(minutos2Aux):
                return True
            return False
        return False

    def listen(self,microfone,compromissosdodia): # arrumar identificador de voz
        while True:
            if compromissosdodia != False:
                for compromisso in compromissosdodia:
                    if self.falta10Min(compromisso[1]):
                        self.Falar(f"Falta 10 minutos para o compromisso {compromisso[0]}")


            audio = self.reconhecer.listen(microfone)
            try:
                texto = self.reconhecer.recognize_google(audio, language='pt-BR')
                if 'nora' in texto.lower() or 'nor' in texto.lower():
                    return self.getComando(compromissosdodia)

            except Exception:
                pass

    def conversa(self):
        if test_conexao():
            with sr.Microphone() as microfone:
                self.reconhecer.adjust_for_ambient_noise(microfone, duration=1)
                audio = self.reconhecer.listen(microfone)
                self.reconhecer.listen(microfone)
            try:
                texto = self.reconhecer.recognize_google(audio, language='pt-BR')
                return texto

            except sr.UnknownValueError:
                self.Falar("Não entendi o que você disse, tente falar novamente")
                return self.conversa()
        else:
            self.Falar("Você não possui conexão com a internet, logo não consigo te ajudar")
            self.Falar("Estarei aqui ansiosa para poder te ajudar assim que possível!Até breve!")
            sys.exit(0)

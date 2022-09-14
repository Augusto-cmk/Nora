class calculadora:

    def tratarPergunta(self,pergunta):
        pergunta = pergunta.lower()
        pergunta = pergunta.replace("%"," %")
        pergunta = pergunta.replace("de ","")
        valores = pergunta.split(" ")
        if valores[0] == '':
            del(valores[0])
        return self.resultConta(valores)

    def resultConta(self,valores):
        while True:
            if len(valores) == 1:
                return valores[0]

            elif '/' in valores:
                valores = self.resultadoDiv(valores)

            elif '%' in valores:
                valores = self.resultPercent(valores)

            elif 'x' in valores:
                valores = self.resultadoMult(valores)

            elif self.getPosition('+',valores) != False or self.getPosition('-',valores) != False:
                return self.resultadoSumSub(valores)

    def resultPercent(self,valores):
        while True:
            posicao = self.getPosition('%', valores)
            if posicao != False:
                resultado = self.mul(self.div(valores[posicao - 1],'100'), valores[posicao + 1])
                del (valores[posicao - 1])
                del (valores[posicao - 1])
                valores[posicao - 1] = resultado
            else:
                break

        return valores

    def resultadoDiv(self,valores):
        while True:
            posicao = self.getPosition('/', valores)
            if posicao != False:
                resultado = self.div(valores[posicao - 1], valores[posicao + 1])
                del (valores[posicao - 1])
                del (valores[posicao - 1])
                valores[posicao - 1] = resultado
            else:
                break

        return valores

    def resultadoMult(self,valores):
        while True:
            posicao = self.getPosition('x', valores)
            if posicao != False:
                resultado = self.mul(valores[posicao - 1], valores[posicao + 1])
                del (valores[posicao - 1])
                del (valores[posicao - 1])
                valores[posicao - 1] = resultado
            else:
                break

        return valores

    def resultadoSumSub(self,valores):
        flagArePass = False
        resultado = 0
        for i in range(len(valores)):
            if valores[i] == '+':
                if flagArePass:
                    resultado = self.sum(resultado, valores[i + 1])

                else:
                    resultado += self.sum(valores[i - 1], valores[i + 1])
                    flagArePass = True

            elif valores[i] == '-':
                if flagArePass:
                    resultado = self.sub(resultado, valores[i + 1])

                else:
                    resultado += self.sub(valores[i - 1], valores[i + 1])
                    flagArePass = True

        return resultado

    def getPosition(self,valor,lista):
        for i in range(len(lista)):
            if valor == lista[i]:
                return i
        return False

    def sum(self,stringA,stringB):
        return float(stringA) + float(stringB)

    def sub(self,stringA,stringB):
        return float(stringA) - float(stringB)

    def mul(self,stringA,stringB):
        return float(stringA) * float(stringB)

    def div(self,stringA,stringB):
        return int(stringA) / int(stringB)
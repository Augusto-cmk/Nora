# -*- coding: utf-8 -*-
import sys

from Backend.Recenhecimento import Nora
from Backend.conexao import test_conexao


if test_conexao() != True:
    print("Nora: Você não possui conexão com a internet, verifique sua conexão e tente novamente mais tarde!")
    sys.exit(0)

Nora().activate()
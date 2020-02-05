from flask import Flask, flash, redirect, render_template, request, session, abort
import os, difflib, unicodedata, re, language_check
from nltk.tokenize import sent_tokenize, word_tokenize
from werkzeug.utils import secure_filename

tool = language_check.LanguageTool('es-MX')
a = open('pgraves.txt', 'r', encoding='utf8')
mensaje = a.read()
print(mensaje)
a.close()

print('Procesando')
text = mensaje
matches = tool.check(text)
t = len(matches)
pe = open('reporteerror.txt', 'a', encoding='utf-8')
for i in range(0, t):
    print(matches[i].ruleId, matches[i])
    palabrasconerror = (matches[i].ruleId, matches[i])
    pe.write(str(palabrasconerror))
    print(matches[i].ruleId, matches[i].replacements)
new = language_check.correct(text, matches)
print(new)
print(t)
tot = str(t)
pe.close()
print('Resultados')


#detección de acentos
  #lectura del corpus
fca = open('./corpus/corpusagudas.txt', 'r')
corpusagudas = fca.read()
fca.close()

fcg = open('./corpus/corpusgraves.txt', 'r')
corpusgraves = fcg.read()
fcg.close()

fce = open('./corpus/corpusesdrujulas.txt', 'r')
corpusesdrujulas = fce.read()
fce.close()

fcse = open('./corpus/corpussobreesdrujulas.txt', 'r')
corpussobreesdrujulas = fcse.read()
fcse.close()

txtentrada = mensaje.lower()
suprimiraaracteresentrada = str(mensaje)
palabrasentrada = re.sub(
      '¿|\,|\!|\°|\¬|\"|\#|\$|\%|\&|\/|\?|\.|\:|\;|\'|\[|\]|\(|\)|[0-9]|\{|\}|\^|\\\|\`|\+|\-|\+|\*|\~|MORFOLOGIK_RULE_ES|',
      '', suprimiraaracteresentrada)
txtentrada = palabrasentrada.lower()
textoentrada = word_tokenize(txtentrada)





def agudas (corpusagudas,textoentrada,estadoagudas = False):
    # Busqueda AGUDAS
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('Agudas')
    ssa = corpusagudas
    ss2a = unicodedata.normalize("NFKD", ssa).encode("ascii", "ignore").decode("ascii")
    agudas = word_tokenize(ss2a)
    # print(agudas)
    suprimiraaracteres = str(agudas)
    palabrasagudas = re.sub(
          '¿|\,|\!|\°|\¬|\"|\#|\$|\%|\&|\/|\?|\.|\:|\;|\'|\[|\]|\(|\)|[0-9]|\{|\}|\^|\\\|\`|\+|\-|\+|\*|\~|MORFOLOGIK_RULE_ES|',
          '', suprimiraaracteres)
    palabrasagudas = word_tokenize(palabrasagudas)
      ###########print(palabrassobre)
    lista1a = textoentrada
    lista2a = palabrasagudas
    ds = difflib.Differ()
    for search in lista1a:
        matches = sorted(lista2a, key=lambda x: difflib.SequenceMatcher(None, x, search).ratio(), reverse=True)
        ################      print('{0} se compara con {1} es más parecido {2}'.format(search, matches, matches[0]))
        vg = ('{0}'.format(search, matches, matches[0]))
        ng = ('{2}'.format(search, matches, matches[0]))
        print('>', vg + "-" + ng)
        ###########print('++', ng)
        if vg == ng:
           estadoagudas = True
           print(estadoagudas)

        def estadop():
            if estadoagudas == True:
                print('errores en palabras agudas')
                print(estadoagudas)

            else:
                print('falla, no hay palabras agudas')
                print(estadoagudas)
            print('***********************************************************************************')
            return estadoagudas
    estadop()
agudas(corpusagudas,textoentrada)



def graves (corpusgraves,textoentrada,estadograves = False):
    # busqueda GRAVES
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('Graves')
    ssg = corpusgraves
    ss2g = unicodedata.normalize("NFKD", ssg).encode("ascii", "ignore").decode("ascii")
    graves = word_tokenize(ss2g)
    suprimiraaracteressobre = str(graves)
    palabrasgrave = re.sub(
        '¿|\,|\!|\°|\¬|\"|\#|\$|\%|\&|\/|\?|\.|\:|\;|\'|\[|\]|\(|\)|[0-9]|\{|\}|\^|\\\|\`|\+|\-|\+|\*|\~|MORFOLOGIK_RULE_ES|',
        '', suprimiraaracteressobre)
    palabrasgrave = word_tokenize(palabrasgrave)
    ###########print(palabrassobre)
    lista1g = textoentrada
    lista2g = palabrasgrave
    ds = difflib.Differ()
    estadograves = False
    for search in lista1g:
        matches = sorted(lista2g, key=lambda x: difflib.SequenceMatcher(None, x, search).ratio(), reverse=True)
        # print('{0} se compara son {1} es más parecido {2}'.format(search, matches, matches[0]))
        vg = ('{0}'.format(search, matches, matches[0]))
        ng = ('{2}'.format(search, matches, matches[0]))
        print('>', vg + "-" + ng)
        if vg == ng:
           estadograves = True
           print(vg + ng)

    def estadograves ():
        if estadograves == True:
            print('errores en palabras graves')
            print(estadograves)
        else:
            print('falla, sin palabras graves: ', estadograves)
        print('**********************************************************')
    estadograves()

graves(corpusgraves, textoentrada)




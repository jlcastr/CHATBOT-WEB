from flask import Flask, flash, redirect, render_template, request, session, abort
import os, difflib, unicodedata, re, language_check
from nltk.tokenize import sent_tokenize, word_tokenize
from werkzeug.utils import secure_filename
from datetime import datetime






app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = './Archivos'#carga

#fecha y hora
now = datetime.now()
año = now.year
year = str(año)
mes = now.month
mount = str(mes)
dia = now.day
day = str(dia)
hora = now.hour
hour = str(hora)
minutos = now.minute
minutes = str(minutos)
secons = now.second
seconds = str(secons)


fechahora = (day+"-"+mount+"-"+year+"-"+hour+"-"+minutes+"-"+seconds)
print(fechahora)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('formulario.html')
        #return "Hello Boss!  <a href='/logout'>Logout</a>"



@app.route('/login', methods=['POST'])
def do_admin_login():
    global username
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        username = request.form['username']
        password = request.form['password']
        session['logged_in'] = True
        print(username, "  ", password)
    if request.form['password'] == '1234' and request.form['username'] == 'julio':
        username = request.form['username']
        password = request.form['password']
        session['logged_in'] = True
        print(username, "  ", password)

    else:
        flash('Error: All the form fields are required. ')
        flash('wrong password!')
    return home()

#analizador de textos
@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files['archivo']

  filename = secure_filename(f.filename)
  # Guardamos el archivo en el directorio "Archivos PDF"
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], username+fechahora+filename))
  # Retornamos una respuesta satisfactoria
  print(filename)

  tool = language_check.LanguageTool('es-MX')
  a = open('./Archivos/'+username+fechahora+filename, 'r',encoding='utf8')
  mensaje = a.read()
  print(mensaje)
  a.close()

  print('Procesando')
  text = mensaje
  matches = tool.check(text)
  t = len(matches)
  pe = open('reporteerror.txt','a',encoding='utf-8')
  for i in range(0, t):
   print(matches[i].ruleId, matches[i])
   palabrasconerror = (matches[i].ruleId, matches[i])
   pe.write(str(palabrasconerror))
   print(matches[i].ruleId, matches[i].replacements)
  new = language_check.correct(text, matches)
  print(new)
  print(t)
  tot=str(t)
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

  tool = language_check.LanguageTool('es-MX')
  print(mensaje)
  print('procesando')
  text = mensaje
  matches = tool.check(text)
  t = len(matches)
  fus = open('./arc/' + username + '.txt', 'a')  # palabras a remplazar

  for i in range(0, t):
      # print(matches[i].ruleId, matches[i])
      # print(matches[i].ruleId, matches[i].replacements)

      p = (matches[i].ruleId, matches[i].replacements)



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
    #busqueda y comparacion
  lista1a = textoentrada
  lista2a = palabrasagudas
  ds = difflib.Differ()
  estadoagudas = False
  for search in lista1a:
      matches = sorted(lista2a, key=lambda x: difflib.SequenceMatcher(None, x, search).ratio(), reverse=True)
      ################      print('{0} se compara con {1} es más parecido {2}'.format(search, matches, matches[0]))
      vg = ('{0}'.format(search, matches, matches[0]))
      ng = ('{2}'.format(search, matches, matches[0]))
      print('>', vg + "-" + ng)
      ###########print('++', ng)
      if vg == ng:
          estadoagudas = True

  if estadoagudas == True:
      print('errores en palabras agudas')
      print(estadoagudas)

  else:
      print('falla, no hay palabras agudas')
      print(estadoagudas)
  print('***********************************************************************************')



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
    #busqueda y comparacion
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
  if estadograves == True:
      print('errores en palabras graves')
      print(estadograves)
  else:
      print('falla, sin palabras graves: ', estadograves)
  print('**********************************************************')

  # palabras ESDRUJULAS
  print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
  print('ESDRUJULAS')
  s = corpusesdrujulas
  s2 = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
  esdrujulas = word_tokenize(s2)

  suprimiraaracteres = str(esdrujulas)
  palabrasesdru = re.sub(
      '¿|\,|\!|\°|\¬|\"|\#|\$|\%|\&|\/|\?|\.|\:|\;|\'|\[|\]|\(|\)|[0-9]|\{|\}|\^|\\\|\`|\+|\-|\+|\*|\~|MORFOLOGIK_RULE_ES|',
      '', suprimiraaracteres)
  palabrasesdru = word_tokenize(palabrasesdru)
    #Busqueda y comparacion
  lista1e = textoentrada
  lista2e = palabrasesdru
  de = difflib.Differ()
  estadoesdrujulas = False
  for search in lista1e:
      matches = sorted(lista2e, key=lambda x: difflib.SequenceMatcher(None, x, search).ratio(), reverse=True)
      # print('{0} se compara con {1} es más parecido {2}'.format(search, matches, matches[0]))
      v = ('{0}'.format(search, matches, matches[0]))
      n = ('{2}'.format(search, matches, matches[0]))
      print('>>>', v + "-" + n)
      if v == n:
          estadoesdrujulas = True
          print(v + n)
  if estadoesdrujulas == True:
      print('errores en palabras esdrujulas')
      print('estado actual: ', estadoesdrujulas)
  else:
      print('falla, sin palabras esdrujulas')
      print('estado actual: ', estadoesdrujulas)
  print('******************************************************************************')

  # palabras SOBREESDRUJULAS
  print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
  print('SOBREESDRUJULAS')
  ss = corpussobreesdrujulas
  ss2se = unicodedata.normalize("NFKD", ss).encode("ascii", "ignore").decode("ascii")
  sobreesdrujulas = word_tokenize(ss2se)
  suprimiraaracteressobre = str(sobreesdrujulas)
  palabrassobre = re.sub(
      '¿|\,|\!|\°|\¬|\"|\#|\$|\%|\&|\/|\?|\.|\:|\;|\'|\[|\]|\(|\)|[0-9]|\{|\}|\^|\\\|\`|\+|\-|\+|\*|\~|MORFOLOGIK_RULE_ES|',
      '', suprimiraaracteressobre)
  palabrassobre = word_tokenize(palabrassobre)
  #busqueda y comparacion
  lista1s = textoentrada
  lista2s = palabrassobre
  ds = difflib.Differ()
  estadosobreesdrujulas = False
  for search in lista1s:
      matches = sorted(lista2s, key=lambda x: difflib.SequenceMatcher(None, x, search).ratio(), reverse=True)
      # print('{0} se compara con {1} es más parecido {2}'.format(search, matches, matches[0]))
      vs = ('{0}'.format(search, matches, matches[0]))
      ns = ('{2}'.format(search, matches, matches[0]))
      print('>', vs + "-" + ns)
      if vs == ns:
          estadosobreesdrujulas = True
  if estadosobreesdrujulas == True:
      print('errores en palabras sobreesdrujulas')
      print('estado actual', estadosobreesdrujulas)
  else:
      print('falla, sin sobreesdrujulas')
      print('estado actual: ', estadosobreesdrujulas)

  global es1,es3,es2,es4

  # prubas para resultados
  if estadosobreesdrujulas == True:
      es1 = 'sobreesdújulas'
      print(es1)
  else:
      print('falso')
      es1 = ' '

  if estadoesdrujulas == True:
      es2 = 'esdrújulas'
      print(es2)
  else:
      print('falso sobre')
      es2 = ' '
  if estadograves == True:
      es3 = 'graves'
      print(es3)
  else:
      es3 = ' '
      print('falso gaves')

  if estadoagudas == True:
      es4 = 'Agudas'
      print(es4)
  else:
      # if estado == False:
      print('falso agudas')
      es4 = ' '

  print(es1, es2, es3, es4)


  """if es4 == True:
      if es3 != True:
          if es1 != True:
              if es2 != True:
                  es4='Agudas,'

  if es4 == True:
      if es1 == False:
          if es2 == False:
              if es4 == False:
                  es4 = "Agudas."""""
  if t==1:
   return "<h1>Felicidades no tiene ningun error</h1>"
  elif t==0:
   return "<h1>Felicidades no tiene ningun error</h1>"
  elif t > 1:
   return render_template('feedback.html', user=username, total=tot, txtorigen=mensaje, erroragu=es4, errorgra=es3, erroresd=es2, errorsob=es1)
   #return " Hola: "+username+"<h1>El archivo se subido exitosamente</h1>"+"<h2>Se detectaron algunos erroes ortográficos</h2>"+'Numero de posibles errores: '+tot+'<h1>Texto original</h1>'+mensaje+'<h2>Palabras con errores detectados</h2>'+perror


@app.route("/logout")
def logout():
        session['logged_in'] = False
        return home()


if __name__ == '__main__':
        app.secret_key = os.urandom(12)
        app.run(debug=True)



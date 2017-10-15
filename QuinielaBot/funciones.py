# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
from telebot import types

bot = telebot.TeleBot(os.environ["TOKENQUINI"])
#Función que nos elimina los tags de la web 
def strip_tags(value):
	return re.sub(r'<[^>]*?>', '', value)

#Devuelve el valor de lo que el usuario introduce (si son dos parámetros). Sino, devuelve -1
def comprobar(m):
	cid = m.chat.id
	cadena_longitud_dinero = m.text.split(" ")
	if len(cadena_longitud_dinero) != 2 :
		bot.send_message(cid, "Cadena errónea. Inténtalo de nuevo. Son 2 parámetros")
		return(-1)
	else:
		return cadena_longitud_dinero

#Devuelve el cid del chat
def cid_(m):
	cid = m.chat.id
	return cid

#Devuelve el valor pasado como argumentos
def asignar_valores(cadena_longitud_dinero):
	numero_ = cadena_longitud_dinero[1]
	return numero_

#Devuelve los resultados en forma de string
def revisar_resultados(resultados_usuario):
	#Se realiza la petición a la web
	URL = "https://loteriasyapuestas.es/es/la-quiniela/"
	req = requests.get(URL)

	cadena_sol = ""
	contador = 1 #Pleno al 15
	contador_guion = 0

	#Recorremos los resultados
	for i in range(len(resultados_usuario)):
		if (resultados_usuario[i] != "u'-'" and i != 29): #No tiene - y no es el guión del pleno al 15
			contador +=1
			cadena_sol += resultados_usuario[i].replace("-","") #Reemplazamos ese -
		else: #Si se trata del guión del pleno
			if i == 29: #Tiene - en la posición del pleno al 15
				cadena_sol += "-" #Se lo dejamos para luego comprobar 
	

	resultados_auxiliar = "" 
	resultados_final = ""
	finalresultados_sin_tags = ""
	solo_digitos = ""

	#Hacemos las llamadas a la web
	html = BeautifulSoup(req.text, "html.parser")
	cuadro_resultados = html.find_all('div', {'class': 'contedorResultados contenedorNuevo'})


	for i in cuadro_resultados:
		#Resultados
		resultados = i.find('ul', {'class': 'fondoGrisClaro'}) #Guardo los resultados que han sido encontrados en la tabla
		resultados_auxiliar += str(resultados) #Lo convertimos a string y lo pasamos a un auxiliar
		resultados_final += str(resultados_auxiliar) #Resultado por separado de los resultados en un string

		#Le quitamos los tags a los equipos y a los resultados
		finalresultados_sin_tags += strip_tags(resultados_final)

	#Recorremos los resultados para dejar solo los dígitos, sin espacios ni caracteres especiales
	for j in range(len(finalresultados_sin_tags)):
		if (finalresultados_sin_tags[j].isdigit() == True or finalresultados_sin_tags[j] == 'M' or finalresultados_sin_tags[j] == 'X' or finalresultados_sin_tags[j] == '-'):
			solo_digitos += finalresultados_sin_tags[j] #Si se cumple, añadimos al string el carácter en cuestión
			#String solo_digitos contiene los resultados de los partidos.
	
	comprobacion = solo_digitos #Le copiamos el valor para recorrerlo ahora y no sobreescribir datos
	contador = 0
	aniadir = "" #Por si ha acertado el pleno al 15, decirselo al usuario
	contador_pleno = 0 #Para saber si acierto el pleno o no
	
	if len(comprobacion) != len(cadena_sol): #Si las cadenas no son iguales
		return ("ERROR, La cadena introducida no tiene la misma longitud que los resultados de la Quiniela")
	else:	
		for i in range(len(comprobacion)): #Mismas longitud, recorremos la cadena de resultados
			if comprobacion[i] == cadena_sol[i] and i < 14: #Si la posicion i de ambas cadenas son la misma y no estoy en el pleno al 15
				contador +=1
			else:
				contador = contador
		#Pleno al 15, si las 3 últimas posiciones son iguales, pleno acertado, 1 acierto más
		if (comprobacion[14] == cadena_sol[14] and comprobacion[15] == cadena_sol[15] and comprobacion[16] == cadena_sol[16]):
			contador_pleno = 1
			aniadir = " contando con el pleno al 15"

	#Vemos el premio que le ha tocado llamando a la función que lo calcula	
	if contador_pleno == 1 and contador == 14:
		premio = dinero_(15)
	else:
		premio = dinero_(contador)
	
	#Le añadimos el valor de lo que le ha tocado y lo devolvemos
	result = str(contador+contador_pleno) + " aciertos has tenido" + str(aniadir) + " y tu premio es de " + str(premio)

	return result



def resultados_():
	#Se realiza la petición a la web
	URL = "https://loteriasyapuestas.es/es/la-quiniela/"
	req = requests.get(URL)
		
	#Comprobar que sea correcto
	statusCode = req.status_code

	if statusCode == 200:
		equipos_auxiliar = ""
		resultados_auxiliar = ""
		equipos_final = ""
		resultados_final = ""
		finalequipos_sin_tags = ""
		finalresultados_sin_tags = ""
		solo_digitos = ""
		string_auxiliar_equipos = ""
		string_solucion = ""


		#Hacemos las llamadas a la web 
		html = BeautifulSoup(req.text, "html.parser")
		cuadro_resultados = html.find_all('div', {'class': 'contedorResultados contenedorNuevo'})

		for i in cuadro_resultados:
			#Equipos
			equipos = i.find('ul', {'class': 'puntosSusp'}) #Guardo los equipos que han sido encontrados en la tabla
			equipos_auxiliar += str(equipos)	#Lo convertimos a string y lo pasamos a un auxiliar 
			equipos_final += str(equipos_auxiliar) #Resultado por separado de los equipos en un string

			#Resultados
			resultados = i.find('ul', {'class': 'fondoGrisClaro'}) #Guardo los resultados que han sido encontrados en la tabla
			resultados_auxiliar += str(resultados) #Lo convertimos a string y lo pasamos a un auxiliar
			resultados_final += str(resultados_auxiliar) #Resultado por separado de los resultados en un string

			#Le quitamos los tags a los equipos y a los resultados
			finalequipos_sin_tags += strip_tags(equipos_final)
			finalresultados_sin_tags += strip_tags(resultados_final)


		#Recorremos los resultados para dejar solo los dígitos, sin espacios ni caracteres especiales
		for j in range(len(finalresultados_sin_tags)):
			if (finalresultados_sin_tags[j].isdigit() == True or finalresultados_sin_tags[j] == 'M' or finalresultados_sin_tags[j] == 'X' or finalresultados_sin_tags[j] == '-'):
				solo_digitos += finalresultados_sin_tags[j] #Si se cumple, añadimos al string el carácter en cuestión
				#String solo_digitos contiene los resultados de los partidos.


		indice = 0 #Variable int para contemplar cuándo es pleno al 15
		primera_iteracion = True #Booleano para contemplar que en la primera iteración no haya un \n
		string_auxiliar_pleno = "" #String que usaremos como auxiliar para almacenar el pleno al 15
	
		#Recorremos el string de los equipos
		for k in range(len(finalequipos_sin_tags)):
			#Si el carácter en cuestión es un \n y no es la primera iteración
			if (finalequipos_sin_tags[k] == '\n' and primera_iteracion != True):
				#Si el valor del índice es 14 (pleno al 15)
				if indice == 14:
					#r = 0 #Para el pleno al 15
					#Recorremos los 3 valores que dispone el pleno al 15
					for i in range(14,17):
						string_auxiliar_pleno += solo_digitos[i] #Añadimos los dígitos en cuestión sólo del pleno al 15
						#Si la longitud del string es 3
						if len(string_auxiliar_pleno) == 3:
							#Añadimos el resultado del pleno al string solución
							string_solucion += string_auxiliar_equipos + " " + string_auxiliar_pleno + '\n'
				#Si no es pleno al 15
				else:	
					#Añadimos los equipos en cuestión más el resultado
					string_solucion += string_auxiliar_equipos + " " + solo_digitos[indice] + '\n'
					#Aumentamos el índice
					indice+=1
					#Vaciamos el string de los equipos para que no salgan duplicados
					string_auxiliar_equipos = ""
			#Si no es un \n
			else:
				#Almacenamos los equipos
				string_auxiliar_equipos += finalequipos_sin_tags[k]

			#Ponemos a false el booleano
			primera_iteracion = False

	else:
		print ("Error, estatus code = ", statusCode)

	return string_solucion

def dinero_(n_aciertos):
	print ("ACIERTOS = " , n_aciertos)
	URL2 = "https://resultados.as.com/quiniela/"
	req2 = requests.get(URL2)

	#Comprobar que sea correcto
	statusCode = req2.status_code

	if statusCode == 200:
		aciertos_auxiliar = ""
		cadena_final_sin_saltos = ""
		finalaciertos_sin_tags = ""
		aciertos_final = ""

		#Hacemos las llamadas a la web
		html2 = BeautifulSoup(req2.text, "html.parser")
		cuadro_dinero = html2.find_all('table', {'class': 'data-table table-striped'})

		#Sacamos la información de la tabla
		for i in cuadro_dinero:
			aciertos = i.find_all('td', {'class': 's-tright'})
			aciertos_auxiliar += str(aciertos) # Lo convertimos en string
			aciertos_final += str(aciertos_auxiliar) #Lo vamos acumulando
		
			finalaciertos_sin_tags += strip_tags(aciertos_final) #Le quitamos los tags del html

		#For que recorre los resultados y los imprime
		cadena_solucion = "" #Cadena donde va a encontrarse la solución de los premios ordenados
		for i in range(len(finalaciertos_sin_tags)):
			cadena_aux = "" #Usaremos una auxiliar para ir acumulando los caracteres
			#Si se trata de un digito o es "." ó "," , almacenamos el valor
			if (finalaciertos_sin_tags[i].isdigit() == True or finalaciertos_sin_tags[i] == '.' or finalaciertos_sin_tags[i] == ','):
				cadena_aux += finalaciertos_sin_tags[i]
			#Si se trata de una "," y el siguiente es un espacio en blanco
			if (finalaciertos_sin_tags[i] == "," and finalaciertos_sin_tags[i+1] == ' '):
				#Reemplazamos la , por un espacio en blanco y le añadimos € más salto de línea
				cadena_aux = cadena_aux.replace(","," ") + '€' + '\n' 
			cadena_solucion += cadena_aux #Almacenamos nuestra solución
		cadena_solucion += ' €' #Añadimos el símbolo


		vector_solucion = [] 
		vector_solucion = cadena_solucion.split() #Convertimos de string a list
		devolver_dinero = []
		#Vemos las opciones que hay en función de lo que nos diga el usuario
		for i in vector_solucion:
			if (n_aciertos == u'15') or (n_aciertos == 15):
				devolver_dinero = (vector_solucion[0] + "€")
			elif (n_aciertos == u'14') or (n_aciertos == 14):
				devolver_dinero = (vector_solucion[2] + "€")
			elif (n_aciertos == u'13') or (n_aciertos == 13):
				devolver_dinero = (vector_solucion[4] + "€")
			elif (n_aciertos == u'12') or (n_aciertos == 12):
				devolver_dinero = (vector_solucion[6] + "€")
			elif (n_aciertos == u'11') or (n_aciertos == 11):
				devolver_dinero = (vector_solucion[8] + "€")
			elif (n_aciertos == u'10') or (n_aciertos == 10):
				devolver_dinero = (vector_solucion[10] + "€")
			else:
				devolver_dinero = ("0,00€")
			break
		
	else:
		print ("Error, estatus code = ", statusCode)

	return devolver_dinero

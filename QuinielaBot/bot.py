# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import telebot
import os
from telebot import types
import funciones

bot = telebot.TeleBot(os.environ["TOKENQUINI"])

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	cid = message.chat.id # Guardamos el ID de la conversacion para poder responder.
	bot.send_message(cid, "Introduzca acción que desea realizar.\nAcciones: \n1. /Resultados: Devuelve los resultados de la quiniela de la última semana\n2. /Premio: Devuelve la cantidad de dinero que le ha tocado, según el número de aciertos\n3. /Comprobar: Comprueba el número de aciertos que has tenido al terminar la Quiniela.Debes escribir tus resultados separados por -\n\nEjemplo:/Resultados ó /Premio 13 ó /Comprobar 1-X-....-2-M-2")


@bot.message_handler(commands=['Resultados', 'resultados'])
def send_resultados(m):
	cid = funciones.cid_(m) # Guardamos el ID de la conversacion para poder responder.
	devolver_resultados = funciones.resultados_()
	bot.send_message(cid,devolver_resultados)

@bot.message_handler(commands=['Premio', 'premio'])
def send_dinero(m):
	cid = funciones.cid_(m)
	cadena_dinero = funciones.comprobar(m)

	if cadena_dinero == -1:
		return (-1)
	else:
		devolver_din = funciones.asignar_valores(cadena_dinero)
		resultado_dinero = funciones.dinero_(devolver_din)
		
		bot.send_message(cid,resultado_dinero)

@bot.message_handler(commands=['Comprobar', 'comprobar'])
def send_comprobar_aciertos(m):
	cid = funciones.cid_(m)
	cadena_resultados = funciones.comprobar(m)

	if cadena_resultados == -1:
		return (-1)

	else:
		prueba = ""
		prueba = funciones.asignar_valores(cadena_resultados)
		resultado_prueba = funciones.revisar_resultados(prueba)
		bot.send_message(cid,resultado_prueba)
		

bot.polling() # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.

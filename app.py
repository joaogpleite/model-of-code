import os

import gspread
import requests
import pandas
import telebot
from flask import Flask
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper


TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as fobj:
  fobj.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta) 
planilha = api.open_by_key("1bmLZIrWU1GG_ikJKRcZNtmmFELcYrBK2dMYqFQIV0Gs")
sheet = planilha.worksheet("lic1")
app = Flask(__name__)

@bot.message_handler(commands=['classificar'])
def classify(message):
    # open the Google Sheets document
    sheet = client.open_by_url(doc_url).sheet1

    # get the values from the cells and create a pandas DataFrame
    data = sheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)

    # Classify the data
    modalidades = df['Modalidade'].value_counts()
    finalidades = df['Finalidade/Objeto/Serviço'].value_counts()
    situacoes = df['Situação'].value_counts()

    dispensa = modalidades.get('Dispensa de Licitacao', 0)
    chamada = modalidades.get('Chamada Publica', 0)
    convite = modalidades.get('Convite', 0)

    andamento = situacoes.get('andamento', 0)
    aberto = situacoes.get('em aberto', 0)
    encerrada = situacoes.get('encerrada', 0)

    # send the response to the user
    response = f"Dispensa de Licitação: {dispensa}\n"
    response += f"Chamada Pública: {chamada}\n"
    response += f"Convite: {convite}\n"
    response += f"-----------------------------------\n"
    response += f"Andamento: {andamento}\n"
    response += f"Em aberto: {aberto}\n"
    response += f"Encerrada: {encerrada}"
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Olá, para classificar a sua planilha digite classificar")



bot.polling()

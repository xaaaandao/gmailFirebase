# GMAIL API
from __future__ import print_function
import httplib2
import os
import json
from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

"""
  Descrição: seriam métodos relacionados a API do GMAIL, que permitem obter e ler o conteúdo das mensagens, dependendo do que foi
  passado na query.
  Autor: Alexandre Yuji Kajihara.
  Data de criação: 02/04/2018
  Data de atualização: 02/04/2018
"""

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

"""
  Se modificar o escopo, exclua suas credenciais salvas anteriormente em ~/.credentials/gmail-python-quickstart.json
"""
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

"""
  O método ListMessagesMatchingQuery(service, user_id, query=''), a partir de usuário de ID e uma query, procura e-mails com aquela
  característica e retorna os e-mails com essas características em uma lista.
  @param service, é uma instância autorizando API do GMAIL.
  @param user_id, é o id do usuário.
  @param query, é uma string que se refere-se que tipo de e-mail devem ser armazenados na lista (exemplo: e-mail não lidos, e-mail de certo destinatário)
  @return messages, que é uma lista de mensagens.
"""
def ListMessagesMatchingQuery(service, user_id, query=''):
  try:
    # Pega o response dado um id de usuário e uma query (que pode ser as mensagens que não foram lidas, ou as que são de certo remetente, etc)
    response = service.users().messages().list(userId=user_id, q=query).execute()

    # Inicializa messages como uma lista vazia    
    messages = []

    # Verifica se no response tem algum índice messages, e concatena na lista que foi inicializada anteriormente
    if 'messages' in response:
      messages.extend(response['messages'])

    # Vai concatenando se encontra no response algum índice messages, e concatena na lista
    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
      messages.extend(response['messages'])

    # Retorna a lista de mensagens
    return messages
  
  # Se for exceção printa que o erro aconteceu
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

"""
  O método get_credentials(), pega as credenciais do usuário que estão armazenadas, caso elas não estejam armazenadas
  ou forem inválidas, o OAuth2 flow irá obter novas credenciais.
  @param nenhum parâmetro.
  @return credentials, que são credenciais que estavam armazenadas, ou novas credenciais.
"""
def get_credentials():
    # Pega o diretório home
    home_dir = os.path.expanduser('~')

    # Pega o diretório credentials
    credential_dir = os.path.join(home_dir, '.credentials')

    # Verifica se não tem o diretorio .credentials
    if not os.path.exists(credential_dir):
      # Caso nao tenha cria o diretório
      os.makedirs(credential_dir)

    # Vai criar no diretório anterior um .json 
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()

    # Se não tiver as credenciais ou se as credenciais forem inválidas
    if not credentials or credentials.invalid:
        # Cria um fluxo para o arquivo client_secret.json
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        # Usada para adqurir credenciais
        if flags:
            credentials = tools.run_flow(flow, store, flags)

        # Também usada para adqurir credenciais
        # Needed only for compatibility with Python 2.6
        else: 
            credentials = tools.run(flow, store)

        # Imprime onde a credencial foi armazenada
        print('Storing credentials to ' + credential_path)

    # Retorna as credenciais
    return credentials


"""
  O método GetMessage(service, user_id, msg_id), a partir de usuário de ID e um ID de mensagem, retorna a mensagem 
  daquele ID e marca a mensagem como lida.
  @param service, é uma instância autorizando API do GMAIL.
  @param user_id, é o id do usuário.
  @param msg_id, é o id da mensagem.
  @return message, que é o conteúdo da mensagem.
"""
def GetMessage(service, user_id, msg_id):
  try:
    # Pega a mensagem
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    # Marca como lido a mensagem
    message = service.users().messages().modify(userId=user_id, id=msg_id, body={ 'removeLabelIds': ['UNREAD']}).execute()

    # Retorna a mensagem
    return message

  # Se for excecao printa que o erro aconteceu
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

"""
  O método getDateTimeMessage(message), retorna a data de recebimento do e-mail.
  @param message, que é o .json onde vêm as informações do e-mail.
  @return date, que é a data de recebimento do e-mail.
"""
def getDateTimeMessage(message):
  i = 0
  while(True):
    # Percorre o .json e procura um campo name com o valor date
    if(message['payload']['headers'][i]['name'] == 'Date'): 
      # Retorna o campo de value do campo name com o valor date
      return message['payload']['headers'][i]['value']
    i = i + 1

"""
  O método getBodyOfEmail(service, listOfMessage), a partir de usuário de ID e um ID de mensagem, retorna a mensagem 
  daquele ID e marca a mensagem como lida.
  @param service, é uma instância autorizando API do GMAIL.
  @param listOfMessage, é uma lista de mensagens.
  @return void, ou seja, nada.
"""
def getBodyOfEmail(service, listOfMessage):
  # Roda um for na lista de mensagens e pegando o conteúdo delas
    for message in listOfMessage:
      bodyOfMessage = GetMessage(service, 'me', message['id'])  
      print(bodyOfMessage['snippet'], getDateTimeMessage(bodyOfMessage))

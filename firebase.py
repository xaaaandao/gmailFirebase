# FIREBASE
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

"""
  Descrição: seriam métodos relacionados a conexão do Firebase e da inserção de dados no Firebase.
  Autor: Alexandre Yuji Kajihara.
  Data de criação: 02/04/2018
  Data de atualização: 02/04/2018
"""

"""
  O método firebaseConnection(), conecta ao database a partir da URL e da credencial, de um usuário que foi cadastrado.
  @param nenhum parâmetro.
  @return db.reference(), que é uma referência ao database.
"""
def firebaseConnection():
	# O .json que é usado na credencial é gerado quando você cadastra um usuário
	cred = credentials.Certificate("key.json")

	# Inicializa a aplicação com a credencial e a URL do database
	firebase_admin.initialize_app(cred, {'databaseURL' : 'https://your_url.firebaseio.com/'})

	# Retorna a referência do database
	return db.reference(path="/", app=None)

"""
  O método firebaseAddData(ref), a partir da referência que foi passada ele irá adicionar valores, no formato de .json.
  @param ref, que é a referência ao database.
  @return void, ou seja, nada.
"""
def firebaseAddData(ref):
	# Cria um nó na raíz chamado server
	users_ref = ref.child('server')

	# Coloca os dados naquele nó do filho
	users_ref.set({
	    'alanisawesome': {
	        'date_of_birth': 'June 23, 1912',
	        'full_name': 'Alan Turing'
	    },
	    'gracehop': {
	        'date_of_birth': 'December 9, 1906',
	        'full_name': 'Grace Hopper'
	    },
	    'show': {
	        'date_of_birth': 'December 9, 1909',
	        'full_name': 'Grace Hopper'
	    }
	})
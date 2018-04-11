# GMAIL API
import gmailapi

# FIREBASE
import firebase

def main():
    # Pega as credenciais
    credentials = gmailapi.get_credentials()

    # Autoriza as credenciais
    http = credentials.authorize(gmailapi.httplib2.Http())

	# Cria um serviço de objeto GMAIL API
    service = gmailapi.discovery.build('gmail', 'v1', http=http)

    # Conexão com o firebase
    ref = firebase.firebaseConnection()

	# Fica no loop infinito
    while(True):
    	# Guarda a lista de e-mails
    	listOfMessage = gmailapi.ListMessagesMatchingQuery(service, 'me', query='is: unread')
    	
    	# Se tem e-mails que não foram lidos
    	if(listOfMessage):
    		# Leio o conteúdo deles
    		gmailapi.getBodyOfEmail(service, listOfMessage)

    		# Adiciono no firebase
    		firebase.firebaseAddData(ref)

# Chama o main()
if __name__ == '__main__':
    main()

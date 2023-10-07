# From https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat
from autogen import AssistantAgent, UserProxyAgent
import requests

import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build



def get_google_doc_text(creds, document_id):
    service = build('docs', 'v1', credentials=creds)
    doc = service.documents().get(documentId=document_id).execute()
    doc_content = doc.get('body').get('content')
    
    text = ""
    for value in doc_content:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                try:
                    text += elem.get('textRun').get('content')
                except:
                    pass

    return text

creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')

# Si no hay credenciales (válidas) disponibles, deja que el usuario inicie sesión.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'path_to_your_credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Guarda las credenciales para la próxima ejecución
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


# create an AssistantAgent instance named "assistant"

def fetch_text_from_url(url):
    response = requests.get(url)
    
    # Verifica que la petición se haya completado con éxito
    response.raise_for_status()
    
    return response.text


massa_texto = fetch_text_from_url("https://docs.google.com/document/d/1xZoMVnmTxs80WT_NsGkvLC-a-nl-LzQxlX_TOnnAbwE")
    
massa_texto = massa_texto[:4000]
assistant_massa = AssistantAgent(name="Massa",
                                 system_message = massa_texto
)

milei_texto = fetch_text_from_url("https://docs.google.com/document/d/1danjDzXG6VIcnoGAv-AL1naOzNyFrU0j5VnZvFhi-7w/")
milei_texto = milei_texto[:4000]

assistant_milei = AssistantAgent(name="Milei",
                                 system_message = milei_texto)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(name="user_proxy")

# the assistant receives a message from the user, which contains the task description
#user_proxy.initiate_chat(
#    assistant_massa,
#    assistant_milei,
#    message="""Pueden empezar a debatir sobre un plan economico con no más de 4 intercambios""",
#)

assistant_massa.initiate_chat(
    assistant_milei,
    message="""Javier, te invito a debatir sobre un posible plan económico y te propongo que cerremos después de 4 respuestas tuyas""",
)
# From https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat
from autogen import AssistantAgent, UserProxyAgent
import requests

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

milei_texto = fetch_text_from_url("https://docs.google.com/document/d/1danjDzXG6VIcnoGAv-AL1naOzNyFrU0j5VnZvFhi-7w/edit")
milei_texto = massa_texto[:4000]

assistant_milei = AssistantAgent(name="Milei",
                                 system_message = milei_texto)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(name="user_proxy")

# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    assistant_massa,
    assistant_milei,
    message="""Pueden empezar a debatir sobre un plan economico""",
)

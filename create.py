import os
import chromadb
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

client = chromadb.HttpClient(host='localhost', port=8000)
col = client.get_or_create_collection(name="hola")

conversation_from_frontend = [
  { "role": "user", "content": "Hola" },
  { "role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy?" },
  { "role": "user", "content": "Quien fue el ganador de la copa del mundo de la FIFA en el año 2018?" },
  { "role": "assistant", "content": "El ganador de la Copa del Mundo de la FIFA en 2018 fue la selección nacional de fútbol de Francia." },
  { "role": "user", "content": "y en el año 2014" },
  { "role": "assistant", "content": "El ganador de la Copa del Mundo de la FIFA en 2014 fue la selección nacional de fútbol de Alemania." },
  { "role": "user", "content": "Ya veo. Y sabes quien gano la copa en el 2010?" },
  { "role": "assistant", "content": "Sí, en 2010, la Copa del Mundo de la FIFA fue ganada por la selección nacional de fútbol de España." },
  { "role": "user", "content": "Genial, muchas gracias" },
  { "role": "assistant", "content": "De nada, ¡si tienes más preguntas, no dudes en preguntar!" },
  { "role": "user", "content": "Hasta que fecha estas actualizado? Es decir, te puedo perguntar eventos del 2023 y del 2024?" },
  { "role": "assistant", "content": "Mi conocimiento se extiende hasta la fecha en que fui desarrollado, por lo que no tengo información actualizada sobre eventos específicos en el futuro, como eventos del 2023 o 2024. Sin embargo, estaré encantado de ayudarte en la medida de mi capacidad." },
  { "role": "user", "content": "Hasta que fecha fuiste desarrollado?" },
  { "role": "assistant", "content": "Fui desarrollado con información actualizada hasta septiembre de 2021. Por lo tanto, mi conocimiento está basado en información disponible hasta esa fecha." },
  { "role": "user", "content": "Ya veo, muchas gracias" },
  # { "role": "assistant", "content": "" },
  # { "role": "user", "content": "" },
  # { "role": "assistant", "content": "" },
]

last_message = conversation_from_frontend[-1]


if(last_message["role"] == "user"):
  col.add(
    documents=[str(last_message)],
    ids=[f"{len(conversation_from_frontend)}"]
  )

client = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.7)

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system", "You are Yorch AI a helpful assistant created by Jorge Ortiz. Answer the following questions as you can.", 
    ),
    MessagesPlaceholder(variable_name="messages")
  ]
)

conversation = ChatMessageHistory()

for message in conversation_from_frontend:
  if message["role"] == "user":
    conversation.add_user_message(message["content"])
  else:
    conversation.add_ai_message(message["content"])

chain = prompt | client

response = chain.invoke({ "messages": conversation.messages })

conversation_from_frontend.append({ "role": "assistant", "content": response.content })

last_message = conversation_from_frontend[-1]

if(last_message["role"] == "assistant"):
  col.add(
    documents=[str(last_message)],
    ids=[f"{len(conversation_from_frontend)}"]
  )

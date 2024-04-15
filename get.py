import os
import chromadb
from dotenv import load_dotenv
from dotenv import load_dotenv

load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

client = chromadb.HttpClient(host='localhost', port=8000)
col = client.get_collection(name="hola")

conversation = [] 

res = col.get()
ids = res["ids"]
documents = res["documents"]

for i in range(len(ids)):
  conversation.append({ "id": f"{ids[i]}", "document": f"{documents[i]}" })

for message in conversation: 
  print(message)

# print(res)

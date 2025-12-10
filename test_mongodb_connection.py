from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://root:password@localhost:27017')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'morphia_db')

try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ MongoDB conectado com sucesso!")
    
    db = client[MONGODB_DATABASE]
    print(f"✅ Banco de dados '{MONGODB_DATABASE}' acessado!")
    
    # Teste de inserção
    test_collection = db['test_collection']
    result = test_collection.insert_one({'test': 'sucesso', 'message': 'Conexão funcionando!'})
    print(f"✅ Documento inserido com ID: {result.inserted_id}")
    
    # Teste de leitura
    doc = test_collection.find_one({'test': 'sucesso'})
    print(f"✅ Documento recuperado: {doc}")
    
    client.close()
    print("✅ Conexão fechada com sucesso!")
    
except ServerSelectionTimeoutError:
    print("❌ Erro: MongoDB não está acessível. Verifique se o container está rodando.")
except Exception as e:
    print(f"❌ Erro: {e}")

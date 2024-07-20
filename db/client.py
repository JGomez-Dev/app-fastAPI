from pymongo import MongoClient

# Base de datos local
# db_client = MongoClient().local

# Base de datos remota
db_client = MongoClient("mongodb+srv://javiergf1991:lB4WFTdPy7v7tFGL@cluster0.jusrkg5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").python

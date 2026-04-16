from pymongo import MongoClient


client = MongoClient("mongodb+srv://lironef_db_user:dGbUbRU8k7475lUC@cluster0.82afdwe.mongodb.net/prod?appName=Cluster0")
db = client["prod"]
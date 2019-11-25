from pymongo import MongoClient
client = MongoClient()
db = client['easyCook']['ingredient']
filter =  { 'name': 'Harina' }
query = { '$set' : { 'name': 'Harina', 'measure': 'Kilos', 'equivalents' : [ ] } }
db.update_one(filter,query, upsert = True)

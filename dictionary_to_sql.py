import json
import mysql.connector
with open('value_dict_1.json', 'r') as f:
    value_dict_1 = json.load(f)
with open('value_dict_2.json', 'r') as f:
    value_dict_2 = json.load(f)
value_dict_1 = {key: str(value) for key, value in value_dict_1.items()}
value_dict_2 = {key: str(value) for key, value in value_dict_2.items()}
for key in list(value_dict_1.keys()):
    new_key = key.strip()
    if new_key != key:
        value_dict_1[new_key] = value_dict_1.pop(key)
for key in list(value_dict_1.keys()):
    new_key = key.strip().replace("_", " ")
    if new_key != key:
        value_dict_1[new_key] = value_dict_1.pop(key)
def connect_dicts(dict1, dict2):
    result = {}
    for key, value in dict1.items():
        if value in dict2:
            result[key] = dict2[value]
    return result
final_dict=connect_dicts(value_dict_1,value_dict_2)
db=mysql.connector.connect(user='root',password='admin',host= 'localhost')
cursor=db.cursor()
cursor.execute('USE main_database;')
cursor = db.cursor()


query = "INSERT INTO dict_value (model, encoded) VALUES (%s, %s)"

for key, value in final_dict.items():
    values = (key, value)
    cursor.execute(query, values)
db.commit()
cursor.close()
db.close()
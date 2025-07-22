import json

filepath = "data/test.json"
with open(filepath, "r", encoding="utf-8") as file:
    datas = json.load(file)

print(len(datas))
dic_len = 0

if len(datas) >= 10:
    print(datas[-5:])
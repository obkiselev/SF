# classifier/application/routes.py

# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from application import app #Cкрипт run.py находитс€ на верхнем уровне и содержит всего одну строку, котора€ импортирует экземпл€р приложени€: from application import app

@app.route('/')#ƒекоратор @app.route создает св€зь между URL-адресом, заданным как аргумент (/), и функцией hello_world().  Ёто означает, что когда веб-браузер
#запрашивает этот URL-адрес, Flask будет вызывать эту функцию и передавать ее возвращаемое значение обратно в браузер в качестве ответа.

#def hello_world():
#    return 'Hello, World!'#возвращает приветствие в виде строки.

@app.route('/hello_user', methods=['POST'])
def hello_user():
#    data = request.json
    data = request.get_json()
    user = data['user']
    return f'hello {user}'

#@app.route('/hello_user', methods=['GET', 'POST'])
#def hello_user():
#   data = request.json
#   print (data['user'])
#   return 1#jsonify({"uuid":uuid})

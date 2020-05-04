# classifier/application/routes.py

# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from application import app #C����� run.py ��������� �� ������� ������ � �������� ����� ���� ������, ������� ����������� ��������� ����������: from application import app

@app.route('/')#��������� @app.route ������� ����� ����� URL-�������, �������� ��� �������� (/), � �������� hello_world().  ��� ��������, ��� ����� ���-�������
#����������� ���� URL-�����, Flask ����� �������� ��� ������� � ���������� �� ������������ �������� ������� � ������� � �������� ������.

#def hello_world():
#    return 'Hello, World!'#���������� ����������� � ���� ������.

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

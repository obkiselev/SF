from flask import Flask, request
from application import app

@app.route('/')
@app.route('/hello_user', methods=['POST'])
def hello_user():
    if not request.json:# or not 'user' in request.json:
        return 'error!'
    data = request.json
    user = data['user']
    return f'hello {user}'

from flask import Flask, request
from application import app

@app.route('/')
@app.route('/calc', methods=['POST'])
def calc():
    if not request.json:
        return 'error!'
    data = request.json
    num_old = int(data['num'])
    num_new = num_old + 1
    return f'old number = {num_old}, new number = {num_new}'

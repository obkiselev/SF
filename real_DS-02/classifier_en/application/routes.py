from flask import Flask, request, jsonify
from application import app
from spam_classifier_en import classify

@app.route('/')

#@app.route('/classify_text', methods=['POST'])
#def classify_text():
#    data = request.json
#    text = data['text']
#    result = classify(text)
#    return jsonify({'result': result})

@app.route('/classify_text', methods=['POST'])
def classify_text():
    data = request.json
    text = data.get('text') 
	#����� ���������� None, ���� �������������� ����� ���
    if text is None:
        params = ', '.join(data.keys()) 
	#����������� ��� ���������� ��������� � ������
        return jsonify({'message': f'Parametr "{params}" is invalid'}), 400 
	#����� �� �� ��������� ��� ������ HTTP ����,
	#�� �� ����� ���� Flask �������� ��� ������ �� ���. 
	#�� ��������� ������������ 200
    else:
        result = classify(text)
        return jsonify({'result': result})

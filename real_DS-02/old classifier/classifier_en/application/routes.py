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
	#ћетод возвращает None, если запрашиваемого ключа нет
    if text is None:
        params = ', '.join(data.keys()) 
	#ѕреобразуем все полученные параметры в строку
        return jsonify({'message': f'Parametr "{params}" is invalid'}), 400 
	#–анее мы не указывали код ответа HTTP €вно,
	#но на самом деле Flask выполн€л эту работу за нас. 
	#ѕо умолчанию возвращаетс€ 200
    else:
        result = classify(text)
        return jsonify({'result': result})

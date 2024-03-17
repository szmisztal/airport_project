from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')

    # Dane dla żądania JSON-RPC
    rpc_data = {
        "jsonrpc": "2.0",
        "method": "multiply",
        "params": [x, y],
        "id": 1,
    }

    # Wywołanie funkcji RPC
    response = requests.post('http://localhost:5000', json=rpc_data)
    result = response.json().get('result', 'Błąd podczas wywoływania funkcji RPC')

    return jsonify(result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    response = requests.post('http://localhost:8080/multiply', json={'x': 5, 'y': 3})
    print(response.json())

from flask import Flask, request, abort
import json
import requests
import gzip
import socket

app = Flask(__name__)

@app.route('/services/collector', methods=['POST'])
def webhook():
    token = request.headers.get('Authorization')
    if token == 'Splunk <token>':
        if request.method == 'POST':


            headers = {'Authorization': 'Splunk <token>'}

            encoded = gzip.decompress(request.data)
            payload = json.loads((encoded).decode('utf-8'))
            data = json.dumps(payload, indent=2)
            print(encoded)
            print("")
            print(data)
            # print(encoded)
            # for val in payload:
            #       print("%s: %s" % (val, payload[val]))
            #       print("")

            requests.post('http://<splunk hec>:8088/services/collector', headers=headers, data=json.dumps(payload))

            requests.post('http://http-us.devo.io/event/<domain>/token!<token>/-/my.app?test', data=json.dumps(payload))

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('<location>', 8888))
                s.sendall(encoded)
                # payload = s.recv(1024)


            # requests.post('http://<some location>:8888', data=json.dumps(payload))

            return 'success', 200

        else:
            abort(400)

    else:
        abort(400)

if __name__ == '__main__':
        app.run()

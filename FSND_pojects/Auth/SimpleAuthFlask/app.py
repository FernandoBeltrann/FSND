from flask import Flask, request

app = Flask(__name__)

@app.route('/headers')
def headers():
  #Unpack the request header
  auth_header = request.headers['Authorization']
  header_parts = auth_header.split(' ')
  print(header_parts[1])
  return 'not implemented'
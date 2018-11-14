from flask import Flask, url_for, render_template, request, redirect, session, jsonify, make_response, send_from_directory
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
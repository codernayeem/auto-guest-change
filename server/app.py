# This file contains the code for the Flask server that show the passkey

from flask import Flask, jsonify, request, render_template
import os
app = Flask(__name__)

TITLE = "MY WIFI"
password_file = "pass.txt"
server_password = "sample_password"

def get_saved_key():
    if not os.path.exists(password_file):
        return ''
    fl = open(password_file)
    key = fl.read()
    fl.close()
    return key.strip()

def save_key(key):
    fl = open(password_file, "w")
    fl.write(key)
    fl.close()

@app.route('/set_new_key', methods=['POST'])
def set_key():
    data = request.form
    mypass = data.get('password')

    if mypass and mypass == server_password:
        key = data.get('new_key')
        if not key:
            return jsonify({"success": False, "message": "Key is required"}), 400
        save_key(key)
        print("Key set successfully:", key)
        return jsonify({"success": True, "message": "Key set successfully"}), 200
    else:
        return jsonify({"success": False, "message": "Some Error Occured"}), 400

@app.route('/get_key', methods=['GET'])
def get_key():
    key = get_saved_key()
    return jsonify({"key": key})

@app.route('/', methods=['GET'])
def show_data():
    key = get_saved_key()
    return render_template('home.html', passkey=(key if key else ''), title=TITLE)


# The server is running on port 5000. You can access the server by visiting http://localhost:5000 in your browser.
if __name__ == '__main__':
    app.run(debug=True)
    

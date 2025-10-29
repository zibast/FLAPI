from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
USER_FILE = 'users.json'

# بارگذاری کاربران
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as f:
        return json.load(f)

# ذخیره کاربران
def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=2)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if username in users:
        return jsonify({'message': 'کاربر قبلاً ثبت شده است'}), 400

    users[username] = {'password': password}
    save_users(users)
    return jsonify({'message': 'ثبت‌نام موفقیت‌آمیز بود'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if username not in users or users[username]['password'] != password:
        return jsonify({'message': 'نام کاربری یا رمز عبور اشتباه است'}), 401

    return jsonify({'message': f'خوش آمدی {username}'}), 200

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    users = load_users()
    if username not in users:
        return jsonify({'message': 'کاربر یافت نشد'}), 404

    return jsonify({'username': username}), 200

if __name__ == '__main__':
    app.run(debug=True)
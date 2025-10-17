from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "The Flask is working!"

@app.route('/test')
def test():
    return "Test page is working!"

if __name__ == '__main__':
    print("🚀 Starting SIMPLE test app...")
    print("📡 Server should run at: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
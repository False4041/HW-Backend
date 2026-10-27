from flask import Flask, jsonify
 
app = Flask(__name__)
 
 
@app.route('/')
def home():
    return 'Hello, server works!'
 
 
@app.route('/api/status')
def status():
    return jsonify({"status": "ok", "framework": "Flask"})
 
 
if __name__ == '__main__':
    app.run(port=3001, debug=True)

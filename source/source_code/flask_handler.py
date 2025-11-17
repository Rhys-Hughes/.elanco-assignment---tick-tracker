from flask import Flask, request, jsonify
import tick_tracker

app = Flask(__name__)

@app.route("/hello")
def hello():
    return jsonify({"message" : "hello there!"})

if __name__ == "__main__":  
    app.run(debug = True)
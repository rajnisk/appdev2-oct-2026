from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/about", methods=["GET"])
def about():
    return "<p>This is the about page.</p>"

@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    name = data.get("name")
    print(f"Received name: {name}")
    return f"<p>this is post method, {name}</p>"

if __name__ == "__main__":
    app.run()
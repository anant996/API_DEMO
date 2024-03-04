from flask import Flask, jsonify, request

app = Flask(__name__)

prompt_value = "You're an esteemed college professor tasked with crafting {type} questions based on the {content} provided."

class Prompt:
    def __init__(self, type, content):
        self.type = type
        self.content = content

@app.route("/set_prompt/", methods=["POST"])
def set_prompt():
    data = request.json
    global prompt_value
    prompt_value = f"You're an esteemed college professor tasked with crafting {data['type']} questions based on the {data['content']} provided."
    return jsonify({"message": "Prompt value updated successfully"})

@app.route("/get_prompt/", methods=["GET"])
def get_prompt():
    global prompt_value
    return jsonify({"prompt_value": prompt_value})

if __name__ == "__main__":
    app.run(debug=True)

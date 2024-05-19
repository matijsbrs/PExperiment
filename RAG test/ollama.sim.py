# pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir
from flask import Flask, request, jsonify
import time
import json
import base64
from hashlib import sha256

app = Flask(__name__)

# In-memory storage for models and blobs
models = {
  "models": [
    {
      "name": "jake",
      "model": "jake",
      "modified_at": "2024-04-30T14:50:53.995477181Z",
      "size": 5011853225,
      "digest": "a72c7f4d0a15522df81486d13ce432c79e191bda2558d024fbad4362c4f7cbf9",
      "details": {
        "parent_model": "",
        "format": "gguf",
        "family": "jake",
        "families": [
          "gemma"
        ],
        "parameter_size": "9B",
        "quantization_level": "Q4_0"
      }
    }
  ]
}
blobs = {}

# Helper function to generate SHA256 digest
def generate_digest(data):
    return sha256(data).hexdigest()

@app.route('/api/version', methods=['GET'])
def get_version():
    return jsonify({"version":"0.1.30"})

@app.route('/ollama/api/chat', methods=['POST'])
def generate_chat():
    data = request.json
    model = data.get('model')
    messages = data.get('messages', ['joehoe'])
    stream = data.get('stream', True)
    response = {"model": model, "created_at": time.time(), "message": {"role": "assistant", "content": "Hello! How are you today?"}, "done": True}
    if stream:
        return jsonify({"model": model, "created_at": time.time(), "message": {"role": "assistant", "content": "The"}, "done": False})
    return jsonify(response)

@app.route('/ollama/v1/chat/completions', methods=['POST'])
def generate_chat_completion():
    data = request.json
    model = data.get('model')
    messages = data.get('messages', ['joehoe'])
    stream = data.get('stream', True)
    response = {"model": model, "created_at": time.time(), "message": {"role": "assistant", "content": "Hello! How are you today?"}, "done": True}
    if stream:
        return jsonify({"model": model, "created_at": time.time(), "message": {"role": "assistant", "content": "The"}, "done": False})
    return jsonify(response)


@app.route('/api/generate', methods=['POST'])
def generate_completion():
    data = request.json
    model = data.get('model')
    prompt = data.get('prompt', '')
    stream = data.get('stream', True)
    response = {"model": model, "created_at": time.time(), "response": "", "done": True}
    if stream:
        return jsonify({"model": model, "created_at": time.time(), "response": "The", "done": False})
    response["response"] = f"The response for prompt '{prompt}'"
    return jsonify(response)

@app.route('/api/chat', methods=['POST'])
def generate_chat_completion2():
    data = request.json
    model = data.get('model')
    messages = data.get('messages', [])
    stream = data.get('stream', True)
    response = {"model": model, "created_at": time.time(), "message": {"role": "assistant", "content": "Hello! How are you today?"}, "done": True}
    if stream:
        return jsonify({"model": model, "created_at": time.time(), "message": {"role": "assistant", "content": "The"}, "done": False})
    return jsonify(response)

@app.route('/api/create', methods=['POST'])
def create_model():
    data = request.json
    name = data.get('name')
    modelfile = data.get('modelfile', '')
    models[name] = {"modelfile": modelfile, "created_at": time.time()}
    return jsonify({"status": "success"})

@app.route('/api/tags', methods=['GET'])
def list_local_models():
    
    # response = {"models": [{"name": name, "modified_at": model["created_at"]} for name, model in models.items()]}
    response = {"models": models["models"]}

    return jsonify(response)

@app.route('/api/show', methods=['POST'])
def show_model_information():
    data = request.json
    name = data.get('name')
    if name in models:
        return jsonify(models[name])
    return jsonify({"error": "Model not found"}), 404

@app.route('/api/copy', methods=['POST'])
def copy_model():
    data = request.json
    source = data.get('source')
    destination = data.get('destination')
    if source in models:
        models[destination] = models[source].copy()
        return jsonify({"status": "success"})
    return jsonify({"error": "Source model not found"}), 404

@app.route('/api/delete', methods=['DELETE'])
def delete_model():
    data = request.json
    name = data.get('name')
    if name in models:
        del models[name]
        return jsonify({"status": "success"})
    return jsonify({"error": "Model not found"}), 404

@app.route('/api/pull', methods=['POST'])
def pull_model():
    data = request.json
    name = data.get('name')
    stream = data.get('stream', True)
    if name not in models:
        models[name] = {"created_at": time.time()}
    if stream:
        return jsonify({"status": "pulling manifest"})
    return jsonify({"status": "success"})

@app.route('/api/push', methods=['POST'])
def push_model():
    data = request.json
    name = data.get('name')
    stream = data.get('stream', True)
    if name in models:
        if stream:
            return jsonify({"status": "starting upload"})
        return jsonify({"status": "success"})
    return jsonify({"error": "Model not found"}), 404

@app.route('/api/embeddings', methods=['POST'])
def generate_embeddings():
    data = request.json
    model = data.get('model')
    prompt = data.get('prompt')
    embeddings = [0.5670403838157654, 0.009260174818336964, 0.23178744316101074]
    return jsonify({"embedding": embeddings})

@app.route('/api/blobs/<digest>', methods=['HEAD'])
def check_blob_exists(digest):
    if digest in blobs:
        return '', 200
    return '', 404

@app.route('/api/blobs/<digest>', methods=['POST'])
def create_blob(digest):
    data = request.data
    if generate_digest(data) == digest:
        blobs[digest] = data
        return '', 201
    return '', 400

@app.route('/api/generate', methods=['POST'])
def load_model():
    data = request.json
    model = data.get('model')
    if model in models:
        return jsonify({"model": model, "created_at": time.time(), "response": "", "done": True})
    return jsonify({"error": "Model not found"}), 404

# @app.before_request
# def log_request_info():
#   print('Headers: %s', request.headers)
#   print('Body: %s', request.get_data())

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")


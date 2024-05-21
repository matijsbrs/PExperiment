# pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir
from flask import Flask, request, jsonify, Response
import time
import json
import base64
from hashlib import sha256
import datetime

app = Flask(__name__)

# In-memory storage for models and blobs
models = {"models":[{"name":"gemma:7b","model":"gemma:7b","modified_at":"2024-04-30T14:50:53.995477181Z","size":5011853225,"digest":"a72c7f4d0a15522df81486d13ce432c79e191bda2558d024fbad4362c4f7cbf8","details":{"parent_model":"","format":"gguf","family":"gemma","families":["gemma"],"parameter_size":"9B","quantization_level":"Q4_0"}},{"name":"gemma:latest","model":"gemma:latest","modified_at":"2024-05-13T12:26:36.900273527Z","size":5011853225,"digest":"a72c7f4d0a15522df81486d13ce432c79e191bda2558d024fbad4362c4f7cbf8","details":{"parent_model":"","format":"gguf","family":"gemma","families":["gemma"],"parameter_size":"9B","quantization_level":"Q4_0"}},{"name":"llama2:latest","model":"llama2:latest","modified_at":"2024-03-28T13:39:15.78752028Z","size":3826793677,"digest":"78e26419b4469263f75331927a00a0284ef6544c1975b826b15abdaef17bb962","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama"],"parameter_size":"7B","quantization_level":"Q4_0"}},{"name":"llama3:latest","model":"llama3:latest","modified_at":"2024-04-18T20:19:35.404746906Z","size":4661224596,"digest":"71a106a910165bc11d43aa128d99e32576a91cbd3e272016abd049f7a09b3235","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama"],"parameter_size":"8B","quantization_level":"Q4_0"}},{"name":"llava:latest","model":"llava:latest","modified_at":"2024-03-29T20:41:21.283636028Z","size":4733363377,"digest":"8dd30f6b0cb19f555f2c7a7ebda861449ea2cc76bf1f44e262931f45fc81d081","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama","clip"],"parameter_size":"7B","quantization_level":"Q4_0"}},{"name":"llava-phi3:latest","model":"llava-phi3:latest","modified_at":"2024-05-13T06:13:33.568376684Z","size":2926568956,"digest":"c7edd7b8759394f9995a9394b97a29aeff7ee9c921054a210347326287d300f2","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama","clip"],"parameter_size":"4B","quantization_level":"Q4_K_M"}},{"name":"mistral:7b","model":"mistral:7b","modified_at":"2024-03-29T20:40:51.616201844Z","size":4109865159,"digest":"61e88e884507ba5e06c49b40e6226884b2a16e872382c2b44a42f2d119d804a5","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama"],"parameter_size":"7B","quantization_level":"Q4_0"}},{"name":"nomic-embed-text:latest","model":"nomic-embed-text:latest","modified_at":"2024-05-14T07:17:38.257062016Z","size":274302450,"digest":"0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f","details":{"parent_model":"","format":"gguf","family":"nomic-bert","families":["nomic-bert"],"parameter_size":"137M","quantization_level":"F16"}},{"name":"phi:latest","model":"phi:latest","modified_at":"2024-03-29T20:40:57.156096182Z","size":1602463378,"digest":"e2fd6321a5fe6bb3ac8a4e6f1cf04477fd2dea2924cf53237a995387e152ee9c","details":{"parent_model":"","format":"gguf","family":"phi2","families":["phi2"],"parameter_size":"3B","quantization_level":"Q4_0"}},{"name":"phi3:latest","model":"phi3:latest","modified_at":"2024-05-13T06:09:55.508357332Z","size":2318920898,"digest":"a2c89ceaed85371d0b8a51b5cc70ff054acc37465ea25e72e1612fe28bce7ad9","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama"],"parameter_size":"4B","quantization_level":"Q4_K_M"}},{"name":"tommy/geitje:7b_ultra_q3_k_s","model":"tommy/geitje:7b_ultra_q3_k_s","modified_at":"2024-04-17T19:36:24.216110896Z","size":3164568007,"digest":"d34ce544954b5a86b1180ae5f2da6a6243b37926aae3b152eeee86079eec2d13","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama"],"parameter_size":"7B","quantization_level":"Q3_K_S"}},{"name":"tommy/geitje:7b_ultra_q8_0","model":"tommy/geitje:7b_ultra_q8_0","modified_at":"2024-04-17T19:33:06.207844974Z","size":7695858117,"digest":"9e0832dbfc6d248af08695596f2bbb53f1ff4c3b217475d570fd38b5c94b8a67","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama"],"parameter_size":"7B","quantization_level":"Q8_0"}}]}
blobs = {}

@app.before_request
def log_request_info():
    print('Headers: %s', request.headers)
    print('Body: %s', request.get_data())


# Helper function to generate SHA256 digest
def generate_digest(data):
    return sha256(data).hexdigest()

@app.route('/api/version', methods=['GET'])
def get_version():
    # Create the JSON content
    content = jsonify({"version":"0.1.30"})
    
    # Define the desired headers
    response_headers = {
        'Content-Type': 'application/json; charset=utf-8', 
        'Date': datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'), 
        'Content-Length': str(len(content.data))
    }
    
    # Create a response object
    response = Response(response=content.data, status=200)
    
    # Set the desired headers
    response.headers.clear()  # Clear any default headers Flask might add
    for key, value in response_headers.items():
        response.headers[key] = value
    
    return response
# @app.route('/v1/chat/completions', methods=['POST'])

@app.route('/api/chat', methods=['POST'])
def chat_response():
    data = request.json
    model = data.get('model')
    messages = data.get('messages', [])
    stream = data.get('stream', True)
    response = {"model": model, "created_at": time.time(), "message": {"role": "assistant", "content": "Hello! How are you today?"}, "done": True}
    if stream:
        return jsonify({"model": model, "created_at": time.time(), "message": {"role": "assistant", "content": "The"}, "done": True}), 200, {'Content-Type': 'application/x-ndjson', 'Date': 'Tue, 21 May 2024 11:57:50 GMT', 'Transfer-Encoding': 'chunked'}
    return jsonify(response), 200, {'Content-Type': 'application/x-ndjson', 'Date': 'Tue, 21 May 2024 11:57:50 GMT', 'Transfer-Encoding': 'chunked'}

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

@app.errorhandler(404)
def bad_request(error):
    app.logger.error('Bad Request: %s', error)
    return 'Bad Request!', 400

# @app.before_request
# def log_request_info():
#   print('Headers: %s', request.headers)
#   print('Body: %s', request.get_data())

if __name__ == '__main__':
    app.run(debug=True, port=5001, host="0.0.0.0")


from flask import Flask, request
import requests
import random

app = Flask(__name__)

# List of backend servers
backend_servers = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
]

@app.route("/", defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def load_balancer(path):
    # Randomly choose a backend server
    backend_server = random.choice(backend_servers)

    # Build the target URL
    target_url = backend_server + '/' + path

    # Proxy the request to the chosen backend server
    response = requests.request(
        method=request.method,
        url=target_url,
        headers=request.headers,
        data=request.get_data(),
        cookies=request.cookies,
        stream=True,
    )

    # Return the response from the backend server to the client
    headers = [(name, value) for name, value in response.raw.headers.items()]
    return response.content, response.status_code, headers

if __name__ == '__main__':
    # Run the load balancer
    app.run(host='0.0.0.0', port=5000)

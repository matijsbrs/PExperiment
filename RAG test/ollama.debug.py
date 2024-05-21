import http.server
import socketserver
import requests
from urllib.parse import urlparse, urlunparse
import logging

# Install required packages
# pip install requests

# Setup logging
logging.basicConfig(filename='proxy.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# The endpoint you want to forward the requests to
# FORWARD_TO = 'http://192.168.2.61:11434'
FORWARD_TO = 'http://192.168.2.61:5001'

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request()

    def do_POST(self):
        self.proxy_request()

    def proxy_request(self):
        try:
            url = urlparse(self.path)
            target_url = urlunparse((url.scheme, FORWARD_TO, url.path, url.params, url.query, url.fragment)).lstrip('//')

            headers = dict(self.headers)
            if 'Host' in headers:
                del headers['Host']  # The Host header will be set by `requests`

            # Log the incoming request
            logging.info(f"Received {self.command} request for {self.path}")
            logging.debug(f"Request Headers: {headers}")
            if self.command == 'POST':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length) if content_length > 0 else None
                logging.debug(f"Request Body: {post_data.decode('utf-8')}")
            else:
                post_data = None

            if self.command == 'GET':
                response = requests.get(target_url, headers=headers)
            elif self.command == 'POST':
                response = requests.post(target_url, headers=headers, data=post_data)
                print(response.content)
            else:
                self.send_error(405, "Method Not Allowed")
                return

            # Log the response from the forwarded request
            logging.info(f"Forwarded request to {target_url}")
            logging.info(f"Response Status Code: {response.status_code}")
            logging.debug(f"Response Headers: {response.headers}")
            logging.debug(f"Response Body: {response.text}")

            self.send_response(response.status_code)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()
            
            # Handle chunked transfer encoding properly
            if 'Transfer-Encoding' in response.headers and response.headers['Transfer-Encoding'] == 'chunked':
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        self.wfile.write(hex(len(chunk))[2:].encode() + b'\r\n' + chunk + b'\r\n')
                self.wfile.write(b'0\r\n\r\n')
            else:
                self.wfile.write(response.content)

        except Exception as e:
            logging.error(f"Error during proxying: {str(e)}")
            self.send_error(500, f"Internal Server Error: {e}")

if __name__ == '__main__':
    PORT = 5000
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        logging.info(f"Serving at port {PORT}")
        print(f"Serving at port {PORT}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            httpd.shutdown()

        httpd.server_close()
        httpd.shutdown()
        
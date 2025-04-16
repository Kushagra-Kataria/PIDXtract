import os
import mimetypes
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # If requesting the root path, serve index.html
        if path == '/' or path == '':
            path = '/index.html'

        # If requesting the contact page, serve contact.html
        if path == '/contact':
            path = '/contact.html'

        try:
            # Construct the file path
            if path.startswith('/static/'):
                file_path = os.path.join(os.getcwd(), path[1:])
            else:
                file_path = os.path.join(os.getcwd(), 'templates', path[1:])

            # Check if the file exists
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Get the file content and content type
                with open(file_path, 'rb') as file:
                    content = file.read()

                # Set content type based on file extension
                _, ext = os.path.splitext(file_path)
                content_type = mimetypes.guess_type(file_path)[0]
                if content_type is None:
                    if ext == '.css':
                        content_type = 'text/css'
                    elif ext == '.js':
                        content_type = 'application/javascript'
                    elif ext == '.html':
                        content_type = 'text/html'
                    else:
                        content_type = 'application/octet-stream'

                # Send response
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                # File not found
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        except Exception as e:
            # Server error
            self.send_response(500)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(f'500 Internal Server Error: {str(e)}'.encode())

    def do_POST(self):
        # Handle contact form submission (simplified)
        if self.path == '/contact':
            # Redirect to home page with a query parameter for a success message
            self.send_response(303)  # 303 See Other
            self.send_header('Location', '/?message=Thank+you+for+your+message!+We+will+get+back+to+you+soon.')
            self.end_headers()
        else:
            # Not found
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Starting server on http://localhost:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Pagina HTML con form di login in chiaro
        html = """
        <html>
        <head><title>Lab HTTP Insecure</title></head>
        <body>
            <h1>Login (HTTP non sicuro)</h1>
            <form method="POST" action="/">
                <label>Username: <input type="text" name="username"></label><br>
                <label>Password: <input type="password" name="password"></label><br>
                <input type="submit" value="Login">
            </form>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        # Legge i dati inviati dal form
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = urllib.parse.parse_qs(post_data.decode("utf-8"))

        username = params.get("username", [""])[0]
        password = params.get("password", [""])[0]

        # Mostra i dati ricevuti (in chiaro!)
        response = f"""
        <html>
        <body>
            <h2>Dati ricevuti</h2>
            <p>Username: {username}</p>
            <p>Password: {password}</p>
            <p><b>Nota:</b> Questi dati sono stati inviati in chiaro su HTTP!</p>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8080)  # Ascolta su tutte le interfacce, porta 8080
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Server HTTP insicuro in ascolto su http://0.0.0.0:8080 ...")
    httpd.serve_forever()

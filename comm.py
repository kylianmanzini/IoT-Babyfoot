#!/usr/bin/python3
import json
import logging
import re
from http.server import BaseHTTPRequestHandler, HTTPServer


scoreboard = {
    "score_equipe1" : 1,
    "score_equipe2" : 1
}



class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if re.search('/api/post/score', self.path):
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length).decode('utf8')

            self.send_response(200)
        else:
            self.send_response(403)
        self.end_headers()

    def do_GET(self):
        if re.search('/api/get/score', self.path):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                # Return json, even though it came in as POST URL params
                data = json.dumps(scoreboard).encode('utf-8')
                self.wfile.write(data)
        else:
            self.send_response(403)
        self.end_headers()

        
if __name__ == '__main__':
    print("caca\n")
    server = HTTPServer(('localhost', 8000), HTTPRequestHandler)
    logging.info('Starting httpd...\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping httpd...\n')
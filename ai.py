import os
import json
import anthropic
from http.server import BaseHTTPRequestHandler

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))

        try:
            msg = client.messages.create(
                model=body.get('model', 'claude-sonnet-4-20250514'),
                max_tokens=body.get('max_tokens', 1000),
                system=body.get('system', ''),
                messages=body.get('messages', [])
            )
            result = {'content': [{'type': 'text', 'text': msg.content[0].text}]}
            self.send_response(200)
        except Exception as e:
            result = {'error': str(e)}
            self.send_response(500)

        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

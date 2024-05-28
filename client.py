import requests

id = 'test'
data = {'key': 'value'}
r = requests.get('http://localhost:8000/api/post/{}'.format(id), json=data)
print(r)
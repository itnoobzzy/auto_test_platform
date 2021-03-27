import requests

data = {
    'page': 1,
    'pageSize': 10
}

r = requests.post('http://127.0.0.1:8000/user/query_user_menu_info/', data=data)
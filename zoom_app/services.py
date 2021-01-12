import requests
from config import client_id, zoom_auth_callback_url
from zoom_app.models import *
from django.shortcuts import redirect


def update_token():
    url = f'https://zoom.us/oauth/authorize?response_type=code&redirect_uri={zoom_auth_callback_url}&client_id={client_id}'
    print(url)
    res = requests.get(url)
    redirect(url)
    return res
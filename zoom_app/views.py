from django.shortcuts import render
from zoom_app.models import *
import requests
from django.http import JsonResponse
from config import client_id,zoom_auth_callback_url
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

def code_callback(request):
    _params = request.GET
    code = _params.get('code')
    auth = ZoomAuth.objects.first()
    if not auth:
        auth = ZoomAuth()
    auth.code = code
    auth.save()
    
    auth_code = "TjEzTkt3eldTeU9IREZvWVZrRnh6ZzplbXpDQ1lKOThpMW9xenJJTWtqTXdraWptUWd5VUs5Rg==" #b64 client_id:client_secret
    url = f"https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri={zoom_auth_callback_url}"
    headers = {
      'Authorization': f'Basic {auth_code}',
    }
    
    try:
        res = requests.request("POST", url, headers=headers)
        if res.status_code == 200:
            token = res.json().get('access_token')
        else:
            return JsonResponse({'success':False})

        auth.auth_token = token
        auth.save()

        return render(request,'menu.html')
    except Exception as e:
        print(e)
        return JsonResponse({'success':False})
    
@csrf_exempt
def channel(request):
    if request.method == 'POST':
        user = json.loads(request.body).get('user')
        url = f'https://api.zoom.us/v2/chat/users/{user}/channels'
        name = json.loads(request.body).get('name')
        type = 1
        members = json.loads(request.body).get('members')
        
        payload = json.dumps({
            "name": name,
            "type": type,
            "members": members
        })
        
        auth_token = ZoomAuth.objects.first().auth_token
        
        headers = {
            "authorization": f"Bearer {auth_token}",
            'content-type': 'application/json'
        }
        
        try:
            res = requests.request("POST", url, headers=headers, data=payload)
            if res.status_code == 200:
                return JsonResponse({'success':True, 'res':res.json()})
            else:
                return JsonResponse({'success':False, 'res':res.json()})
        except:
            return JsonResponse({'success':False})
        
    elif request.method == 'GET':
        user = json.loads(request.body).get('user')
        url = f'https://api.zoom.us/v2/chat/users/{user}/channels'
        auth_token = ZoomAuth.objects.first().auth_token
        
        headers = {
            "authorization": f"Bearer {auth_token}",
            'content-type': 'application/json'
        }
        try:
            res = requests.request("GET", url, headers=headers)
            if res.status_code == 200:
                return JsonResponse({'success':True, 'res':res.json()})
            else:
                return JsonResponse({'success':False, 'res':res.json()})
        except:
            return JsonResponse({'success':False})

@csrf_exempt     
def meeting(request):
    if request.method == 'POST':
        user = json.loads(request.body).get('user')
        url = f'https://api.zoom.us/v2/users/{user}/meetings'
        
        meeting_topic = json.loads(request.body).get('topic')
        meeting_start_time = json.loads(request.body).get('start_time')
        meeting_duration = json.loads(request.body).get('duration')
        meeting_timezone = json.loads(request.body).get('timezone')
        meeting_password = json.loads(request.body).get('password')
        meeting_agenda = json.loads(request.body).get('agenda')
        
        meeting_settings = {'host_video': False,
        'participant_video': False,
        'cn_meeting': False,
        'in_meeting': True,
        'join_before_host': False,
        'mute_upon_entry': True,
        'watermark': False,
        'use_pmi': False,
        'approval_type': 0,
        'registration_type': 1,
        'audio': 'both',
        'auto_recording': 'none',
        'enforce_login': False,
        'registrants_email_notification': True}
        
        body = {
            'topic' : meeting_topic,
            'start_time' : meeting_start_time,
            'duration' : meeting_duration,
            'timezone' : meeting_timezone,
            'password' : meeting_password,
            'agenda' : meeting_agenda,
            'settings' : meeting_settings
        }
        
        auth_token = ZoomAuth.objects.first().auth_token
        
        headers = {
            "authorization": f"Bearer {auth_token}",
            'content-type': 'application/json'
        }
        
        try:
            res = requests.request("POST", url, headers=headers, data=body)
            if res.status_code == 200:
                return JsonResponse({'success':True, 'res':res.json()})
            else:
                return JsonResponse({'success':False, 'res':res.json()})
        except Exception as e:
            print(e)
            return JsonResponse({'success':False})
        
@csrf_exempt
def chat(request):
    if request.method == 'GET':
        _params = request.GET
        user = _params.get('user')
        url = f'https://api.zoom.us/v2/chat/users/{user}/messages'
        
        params = {}
        
        to_contact = _params.get('to_contact',None)
        to_channel = _params.get('to_channel',None)
        pagesize = _params.get('pagesize',50)
        next_page_token = _params.get('next_page_token',None)
        
        if to_contact :
            params['to_contact'] = to_contact
        
        elif to_channel:
            params['to_channel'] = to_channel
            
        params['page_size'] = pagesize
        
        if next_page_token:
            params['next_page_token'] = next_page_token
            
        auth_token = ZoomAuth.objects.first().auth_token
        
        headers = {
            "authorization": f"Bearer {auth_token}",
            'content-type': 'application/json'
        }
        
        try:
            res = requests.request("GET", url, headers=headers, params=params)
            if res.status_code == 200:
                msgs = res.json().get('messages')
                return JsonResponse({'success':True, 'res':msgs})
            else:
                return JsonResponse({'success':False, 'res':res.json()})
        except:
            return JsonResponse({'success':False})

    if request.method == 'POST':
        user = json.loads(request.body).get('user')
        url = f'https://api.zoom.us/v2/chat/users/{user}/messages'
        
        auth_token = ZoomAuth.objects.first().auth_token
        
        headers = {
            "authorization": f"Bearer {auth_token}",
            'content-type': 'application/json'
        }

        to_contact = json.loads(request.body).get('to_contact',None)
        to_channel = json.loads(request.body).get('to_channel',None)        
        msg = json.loads(request.body).get('message',None)
        at_present = json.loads(request.body).get('at_present',False)
        at_pos = json.loads(request.body).get('at_pos',None)
        
        body = {}
        body['message'] = msg
        
        if to_contact:
            body['to_contact'] = to_contact
        
        elif to_channel:
            body['to_channel'] = to_channel
        
        if at_present:
            ats = []
            for at in at_pos:
                if at["content"] != "@all":
                    at_items = {
                    "start_position" : at["start_position"],
                    "end_position" : at["end_position"],
                    "at_type": 1,
                    "at_content" : at["content"]
                    }
                else:
                    at_items = {
                    "start_position" : at["start_position"],
                    "end_position" : at["end_position"],
                    "at_type": 2,
                    "at_content" : at["content"]
                    }
                ats.append(at_items)
        
            body['at_items'] = ats
        
        try:
            print(body)
            res = requests.request("POST", url, headers=headers, data=json.dumps(body))
            print(res.text)
            if res.status_code == 200:
                return JsonResponse({'success':True, 'res':res.json()})
            else:
                return JsonResponse({'success':False, 'res':res.json()})
        except Exception as e:
            print(e)
            return JsonResponse({'success':False})    
        

def contacts(request):
    if request.method == 'GET':
        _params = request.GET
        userId = _params.get('user','me')
        url = f'https://api.zoom.us/v2/chat/users/{userId}/channels'
        pagesize = _params.get('pagesize',100)
        next_page_token = _params.get('next_page_token',None)
        
        params = {}
        
        auth_token = ZoomAuth.objects.first().auth_token
        
        headers = {
            "authorization": f"Bearer {auth_token}",
            'content-type': 'application/json'
        }
        
        params['page_size'] = pagesize
        
        if next_page_token:
            params['next_page_token'] = next_page_token
            
        try:
            res = requests.request("GET", url, headers=headers, params=params)
            if res.status_code == 200:
                return JsonResponse({'success':True, 'res':res.json().get('channels')})
            else:
                return JsonResponse({'success':False, 'res':res.json()})
        except:
            return JsonResponse({'success':False})
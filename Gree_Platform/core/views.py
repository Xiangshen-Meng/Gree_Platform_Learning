from django.shortcuts import render_to_response
from django.http import HttpResponse
from core.support.oauth import oauth
import httplib,urllib
import requests

CONSUMER_KEY = "015ed0cf0e7f"
CONSUMER_SECRET = "44f85c510c34e54691db4746cb881d90"

API_URL = "http://os-sb.gree.jp/api/rest"

def auth_with_request(request, api_url, parameters=None):
  oauth_token = request.GET.get('oauth_token', request.session.get('oauth_token'))
  oauth_token_secret = request.GET.get('oauth_token_secret', request.session.get('oauth_token_secret'))
  oauth_signature = request.GET.get('oauth_signature', request.session.get('oauth_signature'))
  opensocial_viewer_id = request.GET.get('opensocial_viewer_id', request.session.get('opensocial_viewer_id'))
  xoauth_requestor_id = opensocial_viewer_id

  request.session['oauth_token'] = oauth_token
  request.session['oauth_token_secret'] = oauth_token_secret
  request.session['oauth_signature'] = oauth_signature
  request.session['opensocial_viewer_id'] = opensocial_viewer_id


  http_method = 'GET'
  request_data = {'xoauth_requestor_id':xoauth_requestor_id}
  if parameters:
    request_data.update(parameters)

  oauth_consumer = oauth.OAuthConsumer(key = CONSUMER_KEY, secret = CONSUMER_SECRET)
  signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
  access_token = oauth.OAuthToken(oauth_token, oauth_token_secret)
  oauth_request	= oauth.OAuthRequest.from_consumer_and_token(oauth_consumer,
                  token=access_token, http_method=http_method, http_url=api_url, parameters=request_data)
  oauth_request.sign_request(signature_method, oauth_consumer, access_token)

  authorization_header = oauth_request.to_header().get('Authorization')
  headers = {'Content-Type':"application/json", 'Authorization':authorization_header}

  ret_request = requests.get(api_url, params={'xoauth_requestor_id':xoauth_requestor_id}, headers=headers)

  return ret_request

def appstart(request):

  api_url = API_URL+'/people/@me/@self'
  api_request = auth_with_request(request, api_url)
  # if is json, else error
  if 'entry' in api_request.text:
    user_info = api_request.json().get('entry')
  else:
    user_info = {}

  return render_to_response('app_welcome.html', {'user_info':user_info})

def callback_app_start(request):
  return render_to_response('app_start_callback.html', locals())

def gadget(request):
  return render_to_response('gadget.xml')

def friends_info(request):
	
  api_url = API_URL+'/people/@me/@all'
  friends_list = []
  api_request = auth_with_request(request, api_url)
  # if is json, else error
  if 'entry' in api_request.text:
    ret_json = api_request.json()
    total_num = int(ret_json.get('totalResults'))
    cur_count = int(ret_json.get('itemsPerPage'))
    friends_list.extend(ret_json.get('entry'))

    while cur_count < total_num:
      api_request = auth_with_request(request, api_url,parameters={'startIndex':cur_count})
      # if is json, else error
      ret_json = api_request.json()
      cur_count = int(ret_json.get('itemsPerPage'))+cur_count
      friends_list.extend(ret_json.get('entry'))

  return render_to_response('app_friends_info.html', {'friends_list':friends_list})








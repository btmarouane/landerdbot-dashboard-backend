import configparser
import subprocess

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

USERS_PATH = '/opt/landerdbot/users.txt'
CONFIG_PATH = '/opt/landerdbot/twitterbot.properties'

@api_view(['GET'])
def get_server_status(request):
    try:
        command = ['twitterbot', 'status']
        result = subprocess.run(command, capture_output=True, text=True)
        status = result.stdout.strip()
        is_active = (status == 'active')

        return Response(status=200, data=is_active)
    except Exception as e:
        return Response(str(e), status=500)

@api_view(['GET'])
def get_users(request):
    try:
        with open(USERS_PATH, 'r') as file:
            users = file.read()
            return Response(users)
    except FileNotFoundError:
        return HttpResponse(status=500)

@api_view(['GET'])
def get_keywords(request):
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        properties = config['DEFAULT']['KEYWORD']
        keywords = [keyword.strip() for keyword in properties.split(',')]
        keywords = '\n'.join(keywords)
        return Response(status=200, data=keywords)
    except FileNotFoundError:
        return HttpResponse(status=500)

@api_view(['POST'])
def update_users(request):
    try:
        users = request.data.get('users')
        users = [user.strip() for user in users.split('\n') if len(user) > 0]
        users = '\n'.join(users)
        users += '\n'
        with open(USERS_PATH, 'w') as file:
            file.write(users)

        return Response(status=200)
    except Exception as e:
        return Response(str(e), status=500)

@api_view(['POST'])
def update_keywords(request):
    try:
        keywords = request.data.get('keywords')
        keywords = [keyword.strip() for keyword in keywords.split('\n') if len(keyword) > 0]
        keywords = ', '.join(keywords)
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(CONFIG_PATH)
        config.set('DEFAULT', 'KEYWORD', keywords)
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
        return Response(status=200)
    except Exception as e:
        return Response(str(e), status=500)

@api_view(['POST'])
def update_server_status(request):
    try:
        state = request.data.get('state')
        if state is True:
            command = ['twitterbot', 'start']
        else:
            command = ['twitterbot', 'stop']
        subprocess.run(command, check=True)
        return Response(status=200)
    except Exception as e:
        return Response(str(e), status=500)

# system modules
import json
from requests import get

# django module
from django import db
from django.http import HttpResponse, JsonResponse

# 3rd party library modules
from pydialogflow_fulfillment import DialogflowResponse
from pydialogflow_fulfillment.response import SimpleResponse, OutputContexts

class Server(object):
    def __init__(self, request):
        self.req = json.loads(request.body)
        self.text1 = None

    def rcvIntent(self):
        return self.req.get('queryResult').get('intent').get('displayName')

    def rcvParam(self, value):
        return self.req.get('queryResult').get('parameters').get(value)

    def sendMsg(self):
        dialogflow_response = DialogflowResponse(self.text1)
        reply = dialogflow_response.get_final_response()

        db.connections.close_all()
        # return generated response
        return HttpResponse(reply, content_type='application/json; charset=utf-8')
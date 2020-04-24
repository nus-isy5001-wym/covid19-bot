# system modules
import sys
import json
from requests import get

# django module
from django import db
from django.http import HttpResponse, JsonResponse

# 3rd party library modules
from chatbot_app.modules.df_response_lib import *

class Server(object):
    def __init__(self, request):
        self.req = json.loads(request.body)
        self.main_text = None
        self.sub_text = None
        self.img_url = None

    # get intent from dialogflow
    def rcvIntent(self):
        return self.req.get('queryResult').get('intent').get('displayName')

    # get parameter from dialogflow
    def rcvParam(self, key):
        return self.req.get('queryResult').get('parameters').get(key)

    # get session from dialogflow
    def rcvSession(self):
        return self.req.get('session').split('/')[-1]

    # get telegram data from dialogflow 
    def rcvUserData(self, key):
        if self.req.get('originalDetectIntentRequest').get('source') == "telegram":
            try:
                data = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('callback_query').get('from').get(key)
            except:
                data = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('from').get(key)
            if key == 'first_name':
                return data
            elif key == 'id':
                return str(data).split('.')[0]
        else:
            return None
            
    def sendMsg(self, get_fb=False, single=False, dual=False, image=False):
        #for single response only
        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text
        telegram = telegram_response()
        tel_main_text = telegram.text_response([self.main_text, self.main_text, False])

        if single == True:
            res_list = [tel_main_text]
            ans_list = [self.main_text]
        elif dual == True:
            tel_sub_text = telegram.text_response([self.sub_text, self.sub_text, False])
            res_list = [tel_main_text, tel_sub_text]
            ans_list = [self.main_text, self.sub_text]
        elif image == True:
            tel_img = telegram.image_response(self.img_url)
            res_list = [tel_main_text ,tel_img]
            ans_list = [self.main_text, self.img_url]
        else:
            sys.exit("Please set one of parameters (single, dual, image) as True!")

        #######Feedback#######
        if get_fb == True:
            #create feedback card response
            title = "How was I doing? Rate my response!"
            buttons = [
                ['👍','👍'],
                ['👎','👎']
            ]
            feedback_card = telegram.card_response(title, buttons)
            res_list.append(feedback_card)
            
            ff_add = ff_response.fulfillment_messages(res_list)

            #create context
            if single or dual or image:
                session = self.req.get('session')
                session_context = [
                                    ['feedback-followup', 1, {'question': self.req.get('queryResult').get('queryText') , 'answer': ans_list}]
                                ]
                #feedback-followup is input context for feedback. None for parameter
                output = ff_response.output_contexts(session, session_context)
        else:
            ff_add = ff_response.fulfillment_messages(res_list)
            output = None

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=output)
        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)

'''
    def rcvFirstName(self):
        if self.req.get('originalDetectIntentRequest').get('source') == "telegram":
            try:
                fn = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('callback_query').get('from').get('first_name')
            except:
                fn = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('from').get('first_name')
            return fn
        else:
            return None

    def rcvChatID(self):
        if self.req.get('originalDetectIntentRequest').get('source') == "telegram":
            try:
                id_ = self.req.get   ('originalDetectIntentRequest').get('payload').get('data').get('callback_query').get('from').get('id')
            except:
                id_ = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('from').get('id')
            return str(id_).split('.')[0]
        else:
            return None
''' 
'''
    def sendMsg(self):
        #for single response only
        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text
        telegram = telegram_response()
        tel_main_text = telegram.text_response([self.main_text, self.main_text, False])

        #######Feedback#######
        if self.get_input == 1:
            #create feedback card response
            title = "How was I doing? Rate my response!"
            buttons = [
                ['👍','👍'],
                ['👎','👎']
            ]
            feedback_card = telegram.card_response(title, buttons)
            ff_add = ff_response.fulfillment_messages([tel_main_text ,feedback_card])

            #create context
            session = self.req.get('session')
            session_context = [
                                    ['feedback-followup', 1, {'question': self.req.get('queryResult').get('queryText') , 'answer': [self.main_text]}]
                                ]
            #feedback-followup is input context for feedback. None for parameter
            output = ff_response.output_contexts(session, session_context)
        else:
            ff_add = None
            output = None

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=output)
        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)


    def sendMsgs(self):
        #for dual response
        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text
        telegram = telegram_response()
        tel_main_text = telegram.text_response([self.main_text, self.main_text, False])
        tel_sub_text = telegram.text_response([self.sub_text, self.sub_text, False])

        #######Feedback#######
        if self.get_input == 1:
            #create feedback card response
            title = "How was I doing? Rate my response!"
            buttons = [
                ['👍','👍'],
                ['👎','👎']
            ]
            feedback_card = telegram.card_response(title, buttons)
            ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_sub_text, feedback_card])

            #create context
            session = self.req.get('session')
            session_context = [
                                    ['feedback-followup', 1, {'question': self.req.get('queryResult').get('queryText') , 'answer': [self.main_text, self.sub_text]}]
                                ]
            #feedback-followup is input context for feedback. None for parameter
            output = ff_response.output_contexts(session, session_context)
        else:
            ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_sub_text])
            output = None

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=output)
        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)

    def sendMsgImg(self):
        #for msg + img response
        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text
        telegram = telegram_response()
        tel_main_text = telegram.text_response([self.main_text, self.main_text, False])
        tel_img = telegram.image_response(self.img_url)

        #######Feedback#######
        if self.get_input == 1:
            #create feedback card response
            title = "How was I doing? Rate my response!"
            buttons = [
                ['👍','👍'],
                ['👎','👎']
            ]
            feedback_card = telegram.card_response(title, buttons)
            ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_img, feedback_card])

            #create context
            session = self.req.get('session')
            session_context = [
                                    ['feedback-followup', 1, {'question': self.req.get('queryResult').get('queryText') , 'answer': [self.main_text, self.img_url]}]
                                ]
            #feedback-followup is input context for feedback. None for parameter
            output = ff_response.output_contexts(session, session_context)
        else:
            ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_img])
            output = None

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=output)
        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)


    def feedbackMsg(self):
        #for feedback response only
        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text
        telegram = telegram_response()

        feedback_card = telegram.card_response(self.main_text, None)
        ff_add = ff_response.fulfillment_messages([feedback_card])

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=None)
        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)
'''
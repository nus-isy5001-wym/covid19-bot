from chatbot_app.models import userDiagnosis
import requests, json

class Notification():
    def __init__(self):
        pass 

    def send_checkin_days(self):
        d_users = list(userDiagnosis.objects.all().values())
        #print(d_users)
        d_user = d_users[0]
        # use this to control the notification sending
        chat_id = d_user['chat_ID']
        datetime = d_user['datetime']
        diag_result = d_user['diagnosis_result']
        checkin = d_user['check_in']

        #token = "1287227674:AAEFQgu9XUwFQUwgINQzyJJWq-0pLz9IYdU"
        token = "855364779:AAEMZZgLu9qzhhoWhiiz5f84QJ5CJn29Uho"
        text = "Would you like to do self assessment on COVID19?"
        reply_markup =  {"inline_keyboard": [[{"text": "Self Assessment","callback_data": "Self Assessment"}],[{"text": "Nope","callback_data" : "Nope"}]]}
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
        
        req = requests.post(url, data = data)
        res = req.json()
        print(res)

    def send_checkin_weeks(self):
        # same as the fucntion above, just different in period of time to send the notification
        pass
        
'''
https://api.telegram.org/bot1287227674:AAEFQgu9XUwFQUwgINQzyJJWq-0pLz9IYdU/sendMessage
{
    "chat_id": "1010367211",
    "text": "Would you like to do self assessment on COVID19?",
    "reply_markup": {
        "inline_keyboard": [
            [{
                "text": "Self Assessment",
                "callback_data": "Self Assessment"
            }],
            [{
                "text": "Nope",
                "callback_data" : "Nope"
            }]
        ]
    }
}
'''
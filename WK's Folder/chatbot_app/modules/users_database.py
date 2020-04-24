from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.models import userList

class UserDB(Server):
    def __init__(self, request):
        super().__init__(request)
        self.first_name = super().rcvUserData('first_name')
        self.chat_ID = super().rcvUserData('id')

    def storeId(self):
        dict = {'first_name' : self.first_name,
                'chat_ID' : self.chat_ID
                }
        try:
            userList.objects.create(**dict) #use ** to add dict into models
            print('New user added.')
        except:
            print('User already exist. Skip')
    
    def subscribe(self):
        userList.objects.filter(chat_ID=self.chat_ID).update(subscribe=True)

        self.main_text = f"Thanks for sub,  {self.first_name}! We will let you know if there is any announcement. 😁"
        return super().sendMsg(get_fb=True, single=True)

    def unsubscribe(self):
        userList.objects.filter(chat_ID=self.chat_ID).update(subscribe=False)
        self.main_text = f"No prob, {self.first_name}! If you want to subscribe to our announcement, just click here /subscribe ❤️"
        return super().sendMsg(get_fb=True, single=True)

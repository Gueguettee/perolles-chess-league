from requests import post as requests_post

class Telegram():

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.last_message_id = None

    def PostMessage(self, message):
        api_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        response = requests_post(api_url, json={'chat_id': self.chat_id, 'text': message})
        if response.status_code == 200:
            data = response.json()
            self.last_message_id = data['result']['message_id']
            return data['result']['message_id']
        else:
            print('Failed to send message')
            return []

    def SendImage(self, image):
        api_url = f'https://api.telegram.org/bot{self.token}/sendPhoto'
        response = requests_post(api_url, json={'chat_id': self.chat_id, 'photo': image})
        if response.status_code == 200:
            data = response.json()
            self.last_message_id = data['result']['message_id']
            return data['result']['message_id']
        else:
            print('Failed to send image')
            return []

    def EditLastMessage(self, new_message):
        if self.last_message_id is not None:
            api_url = f'https://api.telegram.org/bot{self.token}/editMessageText'
            response = requests_post(api_url, json={'chat_id': self.chat_id, 'message_id': self.last_message_id, 'text': new_message})
            if response.status_code != 200:
                print('Failed to edit message')
                return []
            else:
                data = response.json()
                return data['result']['message_id']
        else:
            print('No previous message to edit')
            return []

    def EditMessageId(self, new_message, id):
        api_url = f'https://api.telegram.org/bot{self.token}/editMessageText'
        response = requests_post(api_url, json={'chat_id': self.chat_id, 'message_id': id, 'text': new_message})
        if response.status_code != 200:
            print('Failed to edit message')
            return []
        else:
            data = response.json()
            return data['result']['message_id']
    
if __name__ == "__main__":
    te = Telegram(
    token = '6109483003:AAEyfQm3g5-h3gFtq_BAVtExZSoiWXSS3tM',
    chat_id = '1646128337'
    )
    te.PostMessage("Hello world !")
    te.EditLastMessage("Modified message!")

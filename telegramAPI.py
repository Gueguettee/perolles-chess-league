from requests import post as requests_post

class Telegram():

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def PostMessage(self, message):
        apiURL = f'https://api.telegram.org/bot{self.token}/sendMessage'
        response = requests_post(apiURL, json={'chat_id': self.chat_id, 'text': message})
        #print(response.text)

    def SendImage(self, image):
        apiURL = f'https://api.telegram.org/bot{self.token}/sendPhoto'
        response = requests_post(apiURL, json={'chat_id': self.chat_id, 'photo': image})
        #print(response.text)
    
if __name__ == "__main__":
    te = Telegram(
    token = '6109483003:AAEyfQm3g5-h3gFtq_BAVtExZSoiWXSS3tM',
    chat_id = '1646128337'
    )
    te.PostMessage("Hello world !")

import ollama
from ollama import Client


class Jake:
    def __init__(self):
        self.name = 'Jake'
        # Initializing an empty list for storing the chat messages and setting up the initial system message
        self.chat_messages = []
        self.system_message='You are a helpful assistant and your name is Jake!'
        self.client = Client(host='http://192.168.2.61:11434')
        

    # Defining a function to create new messages with specified roles ('user' or 'assistant')
    def create_message(self, message, role):
        return {
            'role': role,
            'content': message
        }

    # Starting the main conversation loop
    def chat(self):
        # Calling the ollama API to get the assistant response
        
        ollama_response = self.client.chat(model='llama3:latest', stream=True, messages=self.chat_messages)
        

        # Preparing the assistant message by concatenating all received chunks from the API
        assistant_message = ''
        for chunk in ollama_response:
            assistant_message += chunk['message']['content']
            print(chunk['message']['content'], end='', flush=True)
            
        # Adding the finalized assistant message to the chat log
        self.chat_messages.append(self.create_message(assistant_message, 'assistant'))
        return assistant_message

    # Function for asking questions - appending user messages to the chat logs before starting the `chat()` function
    def ask(self, message):
        self.chat_messages.append(
            self.create_message(message, 'user')
        )
        print(f'\n\n--{message}--\n\n')
        return self.chat()

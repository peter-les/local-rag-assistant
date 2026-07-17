# conversation.py
from dataclasses import dataclass


@dataclass
class Message:

    role: str

    content: str


class Conversation:

    def __init__(self):

        self.messages = []

    def add_user(self, text):

        self.messages.append(

            Message(

                "user",

                text

            )

        )

    def add_assistant(self, text):

        self.messages.append(

            Message(

                "assistant",

                text

            )

        )

    def clear(self):

        self.messages.clear()

    def last_messages(self, count=2):

        history = []

        for message in self.messages[-count:]:

            role = "User" if message.role == "user" else "Assistant"
 
            history.append(
                f"{role}: {message.content}"
            )

        return "\n".join(history)
		
    def last_user_questions(self, count=2):

        questions = []

        for message in self.messages:

            if message.role == "user":
                questions.append(message.content)

        return "\n".join(questions[-count:])
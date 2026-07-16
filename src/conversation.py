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

    def last_messages(

            self,

            count=2  # Znížili sme z 6 na 2, aby model nevidel príliš staré debaty
    ):

        return self.messages[-count:]
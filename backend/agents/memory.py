from collections import deque
from langchain_core.messages import BaseMessage


class ConversationMemory:

    def __init__(
        self,
        max_messages: int = 10
    ):
        self.sessions = {}
        self.max_messages = max_messages

    def get_history(
        self,
        session_id: str
    ):
        return list(
            self.sessions.get(
                session_id,
                deque()
            )
        )

    def add_messages(
        self,
        session_id: str,
        messages
    ):

        if session_id not in self.sessions:

            self.sessions[session_id] = deque(
                maxlen=self.max_messages
            )

        for msg in messages:
            self.sessions[
                session_id
            ].append(msg)

    def clear(
        self,
        session_id: str
    ):

        self.sessions.pop(
            session_id,
            None
        )


memory = ConversationMemory()
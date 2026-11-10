
from brain import answer


def respond(question, state=None):
    """
    Handle farmer conversations.

    Old fertilizer stage recommendations are disabled
    until their source information is verified.
    """

    reply = answer(question)

    return reply, None

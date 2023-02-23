import enum


class Conversation(enum.Enum):
    FEEDBACK = enum.auto()
    BROADCAST = enum.auto()


EXPECT_MESSAGE = object()

CANCEL_FEEDBACK_DATA = "cancel_feedback"
CANCEL_BROADCAST_DATA = "cancel_broadcast"

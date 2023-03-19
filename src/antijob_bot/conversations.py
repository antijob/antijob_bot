import enum


class Conversation(int, enum.Enum):
    FEEDBACK = enum.auto()
    BROADCAST = enum.auto()
    EXPECT_MESSAGE = enum.auto()


CANCEL_FEEDBACK_DATA = "cancel_feedback"
CANCEL_BROADCAST_DATA = "cancel_broadcast"

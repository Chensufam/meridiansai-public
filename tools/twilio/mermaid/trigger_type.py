from enum import Enum


class TriggerType(Enum):
    """Enum for valid trigger types."""

    INCOMING_MESSAGE = "incomingMessage"
    INCOMING_CALL = "incomingCall"
    REST_API = "incomingRequest"
    SUBFLOW = "incomingParent"

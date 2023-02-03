from enum import Enum

class ResponseType(Enum):
    NONE = -1
    AUTHORIZATION = 1

class ResultType(Enum):
    NONE = -1
    SUCCESS = 1
    FAILURE = 0

def jsonTemplate():
    return {"type" : ResponseType.NONE.value, "attribute" : {}}
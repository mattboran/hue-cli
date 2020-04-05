class FailedToSetState(Exception):
    msg = "There was an error updating state"

class FailedToGetState(Exception):
    msg = "Failed to fetch state from api"

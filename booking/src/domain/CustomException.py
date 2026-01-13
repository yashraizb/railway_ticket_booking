class CustomException(Exception):
    def __init__(self, message, name="CustomException"):
        self.message = message
        self.name = name
        self.code = self.codeResolver()
    
    def codeResolver(self):
        mapping = {
            "STATION_NOT_FOUND": 400,
            "TRAIN_NOT_FOUND": 400,
            "INVALID_PASSENGER_COUNT": 400,
            "NO_SEATS_AVAILABLE": 409,
            "NOT_ENOUGH_SEATS": 409,
            "TRAIN_FETCH_ERROR": 500,
            "BOOKING_NOT_FOUND": 404,
            "UNAUTHORIZED_CANCELLATION": 403,
        }
        return mapping.get(self.name, 500)

    def getErrorJson(self):
        return {
            "message": self.message,
            "name": self.name,
        }

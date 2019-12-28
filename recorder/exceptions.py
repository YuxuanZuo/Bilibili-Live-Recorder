class LiveRecorderError(Exception):
    pass


class RequestError(LiveRecorderError):
    pass


class APIError(RequestError):
    
    def __init__(self, url, code, message):
        self.url = url
        self.code = code
        self.message = message
        self.url = url

    def __str__(self):
        reason = f"URL: {self.url} Code: {self.code} Message: {self.message}"
        return reason


class FFmpegExecutableError(LiveRecorderError):
    pass


class FFmpegExecutableNotFoundError(FFmpegExecutableError):

    def __str__(self):
        reason = "FFmpeg executable not found!"
        return reason


class FFmpegProcessingError(LiveRecorderError):
    pass


class UnexpectedError(LiveRecorderError):
    pass

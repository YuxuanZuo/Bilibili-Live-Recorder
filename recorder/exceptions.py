# -*- coding: utf-8 -*-

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


class FFmpegError(LiveRecorderError):
    pass


class FFmpegExecutableError(FFmpegError):
    pass


class FFmpegExecutableNotFoundError(FFmpegError):
    pass


class FFmpegProcessingError(FFmpegError):
    pass


class ConfigFileError(LiveRecorderError):
    pass


class ConfigFileReadError(ConfigFileError):
    pass


class ConfigFileNotFoundError(ConfigFileError):
    pass


class UnexpectedError(LiveRecorderError):
    pass

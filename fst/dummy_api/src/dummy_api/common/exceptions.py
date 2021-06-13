import typing as t
from werkzeug.exceptions import HTTPException
from flask import jsonify


class BaseException(HTTPException):
    """description"""
    code = None
    description = None
    moreInfo = None

    def __init__(
        self,
        description: t.Optional[str]=None,
        response: t.Optional["Response"]=None,
    ):
        super().__init__(description, response)
        self.data = {
            "code": self.code,
            "message": self.description,
            "moreInfo": self.moreInfo,
        }


class InvalidParams(BaseException):
    """description"""
    code = 400
    description = (
        "Illegal or invalid parameters: [arg]"
    )
    moreInfo = (
        "The parameter set is malformed or invalid"
    )
    def __init__(
        self,
        arg_name: t.Optional[str]=None,
        description: t.Optional[str]=None,
        response: t.Optional["Response"]=None,
    ):
        if arg_name:
            self.description = (
                "Illegal or invalid parameters: [{}]".format(arg_name)
            )
        super().__init__(description, response)


class RequiredParams(BaseException):
    """description"""
    code = 400
    description = (
        "Required parameters are not set"
    )


class InternalServerError(BaseException):
    """description"""
    code = 500
    description = (
        "An error has been detected inside the server. "
        "Our engineer is responding"
    )


class InvalidInstrumentPair(BaseException):
    """description"""
    code = 400
    description = (
        "Invalid instrument pairs"
    )


class AccountNotFound(BaseException):
    """description"""
    code = 404
    description = (
        "The set account ID is incorrect"
    )


class InvalidDatetimeFormat(BaseException):
    """description"""
    code = 400
    description = (
        "Invalid Datetime format. "
        "Chose \'RFC3339\' or \'UNIX\' format."
    )

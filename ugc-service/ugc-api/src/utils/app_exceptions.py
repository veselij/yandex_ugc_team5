from fastapi import Request
from starlette.responses import JSONResponse


class AppExceptionCaseError(Exception):
    def __init__(self, status_code: int, context: dict = None):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCaseError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class AppException:
    class UnhandledError(AppExceptionCaseError):
        def __init__(self, context: dict = None):
            status_code = 500
            AppExceptionCaseError.__init__(self, status_code, context)

    class AlreadyExistsError(AppExceptionCaseError):
        def __init__(self, context: dict = None):
            status_code = 409
            AppExceptionCaseError.__init__(self, status_code, context)

    class BadRequestError(AppExceptionCaseError):
        def __init__(self, context: dict = None):
            status_code = 400
            AppExceptionCaseError.__init__(self, status_code, context)

    class NotFoundError(AppExceptionCaseError):
        def __init__(self, context: dict = None):
            status_code = 404
            AppExceptionCaseError.__init__(self, status_code, context)

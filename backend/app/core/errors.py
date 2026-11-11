from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_error_handlers(app: FastAPI) -> None:
    """Every error leaves the API as { "detail": "message" }, as the API contract says."""

    @app.exception_handler(RequestValidationError)
    async def validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": format_validation_errors(exc.errors())},
        )


def format_validation_errors(errors: list[dict]) -> str:
    messages = []
    for error in errors:
        # loc looks like ("body", "pricePerHour"); keep only the field part
        field = ".".join(
            str(part) for part in error["loc"] if part not in ("body", "query", "path")
        )
        message = error["msg"].removeprefix("Value error, ")
        messages.append(f"{field}: {message}" if field else message)
    return "; ".join(messages)

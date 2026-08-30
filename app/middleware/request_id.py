import uuid
from fastapi import Request


async def request_id_middleware(request: Request, call_next):
    # Check whether the client already sent a request ID
    request_id = request.headers.get("X-Request-ID")

    # If not, generate a new unique ID
    if not request_id:
        request_id = str(uuid.uuid4())

    # Store it in request.state so other parts of the application
    # can access it during this request
    request.state.request_id = request_id

    # Continue processing the request
    response = await call_next(request)

    # Add the request ID to the response headers
    response.headers["X-Request-ID"] = request_id

    return response
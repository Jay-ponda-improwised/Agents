import logging
import time
from datetime import datetime, timezone
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import json
from typing import Any, cast

logger = logging.getLogger(__name__)

class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add processing time and timestamps to response metadata
    """

    async def dispatch(self, request: Request, call_next):
        # Capture request time in UTC
        request_time = datetime.now(timezone.utc).isoformat()
        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as e:
            # Even if there's an error, we still want to add timing info
            process_time = time.time() - start_time
            response_time = datetime.now(timezone.utc).isoformat()

            logger.error(f"Error processing request: {e}")
            # Return a proper error response with timing information
            response_content = json.dumps({
                "error": str(e),
                "meta": {
                    "requestTime": request_time,
                    "responseTime": response_time,
                    "processTime": round(process_time, 4)
                }
            })
            return Response(
                content=response_content,
                status_code=500,
                media_type="application/json"
            )

        # Capture response time in UTC
        response_time = datetime.now(timezone.utc).isoformat()
        process_time = time.time() - start_time

        # For JSON responses, add timing to the response body
        if response.headers.get("content-type", "").startswith("application/json"):
            try:
                # Read the response body
                body = b""
                async for chunk in cast(Any, response).body_iterator:
                    body += chunk

                # Parse the JSON response
                if body:
                    response_data = json.loads(body.decode())

                    # Add timing information to the response
                    if isinstance(response_data, dict):
                        if "meta" not in response_data:
                            response_data["meta"] = {}
                        response_data["meta"]["requestTime"] = request_time
                        response_data["meta"]["responseTime"] = response_time
                        response_data["meta"]["processTime"] = round(process_time, 4)
                    else:
                        # If response is not a dict, wrap it
                        response_data = {
                            "data": response_data,
                            "meta": {
                                "requestTime": request_time,
                                "responseTime": response_time,
                                "processTime": round(process_time, 4)
                            }
                        }

                    # Create new response with modified content
                    response_content = json.dumps(response_data)
                    response.headers["content-length"] = str(len(response_content.encode()))

                    return Response(
                        content=response_content,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.media_type
                    )
                else:
                    # Empty response
                    response_content = json.dumps({
                        "meta": {
                            "requestTime": request_time,
                            "responseTime": response_time,
                            "processTime": round(process_time, 4)
                        }
                    })
                    response.headers["content-length"] = str(len(response_content.encode()))

                    return Response(
                        content=response_content,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.media_type
                    )
            except Exception as e:
                # If we can't parse or modify the response, just add the timing as a header
                logger.warning(f"Could not add timing to JSON response: {e}")
                response.headers["X-Request-Time"] = request_time
                response.headers["X-Response-Time"] = response_time
                response.headers["X-Process-Time"] = str(round(process_time, 4))
                return response
        else:
            # For non-JSON responses, add timing as headers
            response.headers["X-Request-Time"] = request_time
            response.headers["X-Response-Time"] = response_time
            response.headers["X-Process-Time"] = str(round(process_time, 4))
            return response
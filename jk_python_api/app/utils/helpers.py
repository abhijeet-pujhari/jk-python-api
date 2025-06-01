# Utility helper functions

from fastapi import HTTPException

def not_found_exception(detail: str = "Not found"):
    raise HTTPException(status_code=404, detail=detail)

def bad_request_exception(detail: str = "Bad request"):
    raise HTTPException(status_code=400, detail=detail)

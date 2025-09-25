import json
import logging
import re


RE_EMAIL = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
RE_PHONE = re.compile(r"(?:(?:\+\d{1,3}[\s-]?)?(?:\(\d{1,4}\)|\d{1,4})[\s-]?)?\d{3,4}[\s-]?\d{3,4}")


def redact_pii(text: str) -> str:
    if not text:
        return text
    text = RE_EMAIL.sub("[REDACTED_EMAIL]", text)
    text = RE_PHONE.sub("[REDACTED_PHONE]", text)
    return text


class PiiSafeLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("django.request")

    def __call__(self, request):
        try:
            body_preview = None
            if request.method in ("POST", "PUT", "PATCH"):
                try:
                    # Read a safe preview only; avoid large payloads
                    raw = request.body.decode("utf-8", errors="ignore")[:2000]
                    body_preview = redact_pii(raw)
                except Exception:
                    body_preview = None
            self.logger.info(
                "req %s %s preview=%s", request.method, request.path, body_preview
            )
        except Exception:
            # Never break the request flow for logging errors
            pass

        response = self.get_response(request)
        try:
            self.logger.info("res %s %s status=%s", request.method, request.path, response.status_code)
        except Exception:
            pass
        return response



import re
import time
from urllib.parse import urlsplit

import requests

_SECRET_PATTERNS = [
    re.compile(r"(api-key=)[^&\s'\"]+", re.I),
    re.compile(r"(x-api-key['\"]?\s*[:=]\s*['\"]?)[^&\s'\"]+", re.I),
]


def scrub(text: str) -> str:
    """Remove API keys from anything that might be logged or printed."""
    for pat in _SECRET_PATTERNS:
        text = pat.sub(r"\1***", text)
    return text


class ApiError(Exception):
    def __init__(self, message: str, status: int | None = None, body: str | None = None):
        super().__init__(scrub(message))
        self.status = status
        self.body = scrub(body or "")


class Http:
    """requests wrapper: retries 429/5xx with backoff, logs every call, never logs secrets."""

    def __init__(self, db=None, timeout: float = 15.0, max_retries: int = 2, sleep=time.sleep):
        self.db = db
        self.timeout = timeout
        self.max_retries = max_retries
        self.sleep = sleep
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "shadowbot/0.1"

    def _log(self, source, url, label, ok, status, ms, error):
        if self.db is None:
            return
        self.db.log_api_call(ts=int(time.time()), source=source, endpoint=label or urlsplit(url).path, ok=ok,
                             status=status, latency_ms=ms, error=scrub(error) if error else None)

    def request(self, source: str, method: str, url: str, *, params=None, json=None, headers=None, label=None):
        last: ApiError | None = None
        for attempt in range(self.max_retries + 1):
            t0 = time.monotonic()
            try:
                r = self.session.request(method, url, params=params, json=json, headers=headers, timeout=self.timeout)
            except requests.RequestException as exc:
                ms = int((time.monotonic() - t0) * 1000)
                last = ApiError(f"network error: {exc}")
                self._log(source, url, label, False, None, ms, str(last))
            else:
                ms = int((time.monotonic() - t0) * 1000)
                if r.status_code == 429 or r.status_code >= 500:
                    last = ApiError(f"HTTP {r.status_code}", r.status_code, r.text[:300])
                    self._log(source, url, label, False, r.status_code, ms, str(last))
                elif r.status_code >= 400:
                    err = ApiError(f"HTTP {r.status_code}", r.status_code, r.text[:300])
                    self._log(source, url, label, False, r.status_code, ms, str(err))
                    raise err
                else:
                    try:
                        data = r.json()
                    except ValueError:
                        err = ApiError("response was not JSON", r.status_code, r.text[:300])
                        self._log(source, url, label, False, r.status_code, ms, str(err))
                        raise err
                    self._log(source, url, label, True, r.status_code, ms, None)
                    return data
            if attempt < self.max_retries:
                self.sleep(min(8.0, 1.5 * (2 ** attempt)))
        raise last or ApiError("request failed")

    def get(self, source, url, **kw):
        return self.request(source, "GET", url, **kw)

    def post(self, source, url, **kw):
        return self.request(source, "POST", url, **kw)

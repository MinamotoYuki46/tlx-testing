"""
config.py
Memuat konfigurasi dari file .env menggunakan python-dotenv.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL             = os.getenv("BASE_URL", "https://tlx.toki.id")
WAIT_TIMEOUT         = int(os.getenv("WAIT_TIMEOUT", "10"))
HEADLESS             = os.getenv("HEADLESS", "true").lower() == "true"

VALID_USERNAME       = os.getenv("VALID_USERNAME", "")
VALID_PASSWORD       = os.getenv("VALID_PASSWORD", "")

VALID_PROBLEM_SLUG   = os.getenv("VALID_PROBLEM_SLUG", "problems/playground/hello-world")
VALID_CONTEST_SLUG   = os.getenv("VALID_CONTEST_SLUG", "contests/acmicpc-jakarta-2023-regional")
VALID_COURSE_SLUG    = os.getenv("VALID_COURSE_SLUG",  "courses/prog-dasar")

INVALID_PROBLEM_SLUG = os.getenv("INVALID_PROBLEM_SLUG", "problems/xxxxxxxxxxx-invalid-999")
INVALID_CONTEST_SLUG = os.getenv("INVALID_CONTEST_SLUG", "contests/xxxxxxxxxxx-invalid-999")
INVALID_COURSE_SLUG  = os.getenv("INVALID_COURSE_SLUG",  "courses/xxxxxxxxxxx-invalid-999")

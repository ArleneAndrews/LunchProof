app.secret_key = ""

try:
from .private import *
except Exception:
pass
from .base import *
import os


if os.environ.get('ENV') == 'prod':
    from .production import *
else:
    from .local import *

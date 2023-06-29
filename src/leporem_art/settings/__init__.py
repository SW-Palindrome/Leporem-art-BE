import os

from .base import *

if os.environ.get('ENV') == 'prod':
    from .production import *
else:
    from .local import *

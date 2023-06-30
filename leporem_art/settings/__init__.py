import os

from .base import *

if os.environ.get('ENV') == 'prod':
    from .production import *
elif os.environ.get('ENV') == 'dev':
    from .develop import *
else:
    from .local import *

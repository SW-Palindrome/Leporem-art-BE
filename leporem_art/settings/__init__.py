import os

from .base import *

if os.environ.get('ENV') == 'prod':
    from .production import *
elif os.environ.get('ENV') == 'dev':
    from .develop import *
elif os.environ.get('ENV') == 'test':
    from .test import *
else:
    from .local import *

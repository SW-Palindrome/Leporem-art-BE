import uuid


def create_random_filename(filename):
    extension = filename.split('.')[-1]
    return str(uuid.uuid4()) + '.' + extension

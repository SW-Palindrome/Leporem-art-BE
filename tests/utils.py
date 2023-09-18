from apps.users.models import User
from utils.auth.leporemart import generate_access_token


def force_login(client, user: User):
    oauth_info = user.user_oauth_info.last()
    access_token, _ = generate_access_token(oauth_info.provider, oauth_info.provider_id, "access")
    client.defaults.update({'HTTP_AUTHORIZATION': f'Bearer {access_token}'})

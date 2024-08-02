from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class EmailOrUsernameLogin(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None

        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

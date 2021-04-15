from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(**kwargs):
    if 'username' not in kwargs:
        kwargs['username'] = 'user_foo%d' % User.objects.all().count()

    if 'email' not in kwargs:
        kwargs['email'] = '%s@bar.com' % kwargs['username']

    if 'password' not in kwargs:
        kwargs['password'] = 'bar'

    return User.objects.create_user(**kwargs)

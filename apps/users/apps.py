from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户信息管理'

    def ready(self):
        import users.signal

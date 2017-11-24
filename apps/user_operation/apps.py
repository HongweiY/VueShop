from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'user_operation'
    verbose_name = '用户行为管理'

    def ready(self):
        import user_operation.signal

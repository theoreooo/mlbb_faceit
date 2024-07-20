from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# Установите переменную окружения для конфигурации Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mlbb_faceit.settings')

# Создайте экземпляр Celery
app = Celery('mlbb_faceit')

# Загрузите настройки из файла settings.py, используя пространство имен "CELERY"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически найдите задачи в приложениях Django
app.autodiscover_tasks()

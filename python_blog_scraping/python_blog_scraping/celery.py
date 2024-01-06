import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_blog_scraping.settings')

broker='amqp://{0}:{1}@{2}:{3}/{4}'.format(
    os.environ["RABBITMQ_DEFAULT_USER"], os.environ["RABBITMQ_DEFAULT_PASS"], os.environ["BROKER_HOST"],
    os.environ["BROKER_PORT"], os.environ["RABBITMQ_DEFAULT_VHOST"]
)

app = Celery('python_blog_scraping', broker=broker, backend='rpc://', include=['python_blog_scraping.tasks'])

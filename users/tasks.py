from celery import shared_task
from datetime import datetime
from .models import Queue, WaitingTime
from .utils import calculate_time


@shared_task
def record_waiting_time():
    queues = Queue.objects.all()
    for queue in queues:
        now = datetime.now()
        waiting_time = calculate_time(
            now, queue.num_servers, queue.max_service, queue.min_service)[1]
        WaitingTime.objects.create(waiting_time=waiting_time, service_name=queue.service_name,
                                   org_id=queue.org.org_id)

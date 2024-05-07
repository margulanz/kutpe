from celery import shared_task
from datetime import datetime, timedelta
from .models import Queue, WaitingTime
from .utils import calculate_time


@shared_task
def record_waiting_time():
    queue = Queue.objects.get(id=1)

    start_time = datetime(2024,
                          4, 19)

    # Define the end time as the end of the day
    end_time = start_time + timedelta(days=1)

    # Iterate over every minute of the day
    current_time = start_time
    while current_time < end_time:
        # Calculate waiting time for the current minute
        waiting_time = calculate_time(
            current_time, queue.num_servers, queue.max_service, queue.min_service)[1]

        # Create a WaitingTime object for the current minute
        WaitingTime.objects.create(
            waiting_time=waiting_time,
            service_name=queue.service_name,
            org_id=queue.org.org_id,
            date=current_time
        )

        # Move to the next minute
        current_time += timedelta(minutes=1)

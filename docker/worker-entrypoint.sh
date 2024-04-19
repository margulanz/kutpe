#!/bin/sh


until cd /app/
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A kutpe worker -B -l INFO

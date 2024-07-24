1. Run now through the future every 1 min
  ```add_user.apply_async(args=(form.data,), eta=datetime.utcnow() + timedelta(minutes=1))```

2. Celery -B: run thing on a particular schedule 
  - Should seperate to another worker
  - @shared_task -> register new task
  - CELERY_CONFIG: beat_schedule: task_name: task: "tasks.sec" schedule: 20 arg: 1,2

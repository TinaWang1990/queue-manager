backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── queue.py
│   │   ├── user.py
│   │   ├── queue_entry.py
│   │   ├── admin.py
│   │   └── note.py
│   ├── schemas/
│   │   ├── queue.py
│   │   ├── patient.py
│   │   ├── admin.py
│   ├── routers/
│   │   ├── queues.py
│   │   ├── patient.py
│   │   ├── admin.py
│   │   └── root.py
│   └── services/
│       ├── wait_time.py
│       └── sms.py
├── alembic/
├── requirements.txt
├── Dockerfile

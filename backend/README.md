# Run appilcation
```
./run.sh start
```

# databse migration
 ```
 pip install alembic
 cd backend
 alembic init alembic
 #config files under alembic
 alembic revision --autogenerate -m "add_address_and_image_to_queue"
 alembic upgrade head
 ```
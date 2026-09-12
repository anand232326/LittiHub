auth-service/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── logger.py
│   │   ├── exceptions.py
│   │   └── enums.py
│   │
│   ├── middleware/
│   │   ├── error_handler.py
│   │   ├── logging.py
│   │   └── request_id.py
│   │
│   ├── dependencies/
│   │   └── auth.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── schemas/
│   │   └── auth.py
│   │
│   ├── repositories/
│   │   └── user_repository.py
│   │
│   ├── services/
│   │   └── auth_service.py
│   │
│   ├── controllers/
│   │   └── auth_controller.py
│   │
│   ├── routers/
│   │   └── auth.py
│   │
│   └── main.py
│
├── .env
├── .env.example
├── requirements.txt
├── Dockerfile
└── README.md
services/
└── restaurant-service/
    ├── app/
    │   ├── core/
    │   │   ├── config.py
    │   │   ├── database.py
    │   │   ├── logger.py
    │   │   └── exceptions.py
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
    │   │   └── restaurant.py
    │   │
    │   ├── schemas/
    │   │   └── restaurant.py
    │   │
    │   ├── repositories/
    │   │   └── restaurant_repository.py
    │   │
    │   ├── services/
    │   │   └── restaurant_service.py
    │   │
    │   ├── controllers/
    │   │   └── restaurant_controller.py
    │   │
    │   ├── routers/
    │   │   └── restaurant.py
    │   │
    │   └── main.py
    │
    ├── .env
    ├── .env.example
    ├── requirements.txt
    ├── Dockerfile
    └── README.md
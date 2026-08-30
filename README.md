backend/
│
├── app/
│   │
│   ├── core/
│   │   ├── config.py                 # Environment/configuration
│   │   ├── database.py               # MongoDB + Beanie initialization
│   │   ├── security.py               # bcrypt, JWT, OAuth2 security
│   │   ├── constants.py              # Application constants
│   │   ├── exceptions.py             # Custom application exceptions
│   │   └── logging.py                # Application logging configuration
│   │
│   ├── middleware/
│   │   ├── request_id.py             # Unique request/correlation ID
│   │   ├── logging.py                # Request/response logging
│   │   ├── rate_limit.py             # Redis-based rate limiting
│   │   └── error_handler.py          # Global exception handling
│   │
│   ├── dependencies/
│   │   ├── auth.py                   # Current user / authorization
│   │   ├── database.py               # DB-related dependencies
│   │   └── common.py                 # Shared FastAPI dependencies
│   │
│   ├── models/
│   │   ├── user.py                   # User Beanie document
│   │   ├── restaurant.py              # Restaurant document
│   │   ├── menu.py                   # Menu document
│   │   ├── order.py                  # Order document
│   │   └── ...
│   │
│   ├── schemas/
│   │   ├── user.py                   # User request/response schemas
│   │   ├── auth.py                   # Login/token schemas
│   │   ├── restaurant.py             # Restaurant schemas
│   │   ├── menu.py                   # Menu schemas
│   │   ├── order.py                  # Order schemas
│   │   └── ...
│   │
│   ├── repositories/
│   │   ├── user_repository.py        # User DB operations
│   │   ├── restaurant_repository.py # Restaurant DB operations
│   │   ├── menu_repository.py        # Menu DB operations
│   │   ├── order_repository.py       # Order DB operations
│   │   └── ...
│   │
│   ├── services/
│   │   ├── auth_service.py           # Authentication business logic
│   │   ├── user_service.py           # User business logic
│   │   ├── restaurant_service.py     # Restaurant business logic
│   │   ├── menu_service.py           # Menu business logic
│   │   ├── order_service.py          # Order business logic
│   │   ├── payment_service.py        # Payment business logic
│   │   └── ...
│   │
│   ├── controllers/
│   │   ├── auth_controller.py        # Auth HTTP orchestration
│   │   ├── user_controller.py        # User HTTP orchestration
│   │   ├── restaurant_controller.py  # Restaurant HTTP orchestration
│   │   ├── menu_controller.py        # Menu HTTP orchestration
│   │   ├── order_controller.py       # Order HTTP orchestration
│   │   └── ...
│   │
│   ├── routers/
│   │   │
│   │   └── v1/
│   │       ├── auth.py               # /api/v1/auth/*
│   │       ├── users.py              # /api/v1/users/*
│   │       ├── restaurants.py        # /api/v1/restaurants/*
│   │       ├── menu.py               # /api/v1/menu/*
│   │       ├── orders.py             # /api/v1/orders/*
│   │       └── ...
│   │
│   ├── clients/
│   │   ├── redis_client.py           # Redis connection/client
│   │   ├── kafka_client.py           # Kafka connection/client
│   │   └── ...
│   │
│   ├── events/
│   │   ├── publishers/
│   │   │   ├── order_events.py
│   │   │   └── ...
│   │   │
│   │   └── consumers/
│   │       ├── payment_consumer.py
│   │       ├── inventory_consumer.py
│   │       ├── notification_consumer.py
│   │       └── ...
│   │
│   ├── utils/
│   │   ├── datetime.py
│   │   ├── pagination.py
│   │   └── ...
│   │
│   └── main.py
│
├── docker/
│   ├── docker-compose.yml
│   ├── nginx/
│   │   └── nginx.conf
│   └── redis/
│       └── redis.conf
│
├── migrations/
│   └── ...
│
├── tests/
│   ├── unit/
│   │   ├── services/
│   │   └── repositories/
│   │
│   ├── integration/
│   │   ├── auth/
│   │   ├── users/
│   │   └── orders/
│   │
│   └── conftest.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md



# HLD

                       ┌───────────────────────┐
                       │     Web / Mobile      │
                       │      React App        │
                       └───────────┬───────────┘
                                   │
                              HTTPS / TLS
                                   │
                                   ▼
                ┌──────────────────────────────────┐
                │              NGINX                │
                │                                  │
                │ Reverse Proxy / Load Balancer    │
                │ TLS Termination                  │
                │ Rate Limiting                    │
                │ Routing                          │
                └────────────────┬─────────────────┘
                                 │
                                 ▼
                ┌──────────────────────────────────┐
                │          API GATEWAY              │
                │                                  │
                │ Authentication / Authorization   │
                │ Rate Limiting                    │
                │ Request ID                       │
                │ Routing                          │
                │ API Versioning                   │
                └────────────────┬─────────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
   ┌─────────────┐       ┌──────────────┐       ┌──────────────┐
   │Auth /       │       │ User Service │       │ Restaurant   │
   │Identity     │       │              │       │ Service      │
   └──────┬──────┘       └──────┬───────┘       └──────┬───────┘
          │                     │                      │
          ▼                     ▼                      ▼
       MongoDB               MongoDB                MongoDB


          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
   ┌─────────────┐       ┌──────────────┐       ┌──────────────┐
   │Menu Service │       │ Order        │       │ Inventory    │
   │             │       │ Service      │       │ Service      │
   └──────┬──────┘       └──────┬───────┘       └──────┬───────┘
          │                     │                      │
          ▼                     ▼                      ▼
       MongoDB               MongoDB                MongoDB


                          ORDER EVENTS
                               │
                               ▼
                     ┌─────────────────────┐
                     │        KAFKA        │
                     │  Event Infrastructure│
                     └──────────┬──────────┘
                                │
         ┌──────────────────────┼─────────────────────┐
         │                      │                     │
         ▼                      ▼                     ▼
  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
  │Payment       │      │Delivery      │      │Notification  │
  │Service       │      │Service       │      │Service       │
  └──────┬───────┘      └──────┬───────┘      └──────────────┘
         │                     │
         ▼                     ▼
      MongoDB               MongoDB
                               │
                               ▼
                             Redis
                        Rider availability
                        Short-lived data


                ┌─────────────────────────────────┐
                │             REDIS               │
                │                                 │
                │ Cache                           │
                │ Rate Limiting                   │
                │ Cart                            │
                │ Sessions / Token metadata       │
                │ Distributed Locks               │
                │ Idempotency                     │
                │ Rider Availability              │
                │ Short-lived data                │
                └─────────────────────────────────┘


                ┌─────────────────────────────────┐
                │          SEARCH                 │
                │       OpenSearch/Elastic        │
                └─────────────────────────────────┘


                ┌─────────────────────────────────┐
                │       OBJECT STORAGE            │
                │          S3 / MinIO             │
                │ Menu / Restaurant Images        │
                └─────────────────────────────────┘


                ┌─────────────────────────────────┐
                │        OBSERVABILITY             │
                │ Prometheus                      │
                │ Grafana                         │
                │ Loki                            │
                │ OpenTelemetry                   │
                └─────────────────────────────────┘


                ┌─────────────────────────────────┐
                │       INFRASTRUCTURE             │
                │ Docker → Kubernetes              │
                │ Autoscaling / Service Discovery │
                └─────────────────────────────────┘#   L i t t i H u b  
 
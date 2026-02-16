# Planetarium API Service 🌌

The Planetarium API Service is a specialized platform for managing planetarium operations, scheduling astronomy shows, and handling ticket reservations. This project was developed using the **Django REST Framework** as part of a Portfolio Project.

## ✨ Key Features

- **JWT Authentication**: Full system for user registration, login, and profile management.
- **Planetarium Management**: Create and manage planetarium domes, show themes, and specific sessions.
- **Reservation System**: Seamless ticket booking with automated seat validation to prevent overbooking or selecting non-existent seats.
- **Filtering**: Advanced search functionality for astronomy shows by title or specific themes.
- **API Documentation**: Interactive and user-friendly API schema provided via Swagger (drf-spectacular).

## 🛠️ Tech Stack

- **Python 3.11+**
- **Django & DRF**
- **SQLite** (Database)
- **Docker & Docker Compose**
- **JWT (Simple JWT)**

## 🚀 How to Run Locally

### Using Docker (Recommended)
Docker is the fastest way to get the project running with all configurations pre-set.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dasha05896/planetarium-api-service.git
   cd planetarium_api_service
   
Build and Start:

docker-compose up --build


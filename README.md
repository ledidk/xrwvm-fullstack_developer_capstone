# XR Dealership Review Platform

A microservices-based full stack app for managing dealerships and reviewing cars. Built as a capstone project combining React, Django, Node.js, and sentiment analysis.

## What's Inside

**Frontend**: React UI for browsing dealerships, viewing inventory, and posting reviews  
**Backend**: Django REST API managing authentication, dealership data, and review coordination  
**Database Service**: Node.js/Express layer for car records, dealership info, and reviews  
**Sentiment Analysis**: Microservice for analyzing review sentiment  

Stack: React | Django | Node.js | MongoDB | Docker | Kubernetes

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js
- Git

### Setup

```bash
# 1. Clone & activate Python environment
git clone https://github.com/ledidk/xrwvm-fullstack_developer_capstone.git
cd xrwvm-fullstack_developer_capstone/server
source env/Scripts/activate  # Windows: .\myenv\Scripts\activate

# 2. Build frontend
cd frontend
npm install
npm run build
cd ..

# 3. Install Python dependencies & migrate DB
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

# 4. Run it
python manage.py runserver
```

Navigate to `http://localhost:8000` to see it running.

## Deployment

Docker & Kubernetes configs included. Check `deployment.yaml` and `docker-compose.yml` for containerized setups.



<a href="https://task-manager-mritesh.vercel.app/" target="_blank" rel="noopener noreferer">To the App</a>

# Task Management Application

A full-stack task management application with a Next.js frontend, FastAPI backend, and PostgreSQL database.

## 🚀 Production Stack

- **Frontend**: Next.js 16
- **Backend**: FastAPI + Python 3.13 (not really necessary but aids in learning)
- **Database**: PostgreSQL

## 🏗️ Architecture (subject to change based on credit balance)

```
┌─────────────┐      ┌──────────────┐      ┌───────────────┐
│   Vercel    │─────▶│   Railway    │─────▶│   Supabase    │
│  (Next.js)  │      │   (FastAPI)  │      │ (PostgreSQL)  │
└─────────────┘      └──────────────┘      └───────────────┘
     Frontend              Backend              Database
```

## 🛠️ Local Development

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.13+

### Quick Start

1. **Clone the repository**
   ```bash
   git clone git@github.com:MriteshAdak/Task_Manager.git
   cd Task_Manager
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up
   ```

### Manual Setup (without Docker)

**Backend:**
```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd ../ui
npm install
npm run dev
```

## 📦 Project Structure

```
.
├── api/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py        # API routes & CORS config
│   │   ├── database.py    # Database connection
│   │   ├── models.py      # SQLAlchemy models
│   │   ├── repository.py  # Data access layer
│   │   └── schemas.py     # Pydantic schemas
│   ├── Dockerfile         # Docker config backend container
│   └── requirements.txt   # Python dependencies
├── ui/                    # Next.js frontend
│   ├── src/
│   │   ├── app/          # Next.js app router
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── lib/          # Utilities & API proxy
│   │   ├── types/        # Interfaces (contracts)
│   │   └── services/     # API & storage services
│   ├── Dockerfile        # Docker config frontend container
│   └── package.json      # Node dependencies
└── docker-compose.yml    # Local containerization setup
```

## 🔧 Configuration

### Environment Variables

**Backend (Railway):**
- `DATABASE_URL` - PostgreSQL connection string from Supabase (may defer based on the type of connection you choose)
- `UI_ORIGINS` - Comma-separated list of allowed origins for CORS

**Frontend (Vercel):**
- `BACKEND_URL` - Railway API URL for server-side requests

### Quick Deploy Steps

1. **Setup Supabase** → Get DATABASE_URL
2. **Deploy to Railway** → Set DATABASE_URL and UI_ORIGINS
3. **Deploy to Vercel** → Set BACKEND_URL to Railway URL
4. **Update CORS** → Add Vercel URL to Railway's UI_ORIGINS

## 🧪 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

Full API documentation available at `/docs` when running the backend.

## 🎨 Features

- ✅ Task CRUD operations
- ✅ Kanban board view (To Do, In Progress, Done)
- ✅ Due date support
- ✅ Responsive design with Tailwind CSS
- ✅ Smooth animations with Framer Motion
- ✅ Production-ready with proper error handling
- ✅ CORS configured for cross-origin requests
- ✅ Health checks and monitoring
- ✅ Connection pooling for database

## 🔒 Security

- Environment variables for sensitive data
- CORS protection on the backend
- Server-side API proxy to hide backend URLs
- Secure database connections with SSL
- Non-root Docker user

## 📊 Monitoring

- Railway: Built-in logging and metrics
- Vercel: Analytics and deployment logs
- Supabase: Database performance monitoring

## 🗺 Future Roadmap

- [ ] **Service Split**: Decouple modules into a standalone internal service.
#### NOTE: This application has no practical purpose other than learning different stacks and transitioning from badly deisgned system (intentional) to a structured application design. 
- [ ] **User-Task Mapping**: Transition Postgres schema to support `user_id` foreign keys.
- [ ] **MongoDB**: Adding MongoDB in the mix for learning purposes. Additional services will be created. Either be limited to storing telemetry (auditing) or the core collections/tables.
- [ ] **SpringBoot**: Write the backend/router in Spring Boot for learning purposes.
- [ ] **Angular**: Angular FrontEnd for learning purposes.
- [ ] **NextJS**: a server component to replace the backend entirely, there will be options. a starter project too various stacks.

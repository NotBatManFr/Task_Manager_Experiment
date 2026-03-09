
<a href="https://task-manager-mritesh.vercel.app/" target="_blank" rel="noopener noreferer">To the App</a> - (might take ~30 secs to load up because of free tier limitations)

# Task Management Application

A full-stack task management application with a Next.js frontend, FastAPI backend, and PostgreSQL database.

## 🚀 Production Stack

- **Frontend**: Next.js 16 (can replace the backend using Prisma as the ORM)
- **Backend**: FastAPI + Python 3.13 (not really necessary but aids in learning)
- **Database**: PostgreSQL

## 🏗️ Architecture (subject to change based on credit balance)

```
 Vercel    ->    Render    ->    Supabase
(NextJS)        (FastAPI)      (PostgreSQL)
```

## 🛠️ Local Development

### Prerequisites
- Docker & Docker Compose
- Node.js 21
- Python 3.12

### Quick Start

1. **Clone the repository**
   ```bash
   git clone git@github.com:MriteshAdak/Task_Manager.git
   cd Task_Manager
   ```

2. **Start with Docker Compose**
   ```bash
   docker compose up
   ```

## 🔧 Configuration

### Environment Variables

**Backend (Railway):**
- `DB_USER` - PostgreSQL username
- `DB_PASSWORD` - PostgreSQL password
- `DB_HOST` - PostgreSQL host
- `DB_PORT` - PostgreSQL port
- `DB_NAME` - PostgreSQL database name
- `UI_ORIGINS` - Comma-separated list of allowed UI origins for CORS

**Frontend (Vercel):**
- `BACKEND_URL` -  API URL for server-side requests

### Quick Deploy Steps

1. **Setup Supabase** → Collect DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
2. **Deploy to Render** → Set the DB_* vars and UI_ORIGINS
3. **Deploy to Vercel** → Set BACKEND_URL to Render URL
4. **Update CORS** → Add Vercel URL to Render's UI_ORIGINS

## 🧪 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Retrieve one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

Full API documentation available at `/docs` when running the backend locally.

## 🔒 Security

- Environment variables for sensitive data
- CORS protection on the backend
- Server-side API proxy to hide backend URLs
- Secure database connections with SSL
- Non-root Docker user

## 🗺 Future Roadmap

- [x] **Service Split**: Decouple modules into a standalone internal service.
#### NOTE: This application has no practical purpose other than learning different stacks and transitioning from badly deisgned system (intentional) to a structured application design. 
- [ ] **User-Task Mapping**: Transition Postgres schema to support `user_id` foreign keys.
- [ ] **MongoDB**: Adding MongoDB in the mix for learning purposes. Additional services will be created. Either be limited to storing telemetry (auditing) or the core collections/tables.
- [ ] **SpringBoot**: Write the backend/router in Spring Boot for learning purposes.
- [ ] **Angular**: Angular FrontEnd for learning purposes.
- [ ] **NextJS**: a server component to replace the backend entirely, there will be options. a starter project too various stacks.

# 🚀 QUICK START GUIDE - Fast Lane

## ⚡ 5-Minute Setup

### Step 1: Generate Directory Structure
```bash
cd "c:\Users\Tani\OneDrive\Desktop\Fast Lane"
python folder_structure.py
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
copy .env.example .env
# Edit .env and update SECRET_KEY (optional for dev)
```

### Step 5: Initialize Database
```bash
python -c "from backend.database import init_db, seed_db; init_db(); seed_db()"
```

### Step 6: Run Backend Server
```bash
python backend/main.py
```

**✅ Done!** Server runs at: http://localhost:8000

---

## 📚 API Documentation

Once running, visit these URLs:

| URL | Purpose |
|-----|---------|
| http://localhost:8000/ | API Home |
| http://localhost:8000/docs | Swagger UI (Try API!) |
| http://localhost:8000/redoc | ReDoc (Alternative docs) |
| http://localhost:8000/health | Health Check |
| http://localhost:8000/api/status | API Status |

---

## 🔐 Test Authentication

### 1. Sign Up
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testplayer",
    "email": "test@example.com",
    "password": "TestPass123",
    "password_confirm": "TestPass123"
  }'
```

Response:
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": 1,
    "username": "testplayer",
    "email": "test@example.com"
  }
}
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "testplayer",
    "email": "test@example.com",
    "coins": 0,
    "gems": 0,
    "level_unlocked": 1,
    ...
  }
}
```

### 3. Get Current User Profile
```bash
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer <access_token>"
```

---

## 📁 Project Structure Created

```
Fast Lane/
├── backend/
│   ├── main.py          ─► FastAPI application
│   ├── models.py        ─► Database models (8 tables)
│   ├── schemas.py       ─► Pydantic validation schemas
│   ├── auth.py          ─► JWT & password hashing
│   ├── database.py      ─► DB initialization & seeding
│   └── __init__.py
│
├── config/
│   ├── settings.py      ─► Configuration management
│   └── __init__.py
│
├── frontend/
│   ├── pages/           ─► HTML files (coming next)
│   ├── js/              ─► Phaser.js & game logic (coming next)
│   ├── css/             ─► Tailwind CSS styles (coming next)
│   └── assets/          ─► Images, sounds, sprites
│
├── database/            ─► SQLite database file
├── logs/                ─► Application logs
├── tests/               ─► Test suites
│
├── requirements.txt     ─► Python dependencies
├── .env.example         ─► Environment variables template
├── .env                 ─► Your local config (create from .env.example)
├── .gitignore           ─► Git ignore patterns
├── README.md            ─► Full documentation
├── SETUP_COMPLETE.md    ─► Setup completion checklist
├── ARCHITECTURE.py      ─► Architecture diagrams
├── QUICKSTART.md        ─► This file
└── folder_structure.py  ─► Directory generator
```

---

## 🎮 What's Included

### Database (8 Tables)
✅ Users - Player accounts  
✅ Vehicles - 3 types with 4 upgrades each  
✅ Levels - 15 levels with 4 difficulty tiers  
✅ LevelProgress - User progress tracking  
✅ GameSession - Active game sessions  
✅ Leaderboard - Global rankings  
✅ UpgradePricing - 50+ upgrade tiers  
✅ Achievements - 8 badges  

### Features
✅ JWT Authentication  
✅ Password Hashing (bcrypt)  
✅ User Registration & Login  
✅ Profile Management  
✅ Vehicle System (Jeep, Bike, Truck)  
✅ Level Progression (1-15)  
✅ Upgrade Shop (4 categories)  
✅ Leaderboard Structure  
✅ Achievement System  
✅ Game Session Management  
✅ API Documentation (Swagger)  

---

## 📊 Database Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USERS                               │
├─────────────────────────────────────────────────────────────┤
│ id | username | email | password_hash | coins | gems       │
│ 1  | player1  | p1@.. | bcrypt..      | 1000  | 50         │
└─────────────────────────────────────────────────────────────┘
        ▲                                  ▲
        │ 1:N                              │ 1:1
        │                                  │
┌───────┴──────────────────┐   ┌──────────┴──────────────┐
│        VEHICLES          │   │     LEADERBOARD        │
├──────────────────────────┤   ├────────────────────────┤
│id|user_id|type|upgrades  │   │id|user_id|rank|distance│
│1 │1      │jeep│1,2,0,1   │   │1 │1      │5  │5432.1  │
│2 │1      │bike│0,1,1,0   │   └────────────────────────┘
└──────────────────────────┘
        ▲
        │ 1:N
        │
┌───────┴──────────────────────────────┐
│         GAME_SESSIONS                │
├───────────────────────────────────────┤
│id|user_id|level_id|vehicle_id|distance│
│1 │1      │5      │1         │2345.6  │
└───────────────────────────────────────┘
```

---

## 🛠️ Common Commands

### Virtual Environment
```bash
# Activate
venv\Scripts\activate

# Deactivate
deactivate

# Install packages
pip install <package>

# Export requirements
pip freeze > requirements.txt
```

### Database
```bash
# Initialize DB
python -c "from backend.database import init_db; init_db()"

# Seed with data
python -c "from backend.database import seed_db; seed_db()"

# Drop all tables (WARNING: deletes data!)
python -c "from backend.database import drop_db; drop_db()"
```

### Server
```bash
# Run with auto-reload
uvicorn backend.main:app --reload

# Run on specific port
uvicorn backend.main:app --port 8001

# Run with logging
uvicorn backend.main:app --log-level debug
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test
pytest tests/backend/test_auth.py -v
```

---

## 🔑 Environment Variables

Create `.env` file from `.env.example`:

```env
# App
DEBUG=True
ENVIRONMENT=development

# Server
HOST=127.0.0.1
PORT=8000

# Database
DATABASE_URL=sqlite:///./database/fast_lane.db

# Security (Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn backend.main:app --port 8001
```

### Database Locked
```bash
# Remove and recreate
rm database/fast_lane.db
python -c "from backend.database import init_db, seed_db; init_db(); seed_db()"
```

### Import Errors
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### CORS Errors
Check `config/settings.py` and update `cors_origins` to match your frontend URL.

---

## 📈 Next Steps

### Phase 2: Frontend (HTML/CSS/JS)
- [ ] Landing page
- [ ] Sign-up & Login forms
- [ ] User Dashboard
- [ ] Garage (vehicle selection)
- [ ] Upgrade Shop
- [ ] Level Select Grid
- [ ] Leaderboard
- [ ] Account Settings
- [ ] Help Chatbot

### Phase 3: Game Engine (Phaser.js)
- [ ] Phaser scene setup
- [ ] Matter.js physics
- [ ] Terrain generation (Perlin noise)
- [ ] Vehicle rendering
- [ ] Collision detection
- [ ] UI overlay
- [ ] Game controls

### Phase 4: Integration
- [ ] Connect frontend to backend APIs
- [ ] Real-time leaderboard (WebSocket)
- [ ] Sound effects & music
- [ ] Mobile responsiveness
- [ ] Performance optimization

---

## 📚 API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/signup` | Register user |
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/refresh` | Refresh token |
| GET | `/api/users/me` | Get current user |
| GET | `/api/users/{id}` | Get user by ID |
| GET | `/api/vehicles/` | Get user's vehicles |
| POST | `/api/vehicles/` | Buy vehicle |
| PUT | `/api/vehicles/{id}/upgrade` | Upgrade vehicle |
| GET | `/api/levels/` | Get all levels |
| GET | `/api/levels/{id}` | Get level details |
| GET | `/api/levels/{id}/progress` | Get user progress |
| POST | `/api/games/start` | Start game |
| PUT | `/api/games/{id}` | Update game |
| POST | `/api/games/{id}/end` | End game |
| GET | `/api/leaderboard/` | Get rankings |
| GET | `/api/achievements/` | Get achievements |

---

## 🎯 Project Goals

✅ **Completed:**
- Backend API setup with FastAPI
- Database schema (8 tables)
- Authentication system (JWT)
- User management
- Vehicle system
- Level structure (15 levels)
- Achievement framework
- Configuration management

⏳ **Next:**
- Frontend pages (HTML5 + Tailwind)
- Phaser.js game engine
- Physics implementation (Matter.js)
- API integration
- Testing & optimization

🚀 **Future:**
- Multiplayer racing
- Mobile app
- Advanced analytics
- Social features
- Monetization

---

## 💡 Tips & Best Practices

1. **Always activate virtual environment** before running Python commands
2. **Keep .env file secret**, never commit to git
3. **Test API with Swagger UI** before frontend integration
4. **Use database seeding** for consistent test data
5. **Log important events** for debugging
6. **Update requirements.txt** when adding packages
7. **Run tests** before deployment
8. **Monitor database size** for production

---

## 🆘 Getting Help

1. Check **README.md** for detailed documentation
2. Review **ARCHITECTURE.py** for system design
3. Read **SETUP_COMPLETE.md** for full checklist
4. Visit API docs at http://localhost:8000/docs
5. Check **logs/** directory for error details

---

## 🎉 Ready to Build!

You now have a production-ready backend API! 

**Next: Create the Frontend** 🎨

```bash
# Once API is running:
# 1. Create frontend HTML pages
# 2. Implement Phaser.js game
# 3. Connect to API endpoints
# 4. Test full integration
```

---

**Happy Building! 🏁**

*Fast Lane - Hill Climb Racing Clone*  
*Powered by FastAPI + Phaser.js*

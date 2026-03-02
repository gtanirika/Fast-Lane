# Fast Lane 🏎️ - Hill Climb Racing Clone

A full-stack web application built with **FastAPI** (backend), **Phaser.js** (frontend), and **SQLAlchemy** (database). Players can upgrade vehicles, unlock levels, and compete on global leaderboards.

## Project Overview

**Fast Lane** is a 2D racing game inspired by Hill Climb Racing. Features include:
- ✅ 15 Levels with increasing difficulty
- ✅ 3 Vehicle types (Jeep, Bike, Truck) with 4 upgrade categories
- ✅ 2D Physics Engine (Phaser + Matter.js)
- ✅ In-game Currency System (Coins & Gems)
- ✅ Global Leaderboard Rankings
- ✅ User Authentication (JWT)
- ✅ Vehicle Garage & Upgrade Shop
- ✅ AI Chatbot for Game Help

---

## 📁 Directory Structure

```
Fast Lane/
├── backend/                      # Python FastAPI Backend
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── models.py                 # SQLAlchemy database models
│   ├── schemas.py                # Pydantic validation schemas
│   ├── auth.py                   # JWT authentication & password hashing
│   ├── database.py               # Database connection & session management
│   └── utils.py                  # Helper functions & utilities
│
├── frontend/                     # Frontend Files
│   ├── css/
│   │   └── style.css             # Tailwind CSS + custom styles
│   ├── js/
│   │   ├── game.js               # Phaser.js game engine
│   │   ├── physics.js            # 2D physics implementation
│   │   ├── ui.js                 # UI interactions & canvas updates
│   │   ├── chatbot.js            # AI chatbot logic
│   │   └── utils.js              # Frontend utilities
│   ├── pages/
│   │   ├── index.html            # Landing page (hero section)
│   │   ├── signup.html           # User registration
│   │   ├── login.html            # User login
│   │   ├── dashboard.html        # User dashboard
│   │   ├── garage.html           # Vehicle selection
│   │   ├── upgrade_shop.html     # Upgrade management
│   │   ├── level_select.html     # 15-level grid
│   │   ├── game.html             # Main game screen
│   │   ├── leaderboard.html      # Global rankings
│   │   ├── account_settings.html # Profile management
│   │   └── help.html             # Help & chatbot
│   └── assets/
│       ├── images/               # UI & level images
│       ├── sounds/               # Game audio files
│       ├── vehicles/             # Vehicle sprites
│       └── terrains/             # Terrain textures
│
├── database/                     # Database files
│   └── fast_lane.db              # SQLite DB (or PostgreSQL)
│
├── config/
│   └── settings.py               # Configuration & environment variables
│
├── tests/                        # Test suites
│   ├── backend/                  # Backend tests
│   └── frontend/                 # Frontend tests
│
├── logs/                         # Application logs
│
├── .env                          # Environment variables (secrets)
├── .gitignore                    # Git ignore patterns
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── folder_structure.py           # Directory generator script
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database management
- **SQLite/PostgreSQL** - Database (configurable)
- **Passlib** - Password hashing with bcrypt
- **PyJWT** - JWT token generation & validation
- **Pydantic** - Data validation & serialization

### Frontend
- **HTML5** - Semantic markup
- **CSS3 + Tailwind** - Responsive styling
- **Phaser.js** - 2D Game Engine
- **Matter.js** - 2D Physics Engine
- **Vanilla JavaScript** - Game logic & interactions

### Database Models
1. **User** - Account info, currency, progress
2. **Vehicle** - Vehicle types & upgrade levels
3. **Level** - 15 game levels with terrain data
4. **LevelProgress** - User progress per level
5. **GameSession** - Active game session tracking
6. **Leaderboard** - Global rankings
7. **UpgradePricing** - Upgrade costs & stat bonuses
8. **Achievement** - Achievements & badges

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 14+ (optional, for build tools)
- SQLite or PostgreSQL

### Installation

1. **Clone/Setup Project**
   ```bash
   cd "Fast Lane"
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # MacOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate Directory Structure**
   ```bash
   python folder_structure.py
   ```

5. **Setup Database**
   ```bash
   python -c "from backend.database import init_db; init_db()"
   ```

6. **Create .env File**
   ```
   DATABASE_URL=sqlite:///./database/fast_lane.db
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   DEBUG=True
   ```

7. **Run Backend Server**
   ```bash
   uvicorn backend.main:app --reload
   ```
   Server runs at: `http://localhost:8000`

8. **Open Frontend**
   Open `frontend/pages/index.html` in your browser

---

## 📊 Database Models Overview

### User Model
```python
- id (PK)
- username (unique)
- email (unique)
- password_hash
- coins, gems
- current_level, level_unlocked
- best_distance
- created_at, updated_at
```

### Vehicle Model
```python
- id (PK)
- user_id (FK)
- vehicle_type (jeep/bike/truck)
- engine_level (0-5)
- suspension_level (0-5)
- tires_level (0-5)
- four_wd_level (0-3)
- is_equipped (boolean)
```

### Level Model
```python
- id (PK)
- level_number (1-15)
- name, description
- difficulty (easy/medium/hard/extreme)
- terrain_type (smooth_hill/rocky/ice/water)
- coin_reward, gem_reward
- max_distance
```

---

## 🎮 Game Mechanics

### Physics System
- **Gravity**: 9.8 m/s² (adjustable per level)
- **Terrain**: Procedural smooth hills using Perlin noise
- **Vehicle Weight**: Affects acceleration & fuel consumption
- **Suspension**: Reduces bounce, improves stability

### Upgrade System
| Upgrade | Effect | Max Level |
|---------|--------|-----------|
| Engine | ↑ Torque & Speed | 5 |
| Suspension | ↓ Bounce, ↑ Stability | 5 |
| Tires | ↑ Friction & Control | 5 |
| 4WD | ↑ Off-road traction | 3 |

### Currency
- **Coins**: Earned in levels, used for upgrades
- **Gems**: Premium currency, rarer rewards
- **Conversion**: Some upgrades require both coins & gems

---

## 🔐 Authentication

Uses **JWT (JSON Web Tokens)**:
1. User signs up with username, email, password
2. Password hashed with **bcrypt** (via Passlib)
3. Login returns JWT token with 60-min expiry
4. Token sent in `Authorization: Bearer <token>` header for protected routes

---

## 📝 API Endpoints (FastAPI)

### Auth Routes
- `POST /api/auth/signup` - Register user
- `POST /api/auth/login` - Login & get token
- `POST /api/auth/refresh` - Refresh token

### User Routes
- `GET /api/users/me` - Get current user
- `PUT /api/users/{user_id}` - Update profile
- `GET /api/users/leaderboard` - Get rankings

### Vehicle Routes
- `GET /api/vehicles/` - User's vehicles
- `POST /api/vehicles/` - Create/buy vehicle
- `PUT /api/vehicles/{vehicle_id}/upgrade` - Upgrade vehicle

### Level Routes
- `GET /api/levels/` - All levels
- `GET /api/levels/{level_id}` - Level details
- `GET /api/levels/{level_id}/progress` - User progress

### Game Routes
- `POST /api/games/start` - Start game session
- `PUT /api/games/{session_id}` - Update session
- `POST /api/games/{session_id}/end` - End session

---

## 🎯 Features (Roadmap)

### Phase 1 ✅
- [ ] Backend API setup
- [ ] Database models
- [ ] User authentication (JWT)
- [ ] Vehicle system
- [ ] Level structure (15 levels)

### Phase 2
- [ ] Phaser.js game engine
- [ ] 2D physics (Matter.js)
- [ ] Terrain generation
- [ ] UI rendering
- [ ] Game controls

### Phase 3
- [ ] Upgrade system
- [ ] Leaderboard
- [ ] Achievement system
- [ ] AI chatbot
- [ ] Sound effects

### Phase 4
- [ ] Mobile responsiveness
- [ ] Multiplayer racing
- [ ] Replay system
- [ ] Advanced analytics

---

## 📖 Usage Examples

### Create a User
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "player1",
    "email": "player1@example.com",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "player1@example.com",
    "password": "SecurePass123"
  }'
```

### Get User Profile
```bash
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer <token>"
```

---

## 🐛 Troubleshooting

### Issue: Database not found
**Solution**: Run `python -c "from backend.database import init_db; init_db()"`

### Issue: Port 8000 already in use
**Solution**: Change port: `uvicorn backend.main:app --port 8001`

### Issue: CORS errors in frontend
**Solution**: Ensure CORS is enabled in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📞 Support

For questions or issues, refer to the in-game chatbot or check the Help page.

---

**Happy Racing! 🏁**

"""
Fast Lane - Project Architecture Overview
Visual representation of the system design and component interactions
"""

# =============================================================================
# ARCHITECTURE DIAGRAM
# =============================================================================

"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FAST LANE - ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────┐
│ FRONTEND │  (HTML5 + CSS3 Tailwind + Phaser.js)
└──────────┘
     │
     └─ /pages           - Landing, Login, Dashboard, Garage, Levels, Game
     └─ /js              - Phaser.js game engine, Physics, UI, Chatbot
     └─ /css             - Tailwind CSS styling
     └─ /assets          - Images, Sounds, Sprites, Terrains
     │
     │ (API Calls via Fetch/Axios)
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            REST API (FastAPI)                               │
│                         http://localhost:8000/                              │
│                                                                              │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────────────┐   │
│  │    Auth Routes  │  │   User Routes    │  │    Game Routes          │   │
│  ├─────────────────┤  ├──────────────────┤  ├─────────────────────────┤   │
│  │ POST /signup    │  │ GET /users/me    │  │ POST /games/start       │   │
│  │ POST /login     │  │ GET /users/{id}  │  │ PUT /games/{id}         │   │
│  │ POST /refresh   │  │ PUT /users/{id}  │  │ POST /games/{id}/end    │   │
│  └─────────────────┘  │ DELETE /users/{id}│ └─────────────────────────┘   │
│                       └──────────────────┘                                  │
│                                                                              │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────────────┐   │
│  │ Vehicle Routes  │  │  Level Routes    │  │ Leaderboard Routes      │   │
│  ├─────────────────┤  ├──────────────────┤  ├─────────────────────────┤   │
│  │ GET /vehicles/  │  │ GET /levels/     │  │ GET /leaderboard/       │   │
│  │ POST /vehicles/ │  │ GET /levels/{id} │  │ GET /leaderboard/friends│   │
│  │ PUT /upgrade    │  │ GET /progress    │  │ GET /users/{id}/rank    │   │
│  └─────────────────┘  └──────────────────┘  └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
     ▲
     │ (Database Queries via SQLAlchemy ORM)
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATABASE LAYER (SQLAlchemy)                          │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ MODELS (8 Tables)                                                  │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │                                                                    │    │
│  │  ┌──────────┐  ┌──────────┐  ┌───────┐  ┌──────────────┐        │    │
│  │  │  Users   │  │ Vehicles │  │ Levels│  │LevelProgress │        │    │
│  │  ├──────────┤  ├──────────┤  ├───────┤  ├──────────────┤        │    │
│  │  │ id (PK)  │  │ id (PK)  │  │id.PK  │  │ id (PK)      │        │    │
│  │  │ username │  │user_id   │  │num    │  │user_id       │        │    │
│  │  │ email    │  │type      │  │name   │  │level_id      │        │    │
│  │  │ password │  │4 upgrades│  │dif    │  │unlocked      │        │    │
│  │  │ coins    │  │stats     │  │reward │  │completed     │        │    │
│  │  │ gems     │  │equipped  │  │...    │  │best_distance │        │    │
│  │  │ level    │  │...       │  │       │  │stars         │        │    │
│  │  └──────────┘  └──────────┘  └───────┘  └──────────────┘        │    │
│  │       ▲             ▲            ▲              ▲                 │    │
│  │       │             │            │              │                 │    │
│  │  ┌────────┐  ┌─────────────┐  ┌──────────┐  ┌────────────────┐  │    │
│  │  │ Leader │  │GameSession  │  │Upgrade   │  │Achievement     │  │    │
│  │  │ board  │  │             │  │Pricing   │  │                │  │    │
│  │  ├────────┤  ├─────────────┤  ├──────────┤  ├────────────────┤  │    │
│  │  │rank    │  │distance     │  │type      │  │name            │  │    │
│  │  │total_* │  │coins,gems   │  │level     │  │criteria        │  │    │
│  │  │streak  │  │fuel_used    │  │cost      │  │reward          │  │    │
│  │  │...     │  │time_elapsed │  │bonus     │  │...             │  │    │
│  │  └────────┘  │crashed      │  └──────────┘  └────────────────┘  │    │
│  │              │out_of_fuel  │                                    │    │
│  │              └─────────────┘                                    │    │
│  │                                                                  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ SUPPORTED DATABASES:                                               │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │ • SQLite (Development)  →  /database/fast_lane.db                 │    │
│  │ • PostgreSQL (Production) → postgresql://user:pass@host/db        │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│                        AUTHENTICATION FLOW                                    │
└──────────────────────────────────────────────────────────────────────────────┘

1. USER SIGNUP
   ┌──────────────┐
   │ Client       │
   └──────────────┘
         │
         │ POST /auth/signup
         │ {username, email, password}
         │
         ▼
   ┌──────────────────────────────────┐
   │ Backend: auth.py                 │
   ├──────────────────────────────────┤
   │ • Validate input (Pydantic)      │
   │ • Hash password (bcrypt)         │
   │ • Check duplicate user           │
   │ • Save User to database          │
   └──────────────────────────────────┘
         │
         │ ✅ Success / ❌ Error
         │
         ▼
   ┌──────────────┐
   │ Response:    │
   │ {success,    │
   │  user_id}    │
   └──────────────┘

2. USER LOGIN
   ┌──────────────┐
   │ Client       │
   └──────────────┘
         │
         │ POST /auth/login
         │ {email, password}
         │
         ▼
   ┌──────────────────────────────────┐
   │ Backend: auth.py                 │
   ├──────────────────────────────────┤
   │ • Find user by email             │
   │ • Verify password (bcrypt)       │
   │ • Create JWT token               │
   │   - Payload: {user_id, username} │
   │   - Expiry: 60 minutes           │
   │   - Algorithm: HS256             │
   └──────────────────────────────────┘
         │
         │
         ▼
   ┌──────────────────────┐
   │ Response:            │
   │ {access_token,       │
   │  token_type: bearer, │
   │  expires_in: 3600}   │
   └──────────────────────┘

3. PROTECTED ENDPOINT ACCESS
   ┌──────────────┐
   │ Client       │
   └──────────────┘
         │
         │ GET /api/users/me
         │ Header: Authorization: Bearer <token>
         │
         ▼
   ┌──────────────────────────────────┐
   │ Backend: auth.py                 │
   ├──────────────────────────────────┤
   │ • Extract token from header      │
   │ • Decode JWT                     │
   │ • Verify signature (SECRET_KEY)  │
   │ • Check expiration               │
   │ • Get user_id from payload       │
   │ • Fetch user from database       │
   │ • Inject user into route         │
   └──────────────────────────────────┘
         │
         │ ✅ Valid / ❌ Invalid/Expired
         │
         ▼
   ┌──────────────────┐
   │ Response:        │
   │ User profile or  │
   │ 401 Unauthorized │
   └──────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│                      GAME STATE MANAGEMENT FLOW                              │
└──────────────────────────────────────────────────────────────────────────────┘

PLAYER JOURNEY:
┌─────────┐
│ Landing │ ──────┬─────────────────────────────────────────────────────┐
│ Page    │       │                                                     │
└─────────┘       │                                                     │
                  │                                                     │
         ┌────────▼─────────┐                                          │
         │ LOGIN / SIGNUP   │                                          │
         └────────┬─────────┘                                          │
                  │                                                     │
         ┌────────▼──────────┐                                         │
         │ DASHBOARD         │ ◄────────────────────────────────────┐  │
         │ View: Coins/Gems  │                                     │  │
         │        Level      │                                     │  │
         │        Best Dist  │                                     │  │
         └────┬───────────┬──┘                                     │  │
              │           │                                        │  │
       ┌──────▼──┐    ┌──▼────┐                                   │  │
       │ GARAGE  │    │ LEVELS │                                  │  │
       │ Select  │    │ Grid   │                                  │  │
       │ Vehicle │    │ 1-15   │                                  │  │
       └──┬──────┘    └──┬─────┘                                  │  │
          │              │                                        │  │
    ┌─────▼────┐    ┌────▼──────┐                                │  │
    │ UPGRADE  │    │ GAME START │                               │  │
    │ SHOP     │    │ Level Load │                               │  │
    │ Upgrades │    │ Vehicle    │                               │  │
    └─────┬────┘    │ Setup      │                               │  │
          │         └────┬───────┘                               │  │
          │              │                                       │  │
          │         ┌─────▼────────────────────────────────┐    │  │
          │         │ GAME SCREEN                          │    │  │
          │         │ ┌──────────────────────────────────┐ │    │  │
          │         │ │ Phaser.js Canvas                │ │    │  │
          │         │ │ • Terrain (Perlin noise)        │ │    │  │
          │         │ │ • Vehicle (Car + 2 wheels)      │ │    │  │
          │         │ │ • Physics (Matter.js)           │ │    │  │
          │         │ │ • Obstacles                     │ │    │  │
          │         │ │ • Coins/Gems scattered         │ │    │  │
          │         │ └──────────────────────────────────┘ │    │  │
          │         │ UI Overlay:                          │    │  │
          │         │ • Distance traveled                  │    │  │
          │         │ • Coins collected                    │    │  │
          │         │ • Fuel remaining                     │    │  │
          │         │ • Time elapsed                       │    │  │
          │         │ • Speed indicator                    │    │  │
          │         └─────┬────────────────────────────────┘    │  │
          │              │                                      │  │
          │         ┌─────▼────────────┐                        │  │
          │         │ GAME END         │                        │  │
          │         │ • Distance: XXXX │                        │  │
          │         │ • Coins: XXX     │                        │  │
          │         │ • Stars: 3       │                        │  │
          │         │ • Time: XX sec   │                        │  │
          │         └─────┬────────────┘                        │  │
          │              │                                      │  │
          │         ┌─────▼────────────┐                        │  │
          │         │ SAVE TO DATABASE │                        │  │
          │    ┌────┤ • Update coins   │                        │  │
          │    │    │ • Update level  │                        │  │
          │    │    │ • Save progress  │                        │  │
          │    │    │ • Update stats   │                        │  │
          │    │    └─────┬────────────┘                        │  │
          │    │         │                                      │  │
          │    │    ┌────▼──────────────────────────────────┐  │  │
          └────┼────┤ PLAY AGAIN or DASHBOARD              │  │  │
               │    │                                       │  │  │
               │    └────────────────────────────────────────┘  │  │
               │                                               │  │
               └───────────────────────────────────────────────┘  │
                                                                   │
                   ┌──────────────────────────────────────────────┘
                   │
         ┌─────────▼──────────┐
         │ LEADERBOARD        │
         │ View global ranks  │
         │ View friend ranks  │
         │ Check achievements │
         └────────┬───────────┘
                  │
                  └───► Back to Dashboard


┌──────────────────────────────────────────────────────────────────────────────┐
│                        DEPENDENCY INJECTION (FastAPI)                        │
└──────────────────────────────────────────────────────────────────────────────┘

Every route has dependencies automatically injected:

@app.get("/api/data")
def get_data(
    current_user: User = Depends(get_current_user),  ◄── Validates JWT, Gets User
    db: Session = Depends(get_db)                     ◄── Database session
):
    # current_user and db are automatically provided
    return {"user": current_user, "data": db.query(...).all()}


┌──────────────────────────────────────────────────────────────────────────────┐
│                            FILE ORGANIZATION                                 │
└──────────────────────────────────────────────────────────────────────────────┘

backend/
├── main.py
│   └── FastAPI app setup, routes, middleware
│
├── models.py
│   └── SQLAlchemy ORM models (tables)
│
├── schemas.py
│   └── Pydantic request/response validation
│
├── auth.py
│   ├── hash_password()          ◄── Bcrypt hashing
│   ├── verify_password()        ◄── Password checking
│   ├── TokenManager             ◄── JWT creation/validation
│   ├── get_current_user()       ◄── Dependency injection
│   └── authenticate_user()      ◄── Login logic
│
└── database.py
    ├── engine                   ◄── SQLAlchemy connection
    ├── SessionLocal             ◄── Database session factory
    ├── get_db()                 ◄── FastAPI dependency
    ├── init_db()                ◄── Create all tables
    ├── seed_db()                ◄── Load initial data
    └── drop_db()                ◄── Delete all tables

config/
├── settings.py
│   ├── Development settings     ◄── DEBUG=True
│   ├── Production settings      ◄── DEBUG=False, strict CORS
│   ├── Testing settings         ◄── SQLite test DB
│   └── validate_settings()      ◄── Security checks


┌──────────────────────────────────────────────────────────────────────────────┐
│                       DATA FLOW EXAMPLE: User Signup                        │
└──────────────────────────────────────────────────────────────────────────────┘

Client                          Backend                         Database
  │                               │                                  │
  │─────── POST /signup ────────► │                                  │
  │   {username,email,password}   │                                  │
  │                               │                                  │
  │                        ┌──────▼────────────┐                    │
  │                        │ Validate input    │                    │
  │                        │ (Pydantic)        │                    │
  │                        └──────┬────────────┘                    │
  │                               │                                  │
  │                        ┌──────▼────────────┐                    │
  │                        │ Hash password     │                    │
  │                        │ (bcrypt)          │                    │
  │                        └──────┬────────────┘                    │
  │                               │                                  │
  │                        ┌──────▼─────────────────────────────┐   │
  │                        │ Check if user exists              │   │
  │                        │ Query: User.email == email        │   │
  │                        └──────┬──────────────────────────────┘  │
  │                               │                                  │
  │                               │─── SELECT * FROM users ────────► │
  │                               │◄────── No results ──────────────│
  │                               │                                  │
  │                        ┌──────▼──────────────┐                  │
  │                        │ Create User object  │                  │
  │                        │ password_hash=XXX   │                  │
  │                        └──────┬──────────────┘                  │
  │                               │                                  │
  │                               │─── INSERT INTO users ──────────► │
  │                               │◄──── ID: 123 ──────────────────│
  │                               │                                  │
  │                        ┌──────▼──────────────┐                  │
  │                        │ Prepare response   │                  │
  │                        │ {success: true,    │                  │
  │                        │  user_id: 123}     │                  │
  │                        └──────┬──────────────┘                  │
  │                               │                                  │
  │◄────── 201 Created ────────── │                                  │
  │   {success,user_id}           │                                  │
  │                               │                                  │


=============================================================================
KEY FEATURES IMPLEMENTED
=============================================================================

✅ 8 Database Models
✅ 20+ Pydantic Schemas 
✅ JWT Authentication
✅ Password Hashing (bcrypt)
✅ Role-based Access Control (ready)
✅ CORS Middleware
✅ Exception Handling
✅ Environment Configuration
✅ Database Initialization
✅ Data Seeding (15 levels + upgrades)
✅ Logging Setup
✅ API Documentation (Swagger UI)
✅ Health Check Endpoints
✅ User Management
✅ Vehicle System
✅ Level Progression
✅ Leaderboard Structure
✅ Achievement System
✅ Upgrade Pricing
✅ Game Session Management

=============================================================================
READY FOR PHASE 2: FRONTEND DEVELOPMENT
=============================================================================
"""

# This is a comprehensive overview document of the architecture
# Keep this as reference while developing the frontend and game engine

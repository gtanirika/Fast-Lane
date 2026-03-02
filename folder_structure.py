"""
Fast Lane - Hill Climb Racing Clone
Directory Structure Generator
"""

import os
from pathlib import Path


def create_directory_structure(base_path):
    """Create the full project directory structure."""
    
    base = Path(base_path)
    base.mkdir(parents=True, exist_ok=True)
    
    # Define all directories to create
    directories = [
        # Backend
        "backend",
        
        # Frontend
        "frontend",
        "frontend/assets",
        "frontend/assets/images",
        "frontend/assets/sounds",
        "frontend/assets/vehicles",
        "frontend/assets/terrains",
        "frontend/js",
        "frontend/pages",
        "frontend/css",
        
        # Database
        "database",
        
        # Config
        "config",
        
        # Logs
        "logs",
        
        # Tests
        "tests",
        "tests/backend",
        "tests/frontend",
    ]
    
    # Create all directories
    for directory in directories:
        dir_path = base / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_path}")
    
    # Create __init__.py files for Python packages
    init_files = [
        "backend/__init__.py",
        "tests/__init__.py",
        "tests/backend/__init__.py",
    ]
    
    for init_file in init_files:
        file_path = base / init_file
        file_path.touch()
        print(f"✓ Created: {file_path}")
    
    print("\n" + "="*60)
    print("✓ Directory Structure Created Successfully!")
    print("="*60)
    
    # Print folder tree
    print("\nProject Structure:")
    print("""
Fast Lane/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── database.py
│   └── utils.py
├── frontend/
│   ├── assets/
│   │   ├── images/
│   │   ├── sounds/
│   │   ├── vehicles/
│   │   └── terrains/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── game.js
│   │   ├── physics.js
│   │   ├── ui.js
│   │   ├── chatbot.js
│   │   └── utils.js
│   └── pages/
│       ├── index.html
│       ├── signup.html
│       ├── login.html
│       ├── dashboard.html
│       ├── garage.html
│       ├── upgrade_shop.html
│       ├── level_select.html
│       ├── game.html
│       ├── leaderboard.html
│       ├── account_settings.html
│       └── help.html
├── database/
├── config/
│   └── settings.py
├── tests/
│   ├── __init__.py
│   ├── backend/
│   │   └── __init__.py
│   └── frontend/
├── logs/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── folder_structure.py
    """)


if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    create_directory_structure(base_path)

# Project Structure

This document describes the organized structure of the Telegram Web Application project.

## Directory Structure

```
telegram/
├── app.py                 # Main FastAPI application
├── index.html            # Web interface
├── requirements.txt      # Python dependencies
├── env.example           # Environment variables template
├── README.md             # Main project documentation
├── .gitignore           # Git ignore rules
│
├── docs/                 # All documentation files
│   ├── API_DOCUMENTATION.md
│   ├── AUTHENTICATION_GUIDE.md
│   ├── QUICK_START.md
│   └── ... (all other .md files)
│
├── scripts/              # Utility and setup scripts
│   ├── auth_cli.py       # CLI authentication script
│   ├── start_app.ps1     # PowerShell startup script
│   ├── start_app.sh      # Bash startup script
│   ├── test_telegram_mcp_setup.py
│   └── ... (other utility scripts)
│
├── data/                 # Data files (session files, etc.)
│   ├── .gitkeep         # Keep directory in git
│   └── *.session        # Telegram session files (gitignored)
│
├── logs/                 # Log files
│   ├── .gitkeep         # Keep directory in git
│   └── *.log            # Application logs (gitignored)
│
├── Apis-Telegram/        # API-related code
│   ├── Apis.py
│   └── README.md
│
└── venv/                 # Python virtual environment (gitignored)
```

## Key Changes

### File Organization
- **Documentation**: All `.md` files (except `README.md`) moved to `docs/`
- **Scripts**: All utility scripts (`.py`, `.ps1`, `.sh`) moved to `scripts/`
- **Session Files**: Telegram session files stored in `data/` directory
- **Logs**: All log files stored in `logs/` directory

### Code Updates
- `app.py`: Updated to store session files in `data/` directory
- `scripts/auth_cli.py`: Updated to store session files in `data/` directory
- `scripts/test-telegram-mcp-setup.ps1`: Updated to reference scripts in `scripts/` folder

### Running the Application

**Authentication:**
```bash
python scripts/auth_cli.py
```

**Start the app:**
```bash
# Windows (PowerShell)
.\scripts\start_app.ps1

# Linux/Mac (Bash)
./scripts/start_app.sh

# Or directly
python app.py
```

## Notes

- Session files and logs are automatically created in their respective directories
- The `data/` and `logs/` directories are gitignored but kept in the repository via `.gitkeep` files
- All documentation is now centralized in the `docs/` folder for easier navigation

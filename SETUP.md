# Setup

## Requirements
- Python 3.9+
- pip

## Clone Repository
```bash
git clone https://github.com/garyohosu/virtual-company.git
cd virtual-company
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Create .env File
```bash
DATABASE_URL=sqlite:///./magicboxai.db
SECRET_KEY=your-secret-key-here
```

## Initialize Database
```bash
python -m scripts.init_db
```

## Run Tests
```bash
python -m pytest
```

## Start Server
```bash
python -m magicboxai.main
```

## Local Smoke Test
```bash
curl http://localhost:8000/api/check-limit
```

## Notes
- If `scripts.init_db` or `magicboxai.main` do not exist in your checkout, skip those steps and follow the active project documentation under `magicboxai_*`.

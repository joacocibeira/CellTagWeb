# CellTagWeb 🧬

A responsive Streamlit web app for tagging biological images with custom labels.

- ✅ User authentication (SQLite)
- ✅ Fast classification via dropdown or buttons
- ✅ Image rotation using Redis (only untagged images shown)
- ✅ Per-user tagging history stored as JSON
- ✅ Fully Dockerized with Redis & volume persistence


## 🚀 Installation & Setup

### 1. Clone the repo

```bash
git clone git@github.com:joacocibeira/CellTagWeb.git
cd celltagweb
```

### 2.  Set up environment variables

```bash
cp .env.template .env
```

### 3.  Create data folder

```bash
mkdir -p data/images
mkdir -p data/auth
```
This folder will contain the images and output

### 4. Create users

```bash
poetry run create-user alice secret123
```

### 5. Run with Docker Compose

```bash
docker-compose up --build -d
```



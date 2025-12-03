# ⚡ Quick Start Guide

Get the Network Monitor Portal running in 5 minutes!

## 🐳 Option 1: Docker (Recommended)

The fastest way to get started:

```bash
# Clone repository
git clone https://github.com/fmspathankot-spec/network-monitor-portal.git
cd network-monitor-portal

# Create .env file
echo "DB_PASSWORD=mysecurepassword" > .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

# Start all services
docker-compose up -d

# Wait for services to start (30 seconds)
sleep 30

# Check status
docker-compose ps
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Database: localhost:5432

**Stop services:**
```bash
docker-compose down
```

## 💻 Option 2: Manual Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+

### Backend Setup (5 steps)

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
createdb network_monitor

# 5. Configure and run
cp .env.example .env
# Edit .env with your database credentials
uvicorn main:app --reload
```

### Frontend Setup (3 steps)

```bash
# 1. Navigate to frontend (new terminal)
cd frontend

# 2. Install dependencies
npm install

# 3. Configure and run
cp .env.example .env.local
npm run dev
```

## 🎯 First Steps

### 1. Register Account
1. Go to http://localhost:3000/register
2. Create your account

### 2. Add Router
1. Login to dashboard
2. Fill in router details:
   - **Name:** My Router
   - **Host:** 192.168.1.1
   - **Username:** admin
   - **Password:** your_router_password
   - **Device Type:** cisco_ios
3. Click "Add Router"

### 3. Monitor
- View real-time interface status
- Check BGP neighbors
- Monitor OSPF neighbors
- Receive alerts for issues

## 🔧 Common Issues

### Port Already in Use
```bash
# Kill process on port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process on port 3000
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql
```

### Module Not Found
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📚 Next Steps

- [Full Setup Guide](docs/SETUP_GUIDE.md)
- [API Documentation](http://localhost:8000/docs)
- [Architecture Overview](docs/ARCHITECTURE.md)

## 💬 Need Help?

- **Issues:** [GitHub Issues](https://github.com/fmspathankot-spec/network-monitor-portal/issues)
- **Email:** fmspathankot@gmail.com

---

**Happy Monitoring! 🚀**

# 🚀 Complete Setup Guide

This guide will walk you through setting up the Network Monitor Portal from scratch.

## 📋 Prerequisites

### Required Software
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 13+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads/)

### Optional Tools
- **pgAdmin** - PostgreSQL GUI
- **Postman** - API testing
- **VS Code** - Recommended IDE

## 🗄️ Database Setup

### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:**
Download and install from [PostgreSQL website](https://www.postgresql.org/download/windows/)

### 2. Create Database

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE network_monitor;
CREATE USER netmon_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE network_monitor TO netmon_user;
\q
```

### 3. Verify Connection

```bash
psql -U netmon_user -d network_monitor -h localhost
# Enter password when prompted
# If successful, you'll see: network_monitor=>
\q
```

## 🐍 Backend Setup

### 1. Clone Repository

```bash
git clone https://github.com/fmspathankot-spec/network-monitor-portal.git
cd network-monitor-portal
```

### 2. Setup Python Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify activation (should show venv path)
which python
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

Update `.env` with your settings:
```env
DATABASE_URL=postgresql://netmon_user:your_secure_password@localhost:5432/network_monitor
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
```

### 5. Initialize Database

```bash
# Create tables
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"

# Verify tables created
psql -U netmon_user -d network_monitor -c "\dt"
```

### 6. Start Backend Server

```bash
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 7. Test API

Open browser: `http://localhost:8000/docs`

You should see the Swagger UI with all API endpoints.

## ⚛️ Frontend Setup

### 1. Navigate to Frontend

```bash
# Open new terminal
cd network-monitor-portal/frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

Update `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### 4. Start Development Server

```bash
npm run dev
```

You should see:
```
  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

### 5. Access Application

Open browser: `http://localhost:3000`

## 🧪 Testing the Application

### 1. Register a User

1. Go to `http://localhost:3000/register`
2. Fill in:
   - Email: `test@example.com`
   - Username: `testuser`
   - Password: `Test123!@#`
3. Click "Register"

### 2. Login

1. Go to `http://localhost:3000/login`
2. Enter credentials
3. You should be redirected to dashboard

### 3. Add a Router

1. In dashboard, fill router form:
   - Name: `Test Router`
   - Host: `192.168.1.1` (your router IP)
   - Username: `admin`
   - Password: `your_router_password`
   - Device Type: `cisco_ios`
2. Click "Add Router"

### 4. Monitor Router

The system will automatically:
- Connect to router via SSH
- Fetch interface status
- Monitor BGP/OSPF neighbors
- Display real-time updates
- Create alerts for issues

## 🔧 Troubleshooting

### Database Connection Issues

**Error:** `could not connect to server`

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql

# Check connection
psql -U netmon_user -d network_monitor -h localhost
```

### Backend Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Build Errors

**Error:** `Module not found: Can't resolve '@/lib/api'`

**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Restart dev server
npm run dev
```

### SSH Connection Failures

**Error:** `Authentication failed` or `Connection timeout`

**Solutions:**
1. Verify router IP is reachable:
   ```bash
   ping 192.168.1.1
   ```

2. Test SSH manually:
   ```bash
   ssh admin@192.168.1.1
   ```

3. Check router SSH configuration:
   ```
   # On router
   show ip ssh
   show running-config | include ssh
   ```

4. Enable SSH on router (if needed):
   ```
   configure terminal
   hostname Router1
   ip domain-name example.com
   crypto key generate rsa modulus 2048
   ip ssh version 2
   line vty 0 4
   transport input ssh
   login local
   exit
   ```

### WebSocket Connection Issues

**Error:** `WebSocket connection failed`

**Solution:**
1. Check if backend is running
2. Verify WebSocket URL in `.env.local`
3. Check browser console for errors
4. Ensure JWT token is valid

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows
```

## 🔐 Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use strong database password
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Encrypt router passwords in database
- [ ] Set up rate limiting
- [ ] Enable CORS only for trusted origins
- [ ] Use environment variables for all secrets
- [ ] Set up database backups
- [ ] Enable audit logging

## 📊 Monitoring

### Check Application Health

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
psql -U netmon_user -d network_monitor -c "SELECT COUNT(*) FROM users;"
```

### View Logs

```bash
# Backend logs (if running with uvicorn)
tail -f uvicorn.log

# Database logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

## 🚀 Next Steps

1. **Add More Routers** - Configure multiple routers for monitoring
2. **Customize Alerts** - Set up email/SMS notifications
3. **Create Dashboards** - Build custom views for your network
4. **Set Up Backups** - Configure automated database backups
5. **Deploy to Production** - See [DEPLOYMENT.md](DEPLOYMENT.md)

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Netmiko Documentation](https://github.com/ktbyers/netmiko)

## 💬 Getting Help

- **Issues:** [GitHub Issues](https://github.com/fmspathankot-spec/network-monitor-portal/issues)
- **Email:** fmspathankot@gmail.com
- **Documentation:** [Project Wiki](https://github.com/fmspathankot-spec/network-monitor-portal/wiki)

---

**Happy Monitoring! 🎉**

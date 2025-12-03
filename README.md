# 🌐 Network Monitor Portal

A comprehensive full-stack web application for monitoring network routers in real-time. Track interface status, WAN links, BGP neighbors, OSPF neighbors, and Layer 2 services with live updates, alerts, and historical analytics.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-16-black.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)

## ✨ Features

### 🔐 Authentication & Security
- JWT-based authentication
- Secure password hashing with bcrypt
- Role-based access control
- Protected API endpoints

### 📊 Real-Time Monitoring
- Live router status updates via WebSockets
- Interface status tracking (up/down)
- WAN link monitoring
- BGP neighbor status
- OSPF neighbor tracking
- Layer 2 services monitoring

### 🚨 Intelligent Alerts
- Automatic alert generation for:
  - Interface failures
  - BGP session drops
  - OSPF neighbor issues
- Real-time notifications via WebSocket
- Alert history and resolution tracking
- Severity levels (info, warning, critical)

### 📈 Analytics & Visualization
- Historical metrics storage
- Interactive charts with Recharts
- 24-hour trend analysis
- CPU and memory usage tracking
- Interface availability statistics
- BGP/OSPF neighbor trends

### 🗄️ Database Management
- PostgreSQL for data persistence
- Router configuration storage
- Time-series metrics
- Alert history
- User management

### 🎨 Modern UI/UX
- Next.js 16 with App Router
- Server Components for performance
- React Query for data management
- React Hook Form with Zod validation
- Tailwind CSS for styling
- Responsive design

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Next.js 16    │ ◄─────► │   FastAPI        │ ◄─────► │  PostgreSQL │
│   Frontend      │  REST   │   Backend        │  SQL    │  Database   │
│                 │ WebSocket│                  │         │             │
└─────────────────┘         └──────────────────┘         └─────────────┘
                                     │
                                     │ SSH
                                     ▼
                            ┌─────────────────┐
                            │  Network Routers│
                            │  (Cisco/Juniper)│
                            └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Git

### Backend Setup

```bash
# Clone repository
git clone https://github.com/fmspathankot-spec/network-monitor-portal.git
cd network-monitor-portal/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your database credentials

# Create database
createdb network_monitor

# Run migrations (if using Alembic)
alembic upgrade head

# Start server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env.local
# Edit .env.local with your API URL

# Start development server
npm run dev
```

Visit: `http://localhost:3000`

## 📁 Project Structure

```
network-monitor-portal/
├── backend/
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection
│   ├── requirements.txt        # Python dependencies
│   ├── auth/
│   │   ├── jwt_handler.py      # JWT token management
│   │   ├── hash_password.py    # Password hashing
│   │   └── dependencies.py     # Auth dependencies
│   ├── models/
│   │   ├── database_models.py  # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   ├── routers/
│   │   ├── auth.py             # Authentication routes
│   │   ├── routers.py          # Router management
│   │   ├── network.py          # Network monitoring
│   │   ├── metrics.py          # Metrics endpoints
│   │   └── websocket.py        # WebSocket handler
│   └── services/
│       ├── ssh_service.py      # SSH connection service
│       ├── alert_service.py    # Alert management
│       ├── monitoring_service.py # Background monitoring
│       └── websocket_manager.py  # WebSocket manager
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── login/
│   │   │   └── page.tsx        # Login page
│   │   ├── register/
│   │   │   └── page.tsx        # Registration page
│   │   └── dashboard/
│   │       └── page.tsx        # Main dashboard
│   ├── components/
│   │   ├── RouterForm.tsx      # Router connection form
│   │   ├── RouterStatus.tsx    # Status display
│   │   ├── MetricsChart.tsx    # Analytics charts
│   │   ├── AlertToast.tsx      # Alert notifications
│   │   └── StatusCard.tsx      # Status cards
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   ├── auth-context.tsx    # Auth context
│   │   ├── queryClient.ts      # React Query setup
│   │   └── use-websocket.ts    # WebSocket hook
│   └── types/
│       └── router.ts           # TypeScript types
│
└── docs/
    ├── API.md                  # API documentation
    ├── DEPLOYMENT.md           # Deployment guide
    └── ARCHITECTURE.md         # Architecture details
```

## 🔧 Configuration

### Backend Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/network_monitor

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Monitoring
ALERT_CHECK_INTERVAL=60
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

#### Router Management
- `POST /api/routers/` - Add new router
- `GET /api/routers/` - List all routers
- `GET /api/routers/{id}` - Get router details
- `PUT /api/routers/{id}` - Update router
- `DELETE /api/routers/{id}` - Delete router

#### Monitoring
- `POST /api/network/router/status` - Get live router status
- `POST /api/network/router/execute` - Execute custom command

#### Metrics
- `GET /api/metrics/router/{id}` - Get historical metrics
- `GET /api/metrics/router/{id}/summary` - Get summary stats

#### WebSocket
- `WS /ws/{token}` - Real-time updates

## 🎯 Usage Examples

### Adding a Router

```typescript
const response = await fetch('http://localhost:8000/api/routers/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Core Router 1',
    host: '192.168.1.1',
    username: 'admin',
    password: 'secure_password',
    device_type: 'cisco_ios',
    location: 'Data Center A'
  })
});
```

### Monitoring Router Status

```python
from services.ssh_service import RouterSSHService

ssh = RouterSSHService(
    host='192.168.1.1',
    username='admin',
    password='password',
    device_type='cisco_ios'
)

if ssh.connect():
    interfaces = ssh.get_interface_status()
    bgp_neighbors = ssh.get_bgp_summary()
    ospf_neighbors = ssh.get_ospf_neighbors()
    ssh.disconnect()
```

## 🔒 Security Best Practices

1. **Never commit sensitive data**
   - Use `.env` files for secrets
   - Add `.env` to `.gitignore`

2. **Use strong SECRET_KEY**
   - Generate with: `openssl rand -hex 32`

3. **Enable HTTPS in production**
   - Use SSL certificates
   - Configure CORS properly

4. **Encrypt router passwords**
   - Use Fernet encryption for stored passwords
   - Never log passwords

5. **Regular security updates**
   - Keep dependencies updated
   - Monitor security advisories

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Manual Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions on:
- AWS deployment
- DigitalOcean deployment
- Heroku deployment
- Railway deployment

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [Netmiko](https://github.com/ktbyers/netmiko) - Network device SSH library
- [React Query](https://tanstack.com/query) - Data fetching library
- [Recharts](https://recharts.org/) - Charting library

## 📧 Support

For support, email fmspathankot@gmail.com or open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Multi-vendor support (Juniper, Arista, etc.)
- [ ] Email/SMS alert notifications
- [ ] Custom dashboard widgets
- [ ] API rate limiting
- [ ] Audit logging
- [ ] Multi-tenancy support
- [ ] Mobile app (React Native)
- [ ] Network topology visualization
- [ ] Configuration backup/restore
- [ ] Compliance reporting

---

**Built with ❤️ for network engineers**
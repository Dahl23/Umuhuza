# ⚡ Umuhuza Platform - Quick Start Guide

## 🚀 Start the Platform

### **For Development (Recommended):**
```bash
./dev.sh
```
Opens servers in **separate windows** - see live output, errors, and **verification codes**! ⭐

### **For Background Mode:**
```bash
./start.sh
```
Runs quietly in background - use `./logs.sh` to view output.

---

## 🎯 Essential Commands

| Command | Description |
|---------|-------------|
| `./dev.sh` | 🔧 Dev mode - see live output! ⭐ |
| `./start.sh` | 🚀 Start in background |
| `./logs.sh` | 📝 View logs (backend/frontend/both) |
| `./stop.sh` | 🛑 Stop all servers |
| `./status.sh` | 📊 Check server status |

---

## 🌐 Access the Platform

| Service | URL |
|---------|-----|
| **Main App** | http://localhost:5173 |
| **API** | http://localhost:8000/api |
| **Admin** | http://localhost:8000/admin |

---

## 📝 View Logs & Verification Codes

### **See Live Output:**
```bash
./logs.sh           # View both logs
./logs.sh backend   # Backend only
./logs.sh frontend  # Frontend only
```

### **Find Verification Codes:**
```bash
grep -i "verification" backend.log
tail -f backend.log | grep "code"
```

### **See Errors:**
```bash
tail -f backend.log | grep -i "error"
```

**💡 Tip:** Use `./dev.sh` to see everything live in separate windows!

📚 **Full guide:** See `VIEW_LOGS.md` for all options

---

## 🔧 First Time Setup

Only needed once:

```bash
# 1. Create virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# 2. Install frontend dependencies
cd frontend
npm install
cd ..

# 3. Setup pricing plans
cd backend
source venv/bin/activate
python manage.py setup_pricing_plans
cd ..

# 4. Start servers
./start.sh
```

---

## 🆘 Troubleshooting

### Servers won't start?

```bash
# Stop everything
./stop.sh

# Check status
./status.sh

# Try again
./start.sh
```

### Port already in use?

```bash
./stop.sh
# Then start again
./start.sh
```

### Check logs for errors:

```bash
cat backend.log
cat frontend.log
```

---

## 📚 More Info

- See **SERVER_SCRIPTS.md** for detailed documentation
- See **README.md** for project documentation

---

**Ready to develop? Run `./start.sh` and open http://localhost:5173** 🎉

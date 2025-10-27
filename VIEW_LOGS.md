# 📝 Viewing Server Logs & Verification Codes

## 🎯 Problem: Can't See Verification Codes?

When you run `./start.sh`, servers run in the **background** and output goes to log files.
This means you can't see:
- ✉️ **Verification codes** (email/phone)
- ❌ **Error messages**
- 📊 **Debug information**
- 🔍 **API requests**

Here are **3 ways** to see this output:

---

## ⭐ **Option 1: Dev Mode (RECOMMENDED for Development)**

### Opens servers in separate terminal windows with LIVE output!

```bash
./dev.sh
```

**What happens:**
- 🪟 Opens **2 new terminal windows**
  - One for Backend (Django)
  - One for Frontend (React)
- 📺 **Live output** in each window
- ✉️ **Verification codes appear directly** in the backend window
- ❌ **Errors are immediately visible**

**Perfect for:**
- 🔬 Active development
- 🐛 Debugging issues
- 📧 Testing email/phone verification
- 👀 Watching real-time logs

**To stop:**
- Press `Ctrl+C` in each terminal window
- Or run `./stop.sh`

---

## 📊 **Option 2: View Log Files (For Background Mode)**

If you used `./start.sh` (background mode), logs are saved to files:

### **Quick View - Both Logs:**
```bash
./logs.sh
```

### **Backend Logs Only:**
```bash
./logs.sh backend
```

### **Frontend Logs Only:**
```bash
./logs.sh frontend
```

### **Manual Methods:**

**Follow backend logs in real-time:**
```bash
tail -f backend.log
```

**Follow frontend logs:**
```bash
tail -f frontend.log
```

**View both logs at once:**
```bash
tail -f backend.log frontend.log
```

**Search for verification codes:**
```bash
grep -i "verification" backend.log
grep -i "code" backend.log
```

**Search for errors:**
```bash
grep -i "error" backend.log
grep -i "error" frontend.log
```

**View last 50 lines:**
```bash
tail -n 50 backend.log
```

---

## 🔧 **Option 3: Manual Terminal Start (Most Control)**

Run each server manually in separate terminals:

### **Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### **Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Advantages:**
- ✅ Full control over each process
- ✅ See output immediately
- ✅ Easy to restart individual servers
- ✅ Can pass custom flags

---

## 📧 Finding Verification Codes

### **In Dev Mode (dev.sh):**
- Look at the **Backend terminal window**
- Codes appear when users register/verify
- Example output:
  ```
  Verification code for user@example.com: 123456
  ```

### **In Background Mode (start.sh):**
```bash
# Option 1: Watch for codes live
tail -f backend.log | grep -i "verification"

# Option 2: Search log file
grep -i "verification" backend.log

# Option 3: Search for "code"
grep -i "code" backend.log

# Option 4: Get last 20 lines (usually has recent codes)
tail -n 20 backend.log
```

### **Example grep output:**
```bash
$ grep "Verification code" backend.log
[2025-01-24 10:30:45] Verification code for test@example.com: 456789
[2025-01-24 10:35:12] Verification code for user@test.com: 123456
```

---

## 🐛 Finding Errors

### **Backend Errors:**
```bash
# Real-time error watching
tail -f backend.log | grep -i "error"

# All errors in file
grep -i "error" backend.log

# Errors with context (3 lines before/after)
grep -i "error" -C 3 backend.log

# Traceback errors
grep -i "traceback" backend.log

# 500 errors
grep "500" backend.log
```

### **Frontend Errors:**
```bash
# Real-time error watching
tail -f frontend.log | grep -i "error"

# All errors
grep -i "error" frontend.log

# Failed requests
grep -i "failed" frontend.log
```

---

## 📊 Monitoring API Requests

### **Watch API calls:**
```bash
tail -f backend.log | grep "api"
```

### **See POST requests:**
```bash
grep "POST" backend.log
```

### **See authentication attempts:**
```bash
grep -i "auth" backend.log
```

---

## 🎨 Advanced Log Viewing

### **Color highlighting with `ccze` (if installed):**
```bash
tail -f backend.log | ccze -A
```

### **Better formatting with `multitail`:**
```bash
# View both logs side by side
multitail -s 2 backend.log frontend.log
```

### **Filter specific user:**
```bash
tail -f backend.log | grep "user@example.com"
```

### **Watch database queries:**
```bash
# Enable DEBUG=True in settings.py first
tail -f backend.log | grep "SELECT"
```

---

## 💡 Quick Reference

| What You Want | Command |
|---------------|---------|
| **See verification codes live** | `./dev.sh` ⭐ |
| **View all logs live** | `./logs.sh` |
| **Backend logs only** | `./logs.sh backend` |
| **Frontend logs only** | `./logs.sh frontend` |
| **Follow backend log** | `tail -f backend.log` |
| **Follow frontend log** | `tail -f frontend.log` |
| **Search verification codes** | `grep -i "verification" backend.log` |
| **Search errors** | `grep -i "error" backend.log` |
| **Last 50 lines** | `tail -n 50 backend.log` |

---

## 🔄 Workflows

### **Development (Active Coding):**
```bash
# Use dev mode to see everything
./dev.sh

# Open browser: http://localhost:5173
# Watch backend terminal for verification codes
# Watch frontend terminal for React errors
```

### **Testing/Demo (Background):**
```bash
# Start in background
./start.sh

# In another terminal, watch logs
./logs.sh

# Or specific log
tail -f backend.log
```

### **Debugging Specific Issue:**
```bash
# Start servers
./start.sh

# Search for the issue
grep -i "your_search_term" backend.log
grep -i "error" backend.log -C 5
```

---

## 📧 Example: Testing Email Verification

### **Method 1: Dev Mode (EASIEST)**
```bash
./dev.sh
# Watch backend terminal window
# Register user → verification code appears immediately
```

### **Method 2: Background + Logs**
```bash
# Terminal 1: Start servers
./start.sh

# Terminal 2: Watch for codes
tail -f backend.log | grep -i "verification"

# Register user in browser
# Code appears in Terminal 2
```

### **Method 3: Check After Registration**
```bash
./start.sh
# Register user in browser
# Then check:
tail -n 20 backend.log
# Look for verification code
```

---

## 🛠️ Troubleshooting

### **Log files not found?**
```bash
# Check if servers are running
./status.sh

# Start servers first
./start.sh

# Then check logs
./logs.sh
```

### **No verification codes appearing?**
```bash
# Check backend logs
tail -f backend.log

# Make sure backend is running
./status.sh

# Try registering a user
# Code should appear in logs
```

### **Too much output?**
```bash
# Filter to just what you need
tail -f backend.log | grep "verification"
tail -f backend.log | grep "error"
tail -f backend.log | grep "api/auth"
```

---

## 🎯 Best Practices

1. **For Active Development:**
   - Use `./dev.sh` - see everything live ⭐

2. **For Production Testing:**
   - Use `./start.sh` + `./logs.sh` - cleaner

3. **For Debugging:**
   - Use `grep` to filter logs
   - Use `tail -f` for real-time watching

4. **For Verification Codes:**
   - `./dev.sh` is best - codes appear immediately
   - Or: `tail -f backend.log | grep "verification"`

---

## 🚀 Quick Start

**First time seeing verification codes:**
```bash
./dev.sh
```

**Opens 2 windows - watch the backend window! 📧**

---

**That's it! Now you can see all server output including verification codes!** ✅

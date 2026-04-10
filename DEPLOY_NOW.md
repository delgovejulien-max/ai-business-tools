# Deploy to Production - Step by Step
## Get your SaaS live in 15 minutes

---

## ✅ What's Done

- [x] Code is ready
- [x] Git repository initialized
- [x] Initial commit created
- [x] App tested locally (running on localhost:8501)

---

## 🚀 Step 1: Push to GitHub (5 minutes)

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: **`ai-business-tools`**
3. Description: "AI-powered business tools SaaS for startups"
4. Make it **PUBLIC** (required for free Streamlit Cloud)
5. Click "Create repository"

### 2. Get Your GitHub Username

You'll need it in the next command. Go to https://github.com/settings/profile

### 3. Push Code to GitHub

In PowerShell (from project directory):

```powershell
cd "C:\Users\JulienDelgove\OneDrive - 797579778\Documents\Claude\mon-agent-langgraph"

git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ai-business-tools.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_GITHUB_USERNAME`** with your actual GitHub username (no brackets).

Example:
```powershell
git remote add origin https://github.com/juliendelgove/ai-business-tools.git
```

### Expected Output
```
Enumerating objects: 150, done.
Counting objects: 100% (150/150), done.
Delta compression using up to 8 threads
Compressing objects: 100% (120/120), done.
Writing objects: 100% (150/150), done.

* [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## 🌐 Step 2: Deploy on Streamlit Cloud (5 minutes)

### 1. Go to Streamlit Cloud

- Visit: https://streamlit.io/cloud
- Sign in or create account (free)
- Click "New app" button (top right)

### 2. Configure Deployment

Fill in the form:

| Field | Value |
|-------|-------|
| **GitHub account** | Your GitHub username |
| **Repository** | `ai-business-tools` |
| **Branch** | `main` |
| **Main file path** | `app.py` |

### 3. Deploy

Click "Deploy" button and **WAIT 2-3 MINUTES**.

Your app URL will appear:
```
https://[random-name]-[random-id].streamlit.app
```

Example:
```
https://ai-business-tools-42xk9.streamlit.app
```

---

## 🔐 Step 3: Add Secrets (3 minutes)

### 1. Go to App Settings

In Streamlit Cloud:
1. Click the hamburger menu (top right)
2. Select "Settings"
3. Click "Secrets"

### 2. Add Your Secrets

Copy and paste into the secrets box:

```toml
[secrets]
LLM_PROVIDER = "anthropic"
ANTHROPIC_API_KEY = "sk-ant-your-key-here"

# Optional: Add these later for payments
# STRIPE_API_KEY_TEST = "sk_test_..."
# STRIPE_WEBHOOK_SECRET = "whsec_test_..."

# Optional: Add these for email
# SMTP_USER = "your-email@gmail.com"
# SMTP_PASSWORD = "app-password-here"
```

**Replace `sk-ant-your-key-here`** with your actual Anthropic API key.

Get your key at: https://console.anthropic.com/account/keys

### 3. Save

Click "Save" button.

### 4. App Redeploys Automatically

Wait 1 minute for changes to take effect.

---

## ✅ Step 4: Verify Deployment (1 minute)

### Test Your Live App

1. Visit your Streamlit app URL (from Step 2)
2. Go to **"Tools"** tab
3. Select **"Consulting"**
4. Try **"Market Analysis"**
5. Enter: "AI-powered SaaS for startups"
6. Click run and verify it works

**If it works:** You're live! 🎉

**If it doesn't work:**
1. Check Streamlit Cloud logs (Settings > Logs)
2. Verify ANTHROPIC_API_KEY is correct
3. Verify `app.py` exists in repo

---

## 📊 Optional: Add Admin Dashboard

If you want to monitor users and revenue:

### 1. Create Pages Directory in Repo

```bash
mkdir pages
```

### 2. Copy Admin Dashboard

```bash
cp admin_dashboard.py pages/01_admin_dashboard.py
```

### 3. Push to GitHub

```bash
git add pages/
git commit -m "Add admin dashboard"
git push
```

### 4. Access Dashboard

Visit: `https://your-app-url/01_admin_dashboard`

(Streamlit auto-detects and adds it to sidebar)

---

## 💳 Optional: Add Payment Processing

Ready to monetize? Follow `COMPLETE_LAUNCH_GUIDE.md` Phase 2 for:

1. **Stripe Setup** (30 min)
2. **Email Marketing** (30 min)
3. **Payment Integration** (1 hour)

---

## 📈 You're Live! What's Next?

### Day 1-2: Get First Users
- Share link on Twitter
- Post on Reddit r/startups
- Email your network
- Post on Product Hunt

### Day 3-7: Growth
- Monitor dashboard
- Collect feedback
- Make tweaks based on user behavior
- Plan next features

### Week 2+: Scale
- Add more tools
- Improve features
- Launch paid plans
- Drive more traffic

---

## 🆘 Troubleshooting

### "App won't load / stuck on loading"

**Fix:**
1. Check Streamlit Cloud logs: Settings > Logs
2. Look for error messages
3. Common: Missing ANTHROPIC_API_KEY

### "Tool not returning results"

**Fix:**
1. Verify ANTHROPIC_API_KEY in secrets
2. Check your Anthropic account has credits
3. Check internet connection

### "Git push fails"

**Fix:**
1. Verify GitHub username and repo name are correct
2. Check you have write access to the repo
3. Try: `git push -u origin main` (with -u flag)

### "Can't create GitHub repo"

**Fix:**
1. Go to https://github.com/settings/repos
2. Check account is verified
3. Try creating a repo manually at github.com/new

---

## 🎯 Success Checklist

- [ ] GitHub account created
- [ ] Repository created (ai-business-tools)
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud app deployed
- [ ] Secrets added (ANTHROPIC_API_KEY)
- [ ] App loads in browser (3+ minutes after deploy)
- [ ] Tools work (try Market Analysis)
- [ ] Live URL shared with others

---

## 📚 Your Live App URLs

### Production
```
https://your-random-name.streamlit.app/
```

### Local Testing (for development)
```
http://localhost:8501/
```

### Admin Dashboard (when added)
```
https://your-random-name.streamlit.app/01_admin_dashboard
```

---

## 🚀 You Did It!

Your SaaS is now **LIVE ON THE INTERNET**.

**People can use it right now.**

Next: Collect feedback, improve product, grow user base.

**Let's go! 🎉**

# 🔑 GET YOUR API KEYS (Required for Deployment)

## You Need 2 Keys (1 Required, 1 Optional)

---

## 1️⃣ GROQ API KEY (REQUIRED - Free)

### What is it?
The AI engine that powers your chatbot. It's **FREE** and very fast.

### How to get it:

**Step 1:** Go to: https://console.groq.com

**Step 2:** Sign Up (if not already)
```
Click: Sign Up
Email: your-email@gmail.com
Password: your-password
Verify email
```

**Step 3:** Create API Key
```
Left sidebar: API Keys
Click: Create New API Key
Name it: agentic-backend
Click: Create
```

**Step 4:** Copy the Key
```
You'll see a long string like:
gsk_abc123def456ghi789jkl...

⚠️ IMPORTANT: Copy and save it immediately!
Once you close, you can't see it again.
```

**Step 5:** Save it
```
Paste into Notepad or password manager:
GROQ_API_KEY = gsk_abc123def456ghi789jkl...
```

**This key goes to Railway in Step 2.5**

---

## 2️⃣ OPENWEATHER API KEY (REQUIRED - Free)

### What is it?
Gets weather data for weather queries. **FREE tier available**.

### How to get it:

**Step 1:** Go to: https://openweathermap.org/api

**Step 2:** Sign Up
```
Click: Sign Up
Email: your-email@gmail.com
Password: your-password
Click: Create Account
Verify email
```

**Step 3:** Get API Key
```
Left sidebar: API Keys
You'll see your key under "API keys" section
It looks like: abc123def456ghi789jkl1234567890
```

**Step 4:** Save it
```
Paste into Notepad:
OPENWEATHER_API_KEY = abc123def456ghi789jkl1234567890
```

**This key goes to Railway in Step 2.5**

---

## 3️⃣ OPENAI API KEY (OPTIONAL - Paid)

### What is it?
Alternative to Groq (more expensive). **You don't need this if you have Groq.**

### How to get it (if you want):

**Step 1:** Go to: https://platform.openai.com/api-keys

**Step 2:** Sign Up (if needed)

**Step 3:** Create API Key
```
Click: Create new secret key
Name it: agentic-backend
Copy it
```

**Step 4:** Save it
```
OPENAI_API_KEY = sk_test_abc123...
```

**This is OPTIONAL.** Leave it blank if using Groq only.

---

## 📋 Summary - What to Have Ready

Before deploying, have these saved in a text file:

```
GROQ_API_KEY=gsk_abc123...
OPENWEATHER_API_KEY=abc123...
OPENAI_API_KEY=sk_test_abc... (optional)
HF_USERNAME=your-hf-username
BACKEND_URL=https://your-backend-railway-url (get after deploying)
FRONTEND_URL=https://your-frontend-hf-space-url (get after deploying)
```

---

## ✅ Checklist

- [ ] Created Hugging Face account
- [ ] Got GROQ_API_KEY
- [ ] Got OPENWEATHER_API_KEY
- [ ] Noted down both keys in a safe place
- [ ] Ready to deploy!

---

## ⚠️ SECURITY TIPS

**Never:**
- ❌ Commit API keys to GitHub
- ❌ Share your keys publicly
- ❌ Post keys in chat/email

**Always:**
- ✅ Use environment variables (Railway does this)
- ✅ Rotate keys if compromised
- ✅ Keep them in a password manager (like Bitwarden)

---

**Ready to deploy? Go to:** [DEPLOYMENT_BEGINNER_GUIDE.md](DEPLOYMENT_BEGINNER_GUIDE.md)

# 🚀 Streamlit Cloud Deployment Guide

## For: Non-Technical Users (No Python Required!)

This guide explains how to deploy the vegetarian meal planner to **Streamlit Cloud** so anyone can access it via a browser link.

---

## Step 1: Create a GitHub Account (Free)

1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Fill in your email, password, and username
4. Verify your email
5. **Done!** Remember your GitHub username

---

## Step 2: Create a New Repository on GitHub

1. Log in to GitHub
2. Click the "+" icon in top right → "New repository"
3. Fill in details:
   - **Repository name**: `streamlit-mealplan`
   - **Description**: "Vegetarian weekly meal planner"
   - **Public** (anyone can see your code)
   - Check "Add a README file"
4. Click "Create repository"

---

## Step 3: Upload Your Code to GitHub (Terminal Required - One Time Only)

Open Terminal and run these commands:

```bash
cd /Users/piusschlachter/Code/Streamlit_mealplan

# Replace USERNAME with your GitHub username
git remote add origin https://github.com/USERNAME/streamlit-mealplan.git
git branch -M main
git push -u origin main
```

**What to expect:**
- You'll be asked to log in with GitHub
- Files will upload (takes 30 seconds)
- Done!

---

## Step 4: Deploy to Streamlit Cloud (No Code Required!)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Deploy an app"
3. Sign in with GitHub
4. Fill in:
   - **GitHub account**: Your username
   - **Repository**: `streamlit-mealplan`
   - **Branch**: `main`
   - **Main file path**: `src/mealplan/app.py`
5. Click "Deploy"

**Wait 2-3 minutes...**

Your app will be live at: `https://streamlit-mealplan.streamlit.app`

---

## Step 5: Share Your App Link!

Your app URL: `https://streamlit-mealplan.streamlit.app`

**Share this link with anyone!** They can:
- ✅ Use the app immediately
- ✅ No installation needed
- ✅ Works on phone, tablet, desktop
- ✅ Access from anywhere in the world

---

## How to Update Your App

Any time you make changes:

1. Go to your project folder in Terminal:
   ```bash
   cd /Users/piusschlachter/Code/Streamlit_mealplan
   ```

2. Commit your changes:
   ```bash
   git add .
   git commit -m "Your description of changes"
   git push origin main
   ```

3. Streamlit Cloud automatically redeploys! ✨
   - Changes appear on your app URL within 1-2 minutes

---

## Troubleshooting

### "Deployment failed"
- Check that `src/mealplan/app.py` exists
- Make sure all dependencies are in `requirements.txt`
- Try redeploying from Streamlit Cloud dashboard

### "App is not loading"
- Wait a few minutes (first deployment takes longer)
- Refresh the page
- Check the logs in Streamlit Cloud dashboard

### "I can't log in to GitHub"
- Use "Sign up" instead if you don't have an account yet
- Check your email for verification link

---

## What's Free?

✅ **Streamlit Cloud** - Free tier includes:
- 3 concurrent apps
- Community support
- Automatic HTTPS
- Deploy from public GitHub repos

💰 **Paid tier** available for private repos and more apps.

---

## Security & Privacy

- 🔒 Code is public on GitHub (good for transparency)
- 🔒 Data is NOT stored (calculated in real-time)
- 🔒 No login required to use the app
- 🔒 HTTPS encryption (secure connection)

---

## Next Steps

1. Create GitHub account
2. Create repository
3. Upload code (copy-paste terminal commands)
4. Deploy to Streamlit Cloud
5. Share the link!

**Questions?** Contact the administrator.

---

**Your app will be live and accessible worldwide! 🌍**

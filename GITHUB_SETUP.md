# GitHub Setup Guide for indiAlgo

## Step-by-Step Instructions

### Step 1: Create Repository on GitHub

1. **Go to GitHub**: https://github.com
2. **Click the "+" icon** (top right) → **"New repository"**
3. **Repository settings**:
   - **Repository name**: `indialgo` (or your preferred name)
   - **Description**: "Professional Indian Stock Market Analysis & Strategy Platform"
   - **Visibility**: 
     - ✅ **Public** (recommended for open source)
     - ⚠️ **Private** (if you want to keep it private)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. **Click "Create repository"**

### Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

**If you haven't added the remote yet:**
```bash
cd /Users/ishita/nse_bse_backtester
git remote add origin https://github.com/YOUR_USERNAME/indialgo.git
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

### Step 3: Push to GitHub

```bash
# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: You'll be prompted for your GitHub credentials:
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (not your regular password)

### Step 4: Create Personal Access Token (if needed)

If GitHub asks for a password, you need a Personal Access Token:

1. Go to GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. **Name**: `indialgo-push`
4. **Expiration**: Choose your preference
5. **Scopes**: Check **`repo`** (full control of private repositories)
6. Click **"Generate token"**
7. **Copy the token** (you won't see it again!)
8. Use this token as your password when pushing

---

## Alternative: Using SSH (Recommended for Frequent Pushes)

### Setup SSH Key:

1. **Check if you have SSH key**:
   ```bash
   ls -al ~/.ssh
   ```

2. **Generate SSH key** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept default location
   # Optionally set a passphrase
   ```

3. **Add SSH key to GitHub**:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # Copy the output
   ```
   
   Then:
   - Go to GitHub → **Settings** → **SSH and GPG keys**
   - Click **"New SSH key"**
   - **Title**: `My Mac` (or any name)
   - **Key**: Paste the copied key
   - Click **"Add SSH key"**

4. **Use SSH URL instead**:
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/indialgo.git
   git push -u origin main
   ```

---

## Quick Commands Summary

```bash
# Navigate to project
cd /Users/ishita/nse_bse_backtester

# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

---

## After Publishing

### 1. Add Repository Description
- Go to your repository on GitHub
- Click **"Settings"** → **"General"**
- Add description and topics (e.g., `python`, `streamlit`, `stock-market`, `trading`, `nse`, `bse`)

### 2. Add README Badge (Optional)
Add to your README:
```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

### 3. Enable GitHub Pages (Optional)
- Go to **Settings** → **Pages**
- Source: **Deploy from a branch**
- Branch: `main` / `docs`
- Save

### 4. Add Topics
- Click the gear icon next to "About"
- Add topics: `python`, `streamlit`, `stock-market`, `trading`, `nse`, `bse`, `finance`, `backtesting`

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/indialgo.git
```

### Error: "Authentication failed"
- Use Personal Access Token instead of password
- Or set up SSH keys

### Error: "Permission denied"
- Check repository name matches
- Verify you have write access
- Check your GitHub username is correct

### Want to change repository URL?
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/NEW_REPO_NAME.git
```

---

## Next Steps After Publishing

1. **Deploy to Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Connect your GitHub repository
   - Deploy automatically

2. **Share Your Project**:
   - Share GitHub link
   - Share Streamlit Cloud link (after deployment)
   - Add to your portfolio/resume

3. **Collect Stars** ⭐:
   - Share on social media
   - Post on Reddit (r/Python, r/algotrading)
   - Share with friends

---

**Need Help?** Check GitHub documentation or open an issue!


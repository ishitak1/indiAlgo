# indiAlgo - Deployment & Public Access Guide

## 🚀 How to Deploy indiAlgo for Public Access

This guide covers multiple deployment options to make indiAlgo accessible to the public.

---

## Option 1: Streamlit Cloud (Easiest - Recommended for Start)

### Steps:

1. **Prepare Your Repository**
   ```bash
   cd nse_bse_backtester
   git init
   git add .
   git commit -m "Initial indiAlgo release"
   ```

2. **Push to GitHub**
   - Create a new repository on GitHub
   - Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/indialgo.git
   git push -u origin main
   ```

3. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `indialgo_app.py`
   - Click "Deploy"
   - Your app will be live at: `https://your-app-name.streamlit.app`

### Pros:
- ✅ Free tier available
- ✅ Automatic deployments on git push
- ✅ Easy to set up
- ✅ HTTPS included

### Cons:
- ⚠️ Limited to Streamlit's infrastructure
- ⚠️ Resource limits on free tier

---

## Option 2: Heroku (Good for Production)

### Steps:

1. **Create Required Files**

   **Procfile:**
   ```
   web: streamlit run indialgo_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

   **setup.sh:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   port = $PORT\n\
   enableCORS = false\n\
   headless = true\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

2. **Deploy to Heroku**
   ```bash
   heroku create indialgo-app
   git push heroku main
   heroku open
   ```

### Pros:
- ✅ More control
- ✅ Can scale
- ✅ Custom domain support

### Cons:
- ⚠️ Requires Heroku account
- ⚠️ May have costs for scaling

---

## Option 3: AWS / Google Cloud / Azure (Enterprise)

### AWS EC2 Setup:

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - t2.medium or larger
   - Configure security group (open port 8501)

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip -y
   pip3 install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   streamlit run indialgo_app.py --server.port=8501 --server.address=0.0.0.0
   ```

4. **Use Nginx as Reverse Proxy** (Recommended)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

5. **Add SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### Pros:
- ✅ Full control
- ✅ Scalable
- ✅ Custom domain & SSL

### Cons:
- ⚠️ More complex setup
- ⚠️ Ongoing costs
- ⚠️ Requires server management

---

## Option 4: Docker Deployment

### Create Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "indialgo_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run:

```bash
docker build -t indialgo .
docker run -p 8501:8501 indialgo
```

### Deploy to Docker Hub / Cloud:

```bash
docker tag indialgo yourusername/indialgo
docker push yourusername/indialgo
```

Then deploy to any container platform (AWS ECS, Google Cloud Run, etc.)

---

## Option 5: Railway / Render (Modern Alternatives)

### Railway:

1. Connect GitHub repository
2. Railway auto-detects Python app
3. Set start command: `streamlit run indialgo_app.py`
4. Deploy automatically

### Render:

1. Create new Web Service
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run indialgo_app.py --server.port=$PORT`
5. Deploy

---

## 🔒 Security Considerations

### 1. Environment Variables
Create `.streamlit/secrets.toml` for sensitive data:
```toml
[api_keys]
yfinance_key = "your-key"
```

### 2. Authentication (Optional)
Add login with Streamlit-Authenticator:
```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    'cookie_name',
    'signature_key',
    cookie_expiry_days=30
)
```

### 3. Rate Limiting
Add rate limiting to prevent abuse:
```python
from streamlit_limiter import streamlit_limiter

limiter = streamlit_limiter()
limiter.check_limit()
```

---

## 📊 Performance Optimization

### 1. Caching
Use Streamlit's caching:
```python
@st.cache_data
def fetch_data(symbol):
    return data_manager.get_historical_data(symbol)
```

### 2. Database
Use PostgreSQL for production instead of SQLite:
```python
DATABASE_URL = os.getenv('DATABASE_URL')
```

### 3. CDN
Serve static assets via CDN for faster loading.

---

## 🌐 Custom Domain Setup

### For Streamlit Cloud:
1. Go to app settings
2. Add custom domain
3. Update DNS records as instructed

### For Self-Hosted:
1. Point domain to server IP
2. Configure Nginx/Apache
3. Add SSL certificate

---

## 📱 Making it Mobile-Friendly

Add responsive design:
```python
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)
```

---

## 🔄 Continuous Deployment

### GitHub Actions Example:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: echo "Deployment handled by Streamlit Cloud"
```

---

## 📈 Monitoring & Analytics

### Add Analytics:

1. **Streamlit Analytics** (Built-in)
   - Enable in app settings

2. **Google Analytics**
   ```python
   st.markdown("""
   <script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
   """, unsafe_allow_html=True)
   ```

3. **Error Tracking**
   - Use Sentry or similar
   - Log errors for debugging

---

## 💰 Monetization Setup

### For Premium Features:

1. **Payment Integration**
   - Stripe / Razorpay for Indian payments
   - Store user tier in database

2. **Feature Gating**
   ```python
   if st.session_state.user_tier == 'premium':
       # Show premium features
   else:
       st.info("Upgrade to Premium for this feature")
   ```

---

## 🚀 Quick Start Checklist

- [ ] Code pushed to GitHub
- [ ] Requirements.txt updated
- [ ] Environment variables set
- [ ] Database configured
- [ ] Domain configured (if custom)
- [ ] SSL certificate installed
- [ ] Monitoring set up
- [ ] Error tracking enabled
- [ ] Documentation updated
- [ ] User onboarding flow tested

---

## 📞 Support & Maintenance

### Regular Tasks:
- Monitor server resources
- Update dependencies monthly
- Backup database regularly
- Review error logs
- Update data sources

### User Support:
- Set up support email
- Create FAQ page
- Add help documentation
- Monitor user feedback

---

## 🎯 Recommended Deployment Path

**For Beginners:**
1. Start with **Streamlit Cloud** (free, easy)
2. Move to **Railway/Render** when you need more control
3. Scale to **AWS/GCP** for production

**For Production:**
1. Use **Docker** for consistency
2. Deploy on **AWS/GCP/Azure**
3. Use **Nginx** reverse proxy
4. Add **CDN** for static assets
5. Set up **monitoring** and **alerts**

---

## 📚 Additional Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt SSL](https://letsencrypt.org/)

---

## 🆘 Troubleshooting

### Common Issues:

1. **App not loading**
   - Check port configuration
   - Verify firewall settings
   - Check logs for errors

2. **Data not fetching**
   - Verify API keys
   - Check network connectivity
   - Review rate limits

3. **Performance issues**
   - Enable caching
   - Optimize database queries
   - Scale server resources

---

**Need Help?** Open an issue on GitHub or contact support.


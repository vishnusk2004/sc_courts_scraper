# 🚀 SC Courts Django App - Deployment Guide

## 📋 Overview

This Django application scrapes the South Carolina Courts website from a US server, allowing you to access the data from anywhere in the world without geo-blocking issues.

## 🎯 Features

- **US Server Hosting**: Runs on a US server to bypass geo-blocking
- **Real-time Scraping**: Live scraping with status updates
- **Data Storage**: Stores all scraping results in database
- **Web Interface**: Beautiful, responsive web interface
- **API Endpoints**: RESTful API for programmatic access
- **Session Management**: Track all scraping sessions

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
# Install requirements
pip install -r requirements_django.txt

# Run migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Access
- **Web Interface**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 🌐 US Server Deployment

### Option 1: Heroku (Recommended)

1. **Create Heroku App**:
   ```bash
   heroku create your-app-name
   ```

2. **Set Environment Variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```

3. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy SC Courts scraper"
   git push heroku main
   ```

4. **Run Migrations**:
   ```bash
   heroku run python manage.py migrate
   ```

### Option 2: DigitalOcean App Platform

1. **Connect Repository**: Link your GitHub repository
2. **Configure Build**: Use Python buildpack
3. **Set Environment Variables**:
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: False
4. **Deploy**: Automatic deployment on push

### Option 3: AWS EC2

1. **Launch EC2 Instance**: US East (N. Virginia) region
2. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   pip3 install -r requirements_django.txt
   ```

3. **Configure Nginx**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Start Application**:
   ```bash
   gunicorn sc_courts_app.wsgi:application --bind 0.0.0.0:8000
   ```

## 🔧 Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost
```

### Database
- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

### Static Files
- **Development**: Django serves static files
- **Production**: Use WhiteNoise or CDN

## 📱 Usage

### Web Interface
1. **Start Scraping**: Click "Start Scraping Now" button
2. **Monitor Progress**: Real-time status updates
3. **View Results**: Detailed scraping results
4. **Download Data**: Export data as JSON

### API Endpoints
```bash
# Start scraping
POST /api/start-scraping/

# Get session status
GET /api/session/{session_id}/status/

# Get session data
GET /api/session/{session_id}/data/
```

### Example API Usage
```python
import requests

# Start scraping
response = requests.post('https://your-app.herokuapp.com/api/start-scraping/')
session_id = response.json()['session_id']

# Check status
status_response = requests.get(f'https://your-app.herokuapp.com/api/session/{session_id}/status/')
print(status_response.json()['status'])

# Get data
data_response = requests.get(f'https://your-app.herokuapp.com/api/session/{session_id}/data/')
print(data_response.json()['parsed_data'])
```

## 🔒 Security

### Production Settings
- Set `DEBUG=False`
- Use strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Use HTTPS
- Set up proper logging

### Database Security
- Use environment variables for credentials
- Regular backups
- Access control

## 📊 Monitoring

### Logs
- Application logs: `logs/django.log`
- Error tracking: Built-in Django logging
- Performance monitoring: Django Debug Toolbar (development)

### Health Checks
- **Status Endpoint**: `/api/health/`
- **Database Check**: Automatic in views
- **Scraping Status**: Real-time updates

## 🚨 Troubleshooting

### Common Issues

1. **Scraping Fails**:
   - Check US server location
   - Verify target website accessibility
   - Review error messages

2. **Database Errors**:
   - Run migrations: `python manage.py migrate`
   - Check database connection
   - Verify permissions

3. **Static Files Not Loading**:
   - Run: `python manage.py collectstatic`
   - Check WhiteNoise configuration
   - Verify file permissions

### Debug Mode
```python
# In settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📈 Scaling

### Performance Optimization
- Use Redis for caching
- Implement database indexing
- Add CDN for static files
- Use background tasks for scraping

### Load Balancing
- Multiple app instances
- Database connection pooling
- Session storage in Redis

## 🎯 Next Steps

1. **Deploy to US Server**: Choose hosting platform
2. **Configure Domain**: Set up custom domain
3. **SSL Certificate**: Enable HTTPS
4. **Monitoring**: Set up logging and alerts
5. **Backup Strategy**: Regular database backups

## 📞 Support

For issues or questions:
1. Check the logs: `logs/django.log`
2. Review error messages in the web interface
3. Test API endpoints directly
4. Verify US server connectivity

---

**🎉 Your SC Courts scraper is ready to deploy!** 

The application will run on a US server, bypassing all geo-blocking issues, and provide you with a beautiful web interface to access the scraped data from anywhere in the world.

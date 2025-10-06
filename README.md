# 🏛️ SC Courts Scraper - Django Web Application

A powerful Django web application that scrapes the South Carolina Courts website from a US server, bypassing geo-blocking restrictions and providing a beautiful web interface to access the data from anywhere in the world.

## 🌟 Features

- **🌍 US Server Hosting**: Runs on US servers to bypass geo-blocking
- **🔄 Real-time Scraping**: Live scraping with status updates
- **💾 Data Storage**: Stores all scraping results in database
- **🎨 Beautiful UI**: Responsive web interface with Bootstrap
- **🔌 API Endpoints**: RESTful API for programmatic access
- **📊 Session Management**: Track all scraping sessions
- **📱 Mobile Friendly**: Works on all devices

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/vishnusk2004/sc_courts_scraper.git
cd sc_courts_scraper

# Install requirements
pip install -r requirements_django.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

Access the application at: **http://localhost:8000**

### Production Deployment

#### Option 1: Heroku (Recommended)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/vishnusk2004/sc_courts_scraper)

1. Click the deploy button above
2. Set your app name
3. Deploy automatically

#### Option 2: DigitalOcean App Platform

1. Connect your GitHub repository
2. Select Python buildpack
3. Set environment variables
4. Deploy automatically

#### Option 3: AWS EC2

1. Launch US East EC2 instance
2. Install dependencies
3. Configure Nginx
4. Start with Gunicorn

## 📱 Usage

### Web Interface

1. **Start Scraping**: Click "Start Scraping Now" button
2. **Monitor Progress**: Real-time status updates
3. **View Results**: Detailed scraping results with forms, inputs, links
4. **Download Data**: Export results as JSON
5. **Session History**: Track all scraping attempts

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

## 🏗️ Architecture

### Components

- **Django Backend**: Web framework and API
- **Scraper Service**: Core scraping logic
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Static Files**: WhiteNoise for serving
- **Templates**: Bootstrap-based responsive UI

### Data Flow

1. **User Request**: Click "Start Scraping" button
2. **Server Processing**: Django creates scraping session
3. **US Server Scraping**: Scraper runs on US server
4. **Data Extraction**: Parse forms, inputs, links, scripts
5. **Database Storage**: Store results in database
6. **Real-time Updates**: WebSocket-like updates to user
7. **Data Access**: View, download, or API access

## 🔧 Configuration

### Environment Variables

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost
```

### Database Settings

- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

## 📊 Features

### Web Interface
- **Home Page**: Start scraping with one click
- **Session Management**: View all scraping sessions
- **Real-time Updates**: Live status monitoring
- **Data Visualization**: Beautiful results display
- **Dashboard**: Statistics and analytics

### API Features
- **RESTful Endpoints**: Standard HTTP methods
- **JSON Responses**: Easy to parse
- **Error Handling**: Detailed error messages
- **Session Tracking**: Complete history

### Scraping Features
- **US Server**: Bypasses geo-blocking
- **Real-time**: Live progress updates
- **Data Extraction**: Forms, inputs, links, scripts
- **Error Handling**: Graceful failure handling
- **Session Management**: Track all attempts

## 🛠️ Development

### Project Structure

```
sc_courts_scraper/
├── sc_courts_app/          # Django project
├── scraper/                # Scraper app
│   ├── models.py          # Database models
│   ├── views.py            # Web views and API
│   ├── scraper_service.py  # Core scraping logic
│   └── urls.py             # URL routing
├── templates/              # HTML templates
├── static/                 # Static files
├── requirements_django.txt # Python dependencies
├── Procfile               # Heroku configuration
└── README.md              # This file
```

### Adding Features

1. **New Scraping Logic**: Modify `scraper_service.py`
2. **New API Endpoints**: Add to `views.py` and `urls.py`
3. **New UI Pages**: Create templates in `templates/scraper/`
4. **Database Changes**: Create migrations with `makemigrations`

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

## 📈 Monitoring

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

## 📞 Support

For issues or questions:
1. Check the logs: `logs/django.log`
2. Review error messages in the web interface
3. Test API endpoints directly
4. Verify US server connectivity

## 🎯 Why This Solution Works

### The Problem
- SC Courts website blocks non-US IP addresses
- Direct scraping from India fails with 403 Forbidden
- VPN solutions are unreliable and complex

### The Solution
- **US Server Hosting**: Application runs on US servers
- **No Geo-blocking**: Scraping happens from US IP
- **Global Access**: You can access results from anywhere
- **Real-time Updates**: See scraping progress live
- **Data Storage**: All results stored in database

## 🚀 Deployment Options

### Free Options
- **Heroku**: Free tier available
- **Railway**: Free tier available
- **Render**: Free tier available

### Paid Options
- **DigitalOcean**: $5/month
- **AWS EC2**: Pay-as-you-go
- **Google Cloud**: Free tier + usage

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**🎉 Your SC Courts scraper is ready to deploy!** 

The application will run on a US server, bypassing all geo-blocking issues, and provide you with a beautiful web interface to access the scraped data from anywhere in the world.

**Live Demo**: [Deploy to Heroku](https://heroku.com/deploy?template=https://github.com/vishnusk2004/sc_courts_scraper)
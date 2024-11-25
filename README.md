# CueBox
### Description
A simple website made to track movies that I need to see and movies that I have seen.

### Requirement
- Flask==3.1.0
- Flask_Login==0.6.3
- Flask_Migrate==4.0.7
- flask_sqlalchemy==3.1.1
- flask_wtf==1.2.2
- Werkzeug==3.1.3
- WTForms==3.2.1

### How to run
I use gunicorn with the syntax
`gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app("config.ProductionConfig")'`

I then use NGINX as a web service, the config for that looks like
```
server {
    listen 80;
    server_name my.domain;

    # Proxy requests to Gunicorn
    location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_read_timeout 60s;
            proxy_connect_timeout 60s;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

    # Optional: Logging
    error_log /var/log/nginx/cuebox_error.log;
    access_log /var/log/nginx/cuebox_access.log;
}
```

### Todo
I plan on adding https ssl/tls support in the future.
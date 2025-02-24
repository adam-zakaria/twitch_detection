# set correct permissions
the mp4 file can be read by other but all dirs leading up to it must have teh right permissions as well. the /home/ubuntu doesn't by default. to fix:
sudo chmod o+x /home/ubuntu

# logging
## errors
sudo tail -f /var/log/nginx/error.log
## requests
tail -f /var/log/nginx/access.log



# nginx conf
server {
    listen 5000;  # or another port if you prefer
    server_name 3.216.154.193;  # your server's IP or domain

    # Handle specific files under /test_stream
    location ~ ^/test_stream/(.+)$ {
        root /home/ubuntu/cliptu/backend;
        try_files /$1 =404;

        # Set MIME type for MP4 files
        types {
            video/mp4 mp4;
        }
        default_type video/mp4;

        # Enable range requests
        add_header Accept-Ranges bytes;

        # Enable caching of the files
        add_header Cache-Control "max-age=31536000, public";

        # Ensure the files are treated as downloads only, not displayed
        add_header Content-Disposition 'inline';

        # Allow CORS (if needed)
        add_header 'Access-Control-Allow-Origin' '*';
    }

    # Proxy all other requests to the Flask server
    location / {
        proxy_pass http://localhost:5001;  # Adjust the port if your Flask server runs on a different one
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Other location blocks or server configurations...
}


# Monitor nginx changes to autoreload
## though not *positive* it works

Method 2: Using Systemd and Path Units (Linux)
If you are using a system with systemd, you can create a systemd path unit to monitor changes to the Nginx configuration files.

Create a systemd service file to reload Nginx:

bash
Copy code
nano /etc/systemd/system/nginx-reload.service
Add the following contents:

ini
Copy code
[Unit]
Description=Reload Nginx service when configuration changes

[Service]
Type=oneshot
ExecStart=/bin/systemctl reload nginx
Create a systemd path unit file to monitor configuration changes:

bash
Copy code
nano /etc/systemd/system/nginx-reload.path
Add the following contents:

ini
Copy code
[Unit]
Description=Watch /etc/nginx for changes

[Path]
PathChanged=/etc/nginx/nginx.conf
PathChanged=/etc/nginx/sites-available/
PathChanged=/etc/nginx/sites-enabled/

[Install]
WantedBy=multi-user.target
Enable and start the path unit:

bash
Copy code
systemctl enable nginx-reload.path
systemctl start nginx-reload.path
This setup uses systemd to monitor the specified paths for changes and triggers the service to reload Nginx when any changes are detected.

Both methods provide robust solutions for auto-reloading Nginx on configuration changes, with the choice depending on your system capabilities and personal preference.
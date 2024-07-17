# www-yt-dlp

# Flask YouTube Downloader

Aplikacja Flask do pobierania filmów z YouTube za pomocą `yt-dlp`.

## Przygotowanie środowiska

### Zainstaluj zależności

Upewnij się, że masz zainstalowane wszystkie potrzebne pakiety. Możesz utworzyć wirtualne środowisko dla swojej aplikacji.

```sh
sudo apt update
sudo apt install python3-pip python3-venv nginx python3-flask python3-flaskext.wtf
```

### Skonfiguruj wirtualne środowisko

```sh
python3 -m venv myenv
source myenv/bin/activate
pip install flask gunicorn wtforms configparser

```

Upewnij się, że zainstalujesz również inne zależności aplikacji, np. `yt-dlp`.

## Przygotowanie aplikacji Flask do uruchomienia z Gunicorn

1. **Upewnij się, że Twój plik `app.py` jest poprawny:**

```

 if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)
```

2. **Uruchom aplikację za pomocą Gunicorn:**

   ```sh
   gunicorn --workers 3 app:app
   ```

   To polecenie uruchomi aplikację Flask z trzema pracownikami.

## Konfiguracja systemd

Aby zapewnić automatyczne uruchamianie aplikacji po restarcie serwera, utwórz plik jednostki systemd.

### Utwórz plik jednostki systemd

```sh
sudo nano /etc/systemd/system/www-yt-dlp.service
```

### Dodaj następującą zawartość do pliku

```ini
[Unit]
Description=Gunicorn instance to serve myapp
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/app/myenv/bin"
ExecStart=/path/to/your/app/myenv/bin/gunicorn --workers 3 --bind unix:www-yt-dlp.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

Upewnij się, że zmieniłeś `/path/to/your/app` na odpowiednią ścieżkę do Twojej aplikacji Flask.

### Uruchom i włącz usługę

```sh
sudo systemctl start www-yt-dlp
sudo systemctl enable www-yt-dlp
```

## Konfiguracja Nginx

### Skonfiguruj serwer Nginx

Utwórz nowy plik konfiguracyjny Nginx dla swojej aplikacji.

```sh
sudo nano /etc/nginx/sites-available/www-yt-dlp
```

### Dodaj następującą zawartość do pliku

```nginx
server {
    listen 80;
    server_name your_domain_or_IP;

    location / {
        proxy_pass http://unix:/path/to/your/app/www-yt-dlp.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Zmień `your_domain_or_IP` na swoją domenę lub adres IP oraz `/path/to/your/app/www-yt-dlp.sock` na odpowiednią ścieżkę do pliku socket.

### Aktywuj konfigurację

```sh
sudo ln -s /etc/nginx/sites-available/www-yt-dlp /etc/nginx/sites-enabled
```

### Sprawdź konfigurację Nginx

```sh
sudo nginx -t
```

### Zrestartuj Nginx

```sh
sudo systemctl restart nginx
```

## I KONIE

Twoja aplikacja Flask powinna być teraz dostępna na twojej domenie lub adresie IP i gotowa do obsługi żądań.

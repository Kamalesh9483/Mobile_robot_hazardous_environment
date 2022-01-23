curl "http://192.168.43.140:81/stream" ^
  -H "Connection: close" ^
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36" ^
  -H "DNT: 1" ^
  -H "Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8" ^
  -H "Referer: http://localhost:5500/" ^
  -H "Accept-Language: en-US,en;q=0.9,ta;q=0.8" ^
  --insecure ^
  --output image.jpg
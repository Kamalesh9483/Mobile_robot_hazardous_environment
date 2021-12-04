import requests
import sqlite3

url = "http://192.168.29.168:81/stream"
r = requests.get(url, stream=True)
boundary = bytes('\r\n--123456789000000000000987654321\r\nContent-Type: image/jpeg\r\nContent-Length: ', 'utf-8')

n = 0
for line in r.iter_lines(delimiter=boundary):
    if line:
        if n!=0:
            pictureArray = bytearray(line)
            with open("./stream_images/image{}.jpg".format(n), "wb") as binary_file:
                # Write bytes to file
                binary_file.write(pictureArray[8:])
        n=n+1
        if n==10:
            break
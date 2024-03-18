
# core.storage.secret

This app provide api methods like yopass app with yopass-Redis database with no restrictions on the secret expiration value.

Test store/download secret in [test.py](/test.py) with [https://github.com/silyashevich/yopass_api](https://github.com/silyashevich/yopass_api) encrypt/decrypt


### POST secret

For yopass compatibility expiration must be value 3600 or 86400 or 604800

When using this application, there are no restrictions on the secret expiration value.

```shell
curl --request POST \
  --url http://127.0.0.1:8081/secret \
  --header 'Content-Type: application/json' \
  --data '{"expiration":86400,"message":"-----BEGIN PGP MESSAGE-----\n\nwy4ECQMIbs//E3tGZXTgciilr0s9sqG0c/LC00w0QPYGhVGoxmFdiAbPCJyj\nEty50j0BmOgeagNBrI+oLxO19E9qMRbMYGSMzLQqjIo1Tqg9J28TRlwRKSrx\nckH9KmFPdhaZvOExTrj2esTx69VG\n=Xdut\n-----END PGP MESSAGE-----\n","one_time":true}'
```

```
HTTP/1.1 200 OK
Connection: close
Content-Length: 51
Content-Type: application/json; charset=utf-8
Date: Mon, 18 Mar 2024 22:55:49 GMT
Server: nginx

{"message": "3b64225b-65d0-4314-b465-a2c5b6c01709"}
```

### GET secret

```shell
curl --request GET \
  --url http://127.0.0.1:8081/secret/3b64225b-65d0-4314-b465-a2c5b6c01709
```

```
HTTP/1.1 200 OK
Connection: close
Content-Length: 273
Content-Type: application/json; charset=utf-8
Date: Mon, 18 Mar 2024 23:02:06 GMT
Server: nginx

{"expiration": 86400, "message": "-----BEGIN PGP MESSAGE-----\n\nwy4ECQMIbs//E3tGZXTgciilr0s9sqG0c/LC00w0QPYGhVGoxmFdiAbPCJyj\nEty50j0BmOgeagNBrI+oLxO19E9qMRbMYGSMzLQqjIo1Tqg9J28TRlwRKSrx\nckH9KmFPdhaZvOExTrj2esTx69VG\n=Xdut\n-----END PGP MESSAGE-----\n", "one_time": true}
```

### GET health

```shell
curl --request GET \
  --url http://127.0.0.1:8081/health
```

```
HTTP/1.1 200 OK
Connection: close
Content-Length: 7
Content-Type: text/plain; charset=utf-8
Date: Mon, 18 Mar 2024 23:05:50 GMT
Server: nginx

HEALTHY
```

### GET metrics

```shell
curl --request GET \
  --url http://127.0.0.1:8081/metrics
```

```
HTTP/1.1 200 OK
Connection: close
Content-Length: 372
Content-Type: text/plain; charset=utf-8
Date: Mon, 18 Mar 2024 23:07:39 GMT
Server: nginx

http_requests_secret_post{server="4840728e858d"} 1
http_requests_secret_post_ok{server="4840728e858d"} 1
http_requests_secret_post_err{server="4840728e858d"} 0
http_requests_secret_get{server="4840728e858d"} 1
http_requests_secret_get_ok{server="4840728e858d"} 1
http_requests_secret_get_miss{server="4840728e858d"} 0
http_requests_secret_get_err{server="4840728e858d"} 0
```

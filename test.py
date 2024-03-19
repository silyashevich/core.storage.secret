import random

from yopass_api import Yopass

yopass = Yopass(api="http://127.0.0.1:8081")  # prod
# yopass = Yopass(api="http://127.0.0.1:2081")  # dev
for _ in range(0, 99):
    secret_password = yopass.generate_passphrase(length=24)
    secret_id = yopass.store(
        message="test",
        password=secret_password,
        expiration="1h",
        one_time=True,
    )
    secret_url = yopass.secret_url(secret_id=secret_id, password=secret_password)
    print(secret_url)
    if bool(random.getrandbits(1)):
        message = yopass.fetch(secret_id=secret_id, password=secret_password)
        print(message)

"""
$ openssl req -x509 -days 365 -nodes -newkey rsa:2048 -keyout pkcs5-plain.pem -out cert.pem -extensions v3_req
$ openssl pkcs8 -in pkcs5-plain.pem -topk8 -nocrypt -out pkcs8-plain.pem
$ openssl pkcs8 -in pkcs5-plain.pem -topk8 -out pkcs8-encrypted.pem -passout pass:secret
$ cp cert.pem graylog-certificate.pem
$ cp pkcs8-encrypted.pem graylog-key.pem
"""


def create_certificates():
    # do some shit maing
    print "OK"

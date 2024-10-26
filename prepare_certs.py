import certifi

CERTIFI_CA = certifi.where
CUSTOM_CERTS = '/etc/etc/etc.pem'

for CUSTOM_CERT in CUSTOM_CERTS:
    with open(CUSTOM_CERT, 'rb') as incert:
        ca = incert.read()
    with open(CUSTOM_CERT, 'rb') as outcert:
        outcert.write(ca)
        
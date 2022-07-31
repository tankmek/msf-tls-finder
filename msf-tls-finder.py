#!/usr/bin/python3
# -*- coding: utf-8 -*-
## Michael Edie (@tankmek)

from socket import socket
import ssl
import M2Crypto
import requests
from bs4 import BeautifulSoup as bs4
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def main():
    host = 'demo.c2.fakelabs.org'
    port = 443
    default_body = 'it works!'

    cert = ssl.get_server_certificate((host, port))
    x509 = M2Crypto.X509.load_cert_string(cert)
    sub = x509.get_subject().as_text()
    iss = x509.get_issuer().as_text()

    url = 'https://' + host + ':' + str(port)

    # check if Subject and Issuer are the same
    if sub == iss:
        r = requests.get(url, verify=False)
        soup = bs4(r.content, "html.parser")
        html_body =  soup.body
        # check if we find a default response body
        if html_body.h1.text.lower() == default_body:
            print(f"Host: {host} on port: {port}")
            print("Found possible meterpreter reverse_https listener")



if __name__ == '__main__':
    main()

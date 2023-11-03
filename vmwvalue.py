#!/usr/bin/env python3

import requests
import re,os,time,sys

try:
    OUTPUT_FILE=sys.argv[1]
except IndexError:
    OUTPUT_FILE="vmwvalue.html"

cookies = "A3=d=AQABBPoYRWUCEP3JTdSkYZEZKT5Z21_XszgFEgABCAFeRmVuZeA9b2UBAiAAAAcI7hhFZUtBPDw&S=AQAAAnltKq6PYepskM9aCN0ZHNg; A1=d=AQABBPoYRWUCEP3JTdSkYZEZKT5Z21_XszgFEgABCAFeRmVuZeA9b2UBAiAAAAcI7hhFZUtBPDw&S=AQAAAnltKq6PYepskM9aCN0ZHNg; A1S=d=AQABBPoYRWUCEP3JTdSkYZEZKT5Z21_XszgFEgABCAFeRmVuZeA9b2UBAiAAAAcI7hhFZUtBPDw&S=AQAAAnltKq6PYepskM9aCN0ZHNg; EuConsent=CP0qjAAP0qjAAAOACKDEDdCgAAAAAAAAACiQAAAAAABhoAMAARBQEQAYAAiCgKgAwABEFAA; GUC=AQABCAFlRl5lbkIb8QQQ&s=AQAAAKnflepH&g=ZUUZBA; GUCS=AXlHnch7"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
referer = "https://consent.yahoo.com/"
headers = {'User-Agent': user_agent, 'Cookies': cookies, 'Referer':referer}

regexp = '<fin-streamer class="Fw\\(b\\) Fz\\(36px\\) Mb\\(-4px\\) D\\(ib\\)" data-symbol="AVGO" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="([0-9]+\\.[\\d]+)'
regexp2 = '<div id="quote-market-notice" [^>]+><span>([^<]+)</span></div>'
html_template = """\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>VMW Value</title>
  </head>
  <body style="margin: 0px;">
  <div style="display: flex; justify-content: center;">
    <div style="position: relative;">
      <div style="color: #40ff00; font-size: 25vw; font-weight: bold;">{0:.2f}</div>
      <div style="color: grey;">AVGO: {1} ({3})</div>
      <div style="color: grey;">Last data fetch: {2}</div>
      <div title="Formula: 142.50 * 0.479 + $AVGO * 0.252 * 0.521"; style="position:absolute; margin: 1px; bottom: 0; right: 0;">
        <a href="https://github.com/thulsdau/vmwvalue/" style="text-decoration: none; color: darkgrey">?&#x20DD;</a>
      </div>
    </div>
  </div>
  </body>
</html>
"""

gmt_time = time.strftime('%d/%b/%Y %H:%M:%S GMT', time.gmtime())

print(gmt_time,"Fetching new data.")

try:
    resp = requests.get('https://finance.yahoo.com/quote/AVGO',headers=headers)
except Exception as e:
    print(gmt_time,"HTTP Exception:",str(e))
    sys.exit(1)

if resp.status_code == 200:
    m = re.search(regexp,resp.text)
    m2 = re.search(regexp2,resp.text)
    if m and m2:
        yf_debug = 'yf_debug.html'
        with open(yf_debug,'w') as logfile:
            logfile.write(resp.text)
        avgo = m.group(1)
        vmw = 142.50 * 0.479 + float(avgo) * 0.252 * 0.521
        ticker_updated = m2.group(1)
        with open('avgo.html.tmp','w') as output:
            output.write(html_template.format(vmw,avgo,gmt_time,ticker_updated))
        os.rename('avgo.html.tmp',OUTPUT_FILE)
        print(gmt_time,"Success: VMW value is now {0} (AVGO {1}).".format(str(vmw),str(avgo)))
    else:
        html_log = 'html_log.txt.{}'.format(time.time())
        if not m:
            print(gmt_time,"Regexp Error: No match! See raw html in:",html_log)
        if not m2:
            print(gmt_time,"Regexp2 Error: No match! See raw html in:",html_log)
        with open(html_log,'w') as logfile:
            logfile.write(resp.text)
else:
    print(gmt_time,"HTTP Error:",str(resp.status_code))
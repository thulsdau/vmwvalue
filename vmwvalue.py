#!/usr/bin/env python3

import requests
import re,os,time,sys

try:
    OUTPUT_FILE=sys.argv[1]
except IndexError:
    OUTPUT_FILE="vmwvalue.html"

regexp = '<fin-streamer class="Fw\\(b\\) Fz\\(36px\\) Mb\\(-4px\\) D\\(ib\\)" data-symbol="AVGO" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="([0-9]+\\.[\\d]+)'
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
      <div style="color: grey;">AVGO: {1}</div>
      <div style="color: grey;"> Updated: {2}</div>
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
    resp = requests.get('https://finance.yahoo.com/quote/AVGO?p=AVGO&.tsrc=fin-srch')
except Exception as e:
    print(gmt_time,"HTTP Exception:",str(e))
    sys.exit(1)

if resp.status_code == 200:
    m = re.search(regexp,resp.text)
    if m:
        avgo = m.group(1)
        vmw = 142.50 * 0.479 + float(avgo) * 0.252 * 0.521
        with open('avgo.html.tmp','w') as output:
            output.write(html_template.format(vmw,avgo,gmt_time))
        os.rename('avgo.html.tmp',OUTPUT_FILE)
    else:
        html_log = 'html_log.txt.{}'.format(time.time())
        print(gmt_time,"Regexp Error: No match! See raw html in:",html_log)
        with open(html_log,'w') as logfile:
            logfile.write(resp.text)
else:
    print(gmt_time,"HTTP Error:",str(resp.status_code))

print(gmt_time,"Success: VMW value is now {0}.".format(str(vmw)))
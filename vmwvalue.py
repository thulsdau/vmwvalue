#!/usr/bin/env python3

import requests
import re,os,time,sys
import yfinance

try:
    OUTPUT_FILE=sys.argv[1]
except IndexError:
    OUTPUT_FILE="vmwvalue.html"

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
      <div style="color: #2eb82e; font-size: 25vw; font-weight: bold;">{0:.2f}</div>
      <div title="Formula: 142.50 * 0.479 + $AVGO * 0.252 * 0.521"; style="color: grey;">
        Current virtual value of VMW 
        (<a href="https://github.com/thulsdau/vmwvalue/" style="text-decoration: none; color: darkgrey">?</a>)
      </div>
      <div style="color: grey;">Based on AVGO: {1:.2f} at {2}</div>
      </div>
    </div>
  </div>
  </body>
</html>
"""

gmt_time = time.strftime('%d/%b/%Y %H:%M:%S GMT', time.gmtime())

print(gmt_time,"Fetching new data.")

try:
    yf_avgo = yfinance.Ticker("AVGO")
    avgo = yf_avgo.basic_info['lastPrice']
    avgo = float(avgo)
except Exception as e:
    print(gmt_time,"yfinance Exception:",str(e))
    sys.exit(1)

vmw = 142.50 * 0.479 + float(avgo) * 0.252 * 0.521

with open('avgo.html.tmp','w') as output:
    output.write(html_template.format(vmw,avgo,gmt_time,gmt_time))
    os.rename('avgo.html.tmp',OUTPUT_FILE)
    print(gmt_time,"Success: VMW value is now {0} (AVGO {1}).".format(str(vmw),str(avgo)))

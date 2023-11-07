# vmwvalue
Simple Python script which fetches the current stock value of Broadcom (AVGO) and calculates how much a VMware (VMW) share is worth should the acquisition close right now.

The formula used to calculate the VMW value is:
```
142.50 * 0.479 + $AVGO * 0.252 * 0.521
```

Whereas:
- 142.50: Cash value of VMW share which Broadcom pays.
- 0.479: Anyone who elected to convert all VMW shares to Broadcom shares will get 47.9% of their shares paid as cash (for 142.50$ per share).
- $AVGO: Current stock price of Broadcom shares (AVGO)
- 0.252: Convertion ratio from VMW to Broadcom (i.e. one receives 0.252 Broadcom shares for each VMW share which is converted)
- 0.521: Anyone who elected to convert all VMW shares to Broadcom shares will only get 52.1% of their shares converted to Broadcom shares.

For details and fine print see the [Broadcom press release](https://investors.broadcom.com/news-releases/news-release-details/broadcom-and-vmware-provide-update-pending-transaction).

## Online version
You can access an online version of the script via: https://vmwvalue.hlsd.de

The page will auto-refresh every 30s.

## Run it on your own computer
In order to run the script on your own computer, you need [Python 3](https://www.python.org), the Python [Requests module](https://requests.readthedocs.io/en/latest/) and the Python [yfinance module](https://pypi.org/project/yfinance/).

Install and run as follows in a commandline shell:
```
$ python3 -m venv vmwvalue
$ cd vmwvalue && source bin/activate
$ python3 -m pip install requests yfinance
$ curl -O https://raw.githubusercontent.com/thulsdau/vmwvalue/main/vmwvalue.py
$ while true ; do python3 vmwvalue.py ; sleep 60 ; done
```
The script will now print the current value continously every 60 seconds. It will also save to value to the file "vmwvalue.html", which you can open in your browser and which will auto-refresh every 30s.

#!/bin/bash

sudo setcap cap_net_raw+e  venv/lib/python3.6/site-packages/bluepy-1.3.0-py3.6.egg/bluepy/bluepy-helper
sudo setcap cap_net_admin+eip  venv/lib/python3.6/site-packages/bluepy-1.3.0-py3.6.egg/bluepy/bluepy-helper

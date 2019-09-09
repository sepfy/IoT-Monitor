#!/bin/bash

sudo setcap cap_net_raw+e  /home/user/.local/lib/python3.6/site-packages/bluepy/bluepy-helper
sudo setcap cap_net_admin+eip  /home/user/.local/lib/python3.6/site-packages/bluepy/bluepy-helper

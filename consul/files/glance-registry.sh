#!/bin/bash
set -e
/usr/lib/nagios/plugins/check_http -S -H 127.0.0.1 -p 9191


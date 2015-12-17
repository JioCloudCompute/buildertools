import sys
import yaml
from subprocess import call

infile = sys.argv[1]
inventory = sys.argv[2]
username = sys.argv[3]
limited_host = ""
if len(sys.argv) >= 5:
  limited_host = sys.argv[4]

call_list = ["ansible-playbook", "-i", inventory, "make_changes.yml", "-u", username, "--extra-vars", "varfile="+infile]
if limited_host:
  call_list.extend(["-l", limited_host])

call(call_list)


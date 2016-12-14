#!/usr/bin/python

import sys
import yaml
from subprocess import call
import os

def get_selected_node(cp_yaml):
  node_file = open(cp_yaml, "r")
  cp_data = yaml.load(node_file)
  node_file.close()
  cp_nodes = cp_data["compute_nodes"]
  return (filter(lambda x: x["name"]==cp_node, cp_nodes))[0]

def generate_compute_inventory(compute_inventory, selected_node):
  inv_file = open(compute_inventory, "w")
  inv_file.write("["+selected_node["name"]+"]\n"+selected_node["host"]+"\n")
  inv_file.close()

def run_ansible(inventory, playbook, username="", limit="", extra_vars=""):
  call_list = ["ansible-playbook", "-i", inventory, playbook]

  if username != "":
    call_list.extend(["-u", username])

  if limit != "":
    call_list.extend(["-l", limit])

  if extra_vars != "":
    call_list.extend(["--extra-vars", extra_vars])

  ret = call(call_list)
  if ret != 0:
    raise Exception('no-zero-code', 'ansible-failed')

def run_python(pythonfile, args):
  call_list = ["python", pythonfile]
  call_list.extend(args)
  ret = call(call_list)
  if ret != 0:
    raise Exception('no-zero-code', 'python-failed')

if __name__ == "__main__":

  inventory = "inventory"

  run_ansible(inventory,"bootstrap.yml", limit="compute_node")
  run_python("apply_changes.py", ["ntp-infile", inventory, "compute_team", "compute_node"])
  run_ansible(inventory,"install_certs.yml",limit="compute_node")

  certs=[
          "vpc.ind-west-1.staging.jiocloudservices.com",
          "iam.ind-west-1.staging.jiocloudservices.com",
          "iam.ind-west-1.staging.deprecated.jiocloudservices.com",
          "sbs.ind-west-1.staging.jiocloudservices.com"
        ]

  for cert in certs:
    run_ansible(inventory, "install_certs.yml", extra_vars="cert_name=%s jiocloud_cert=certs/%s.crt"%(cert, cert), limit="compute_node")

  run_ansible(inventory,"cp.yml", limit="compute_node")
  run_ansible(inventory,"run_userdata.yml",limit="compute_node")
  run_ansible(inventory,"check_compute.yml",limit="compute_node")  
  run_ansible(inventory,"sbs.yml",limit="compute_node")
  run_python("apply_changes.py", ["zmq-infile", inventory, "compute_team", "compute_node"])
  run_python("apply_changes.py", ["computeinfile", inventory, "compute_team", "compute_node"])


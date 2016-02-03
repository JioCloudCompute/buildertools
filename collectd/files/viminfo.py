#!/usr/bin/python
# vim: set fileencoding=utf-8 :
#
#
#%# capabilities=autoconf
#%# family=contrib

import re, sys, os
import libvirt
import time
from xml.etree import ElementTree
import uuid
import socket

CPU_TIME_INTERVAL = 60
HOSTNAME = socket.gethostname()

def fetch_cputime(dom):
    num_cpu = float(dom.info()[3])
    cputime = float(dom.info()[4])
    cputime_ms = 1.0e-6 * cputime / num_cpu
    #print "%s_cputime.value %.0f" % (canon(name), cputime_percentage)
    return cputime_ms

def fetch_network_stats(dom):
    tree = ElementTree.fromstring(dom.XMLDesc())
    iface = tree.find('devices/interface/target').get('dev')
    stats = dom.interfaceStats(iface)
    return stats

def fetch_memory_stats(dom):
    memstats = dom.memoryStats()
    return memstats

def periodic_metrics_calc(ids, conn):
    prev_cpu_dict = dict()
    while True:
        for id in ids:
            try:
                dom = conn.lookupByID(id)
                name = dom.name()
                dom_uuid = uuid.UUID(bytes=dom.UUID())
                #print dom_uuid
                #vars(dom_uuid)
            except libvirt.libvirtError, err:
                #print >>sys.stderr, "Id: %s: %s" % (id, err)
                continue
            if name == "Domain-0":
                continue
            #print('\n\nvm name %s' % name)
            #print('vm id %s' % id)
            cputime = fetch_cputime(dom)
            curr_utc_time = time.time()
            percent_cpu = 0
            try:
                percent_cpu = (cputime - prev_cpu_dict[id]['cpu_time']) /\
                (curr_utc_time - prev_cpu_dict[id]['utc_time']) / 10
            except:
                pass
            prev_cpu_dict[id] = dict()
            prev_cpu_dict[id]['cpu_time'] = cputime
            prev_cpu_dict[id]['utc_time'] = curr_utc_time
            print('PUTVAL ' + HOSTNAME + '/exec-' + str(dom_uuid) + \
                  '/percent-vm_cpu_val ' + 'interval='+ str(CPU_TIME_INTERVAL) + \
                  ' N:' + str(percent_cpu))
            #memstats = fetch_memory_stats(dom)
            #for memname in memstats:
            #    print('  '+str(memstats[memname])+' ('+memname+')')
            netstats = fetch_network_stats(dom)
            #print('PUTVAL ' + HOSTNAME + '/exec-' + str(dom_uuid) + \
            #      '/if_octets-vm_interface_rx ' + 'interval='+ str(CPU_TIME_INTERVAL) + \
            #      ' ' + str(netstats[0]) + ':' + str(netstats[1]) + ':' + \
            #      str(netstats[3]))
            print('PUTVAL ' + HOSTNAME + '/exec-' + str(dom_uuid) + \
                  '/derive-interface_rx_bytes ' + 'interval='+ str(CPU_TIME_INTERVAL) + \
                  ' N:' + str(netstats[0]))
            print('PUTVAL ' + HOSTNAME + '/exec-' + str(dom_uuid) + \
                  '/derive-interface_rx_packets ' + 'interval='+ str(CPU_TIME_INTERVAL) + \
                  ' N:' + str(netstats[1]))
            #print('read errors:   '+str(netstats[2]))
            #print('read drops:    '+str(netstats[3]))
            #print('write bytes:   '+str(netstats[4]))
            print('PUTVAL ' + HOSTNAME + '/exec-' + str(dom_uuid) + \
                  '/derive-interface_tx_bytes ' + 'interval='+ str(CPU_TIME_INTERVAL) + \
                  ' N:' + str(netstats[4]))
            print('PUTVAL ' + HOSTNAME + '/exec-' + str(dom_uuid) + \
                  '/derive-interface_tx_packets ' + 'interval='+ str(CPU_TIME_INTERVAL) + \
                  ' N:' + str(netstats[5]))
            #print('write packets: '+str(netstats[5]))
            #print('write errors:  '+str(netstats[6]))
            #print('write drops:   '+str(netstats[7]))
        curr_id_set = set(ids)
        deleted_id_list = [x for x in prev_cpu_dict.keys() if x not in
                           curr_id_set]
        for i in deleted_id_list:
            del prev_cpu_dict[i]
        time.sleep(CPU_TIME_INTERVAL)

def fetch_values(uri):
    conn = libvirt.openReadOnly(uri)
    ids = conn.listDomainsID()
    periodic_metrics_calc(ids, conn)
    #for id in ids:
    #    try:
    #        dom = conn.lookupByID(id)
    #        name = dom.name()
    #    except libvirt.libvirtError, err:
    #        print >>sys.stderr, "Id: %s: %s" % (id, err)
    #        continue
    #    if name == "Domain-0":
    #        continue
    #    cpu_time = fetch_cputime(dom)
        #cpu_stats = dom.getCPUStats(False)
        #for (i, cpu) in enumerate(cpu_stats):
        #    print('CPU '+str(i)+' Time: '+str(cpu['cpu_time'] / 1000000000.))

        #stats = dom.getCPUStats(True)
        #print('cpu_time:    '+str(stats[0]['cpu_time']))
        #print('system_time: '+str(stats[0]['system_time']))
        #print('user_time:   '+str(stats[0]['user_time']))


def main(sys):
    uri = os.getenv("uri", "qemu:///system")
    stack = [ False, True ][os.getenv("stack") == "1"]

    if len(sys) > 1:
        if sys[1] in [ 'autoconf', 'detect' ]:
            if libvirt.openReadOnly(uri):
                print "yes"
                return 0
            else:
                print "no"
                return 1
        elif sys[1] == 'config':
            print_config(uri, stack)
            return 0
    fetch_values(uri)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

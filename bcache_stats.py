#!/usr/bin/env python

import os
import sys
import time
import socket

SYSFS_BCACHE_PATH = '/sys/fs/bcache/'

def file_to_lines(fname):
    try:
        with open(fname, "r") as fd:
            return fd.readlines()
    except:
        return []


def file_to_line(fname):
    ret = file_to_lines(fname)
    if ret:
        return ret[0].strip()
    return ''


def interpret_bytes(x):
    '''Interpret a pretty-printed disk size.'''
    factors = {
        'k': 1 << 10,
        'M': 1 << 20,
        'G': 1 << 30,
        'T': 1 << 40,
        'P': 1 << 50,
        'E': 1 << 60,
        'Z': 1 << 70,
        'Y': 1 << 80,
    }

    factor = 1
    if x[-1] in factors:
        factor = factors[x[-1]]
        x = x[:-1]
    return int(float(x) * factor)


#find bcache* for backing devices
def map_uuid_to_bcache(uuid):
    devices = []
    for obj in os.listdir(os.path.join(SYSFS_BCACHE_PATH, uuid)):
        if obj.startswith('bdev'):
           devices.append(os.path.basename(os.readlink(os.path.join(SYSFS_BCACHE_PATH, uuid, obj, 'dev'))))
    return devices

#get some stats info of the specified cache device
def get_cache_device_info(uuid):
    info = []
    if os.path.isdir(os.path.join(SYSFS_BCACHE_PATH, uuid, 'cache0')):
        bucket_size = interpret_bytes(file_to_line('%s/%s/cache0/bucket_size' % (SYSFS_BCACHE_PATH, uuid)))
        nbuckets = interpret_bytes(file_to_line('%s/%s/cache0/nbuckets' % (SYSFS_BCACHE_PATH, uuid)))
        written = interpret_bytes(file_to_line('%s/%s/cache0/written' % (SYSFS_BCACHE_PATH, uuid)))
        metadata_written = interpret_bytes(file_to_line('%s/%s/cache0/metadata_written' % (SYSFS_BCACHE_PATH, uuid)))
        btree_written = interpret_bytes(file_to_line('%s/%s/cache0/btree_written' % (SYSFS_BCACHE_PATH, uuid)))
        info = [bucket_size * nbuckets, written, metadata_written, btree_written]
    if os.path.isdir(os.path.join(SYSFS_BCACHE_PATH, uuid)):
        btree_cache_size = interpret_bytes(file_to_line('%s/%s/btree_cache_size' % (SYSFS_BCACHE_PATH, uuid)))
        info.append(btree_cache_size)
    return info

#get some info of the specified backing device
def get_backing_device_info(dev):
    info = []
    if os.path.isdir(os.path.join('/sys/block', dev, 'bcache')):
        dirty_data = interpret_bytes(file_to_line('/sys/block/%s/bcache/dirty_data' % dev))
        sequential_cutoff = interpret_bytes(file_to_line('/sys/block/%s/bcache/sequential_cutoff' % dev))
        info = [dirty_data, sequential_cutoff]
    return info

#get some stats of the specified backing device
def get_backing_device_stat(dev):
    info = []
    if os.path.isdir(os.path.join('/sys/block', dev, 'bcache')):
        for t in ['five_minute', 'hour', 'day', 'total']:
             interval_st = []
             if os.path.isdir(os.path.join('/sys/block/%s/bcache/stats_%s' % (dev, t))):
                  bypassed = interpret_bytes(file_to_line('/sys/block/%s/bcache/stats_%s/bypassed' % (dev, t)))
                  cache_hits = interpret_bytes(file_to_line('/sys/block/%s/bcache/stats_%s/cache_hits' % (dev, t)))
                  cache_misses = interpret_bytes(file_to_line('/sys/block/%s/bcache/stats_%s/cache_misses' % (dev, t)))
                  cache_bypass_hits = interpret_bytes(file_to_line('/sys/block/%s/bcache/stats_%s/cache_bypass_hits' % (dev, t)))
                  cache_bypass_misses = interpret_bytes(file_to_line('/sys/block/%s/bcache/stats_%s/cache_bypass_misses' % (dev, t)))
                  interval_st = [bypassed, cache_hits, cache_misses, cache_bypass_hits, cache_bypass_misses]
             info.append(interval_st)
    return info

#find all uuid of cache devices
def bcache_uuids():
    uuids = []

    if not os.path.isdir(SYSFS_BCACHE_PATH):
        print('# bcache is not loaded.')
        return uuids

    for cache in os.listdir(SYSFS_BCACHE_PATH):
        if not os.path.isdir('%s%s' % (SYSFS_BCACHE_PATH, cache)):
            continue
        uuids.append(cache)

    return uuids

def main():
    uuids = bcache_uuids()
    #print uuids
    for uuid in uuids:
        devices = map_uuid_to_bcache(uuid)
        #print devices
        cache_info = get_cache_device_info(uuid)
        print '=======SSD: %s=====' %uuid
        print '--size--written--metadat--btree--btree-cache-size--'
        print cache_info
        devices.sort()
        for device in devices:
             print '========HDD: %s======' %device
             backing_info = get_backing_device_info(device)
             print '--dirty_data----sequtial_cutoff--'
             print backing_info
             backing_status = get_backing_device_stat(device)
             print '---five_minute---hour---day---total---'
             print '--bypassed--cache_hits--cache_misses--cache_bypass_hits--cache_bypass_misses--'
             print backing_status
        print '\n'
    print '\n'


if __name__ == '__main__':
    main()

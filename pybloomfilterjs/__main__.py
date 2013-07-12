# -*- coding: utf-8 -*-
import sys
from filter import BloomFilter

try:
    m = int(sys.argv[1])
    k = int(sys.argv[2])
    values = sys.argv[3:]
    assert len(values) > 0
except:
    print "Usage: {0} <m> <k> <value1> [value2 value3 ...]".format(sys.argv[0])
    sys.exit(1)

bloom = BloomFilter(m, k)
for val in values:
    bloom.add(val)
while 1:
    try:
        test_val = raw_input()
    except KeyboardInterrupt:
        sys.exit(0)
    if not test_val:
        sys.exit(0)
    if bloom.test(test_val):
        print "true"
    else:
        print "false"

# -*- coding: utf-8 -*-
import struct
from hash import fnv_1a, fnv_1a_b

class BloomFilter(object):
    def __init__(self, m, k):
        self.m = m
        self.k = k
        n = m/32 + (1 if m%32 else 0) # 32 bits per bucket
        self.buckets = [0] * n
        self._locations = [0] * k

    def locations(self, value):
        r = self._locations
        a = fnv_1a(value)
        b = fnv_1a_b(a)
        x = a % self.m
        for i in range(self.k):
            r[i] = (x + self.m) if x < 0 else x
            x = (x + b) % self.m
        return r

    def add(self, value):
        """Add value"""
        l = self.locations(value)
        for i in range(self.k):
            self.buckets[l[i]/32] |= 1 << (l[i] % 32)

    def test(self, value):
        """Test value membership"""
        l = self.locations(value)
        for i in range(self.k):
            b = l[i]
            if (self.buckets[b/32] & (1 << (b % 32))) == 0:
                return False
        return True

    def encode_base2(self):
        binbuckets = []
        for b in self.buckets:
            binbuckets.append(''.join(str((b>>i)&1) for i in range(31)))
        return ''.join(binbuckets)[:self.m]

    def encode_octets(self):
        octbuckets = []
        for b in self.buckets:
            octbuckets.append(struct.pack('I', b))
        return ''.join(octbuckets)[:self.m/8 + (1 if self.m%8 else 0)]


if __name__ == "__main__":
    bloom = BloomFilter(32, 16)
    bloom.add("foo")
    bloom.add("bar")

    print "test foo:", bloom.test("foo")
    print "test bar:", bloom.test("bar")
    print "test blah:", bloom.test("blah")
    print "bucket contents:", bloom.buckets
    print "base2 encoding:", bloom.encode_base2()
    print "octet encoding:", repr(bloom.encode_octets())

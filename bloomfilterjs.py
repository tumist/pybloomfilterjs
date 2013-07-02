# -*- coding: utf-8 -*-
import struct
from ctypes import c_uint32, c_int32

FNV_prime = 0x01000193

def fnv_1a(message):
    if isinstance(message, str):
        message = [ord(c) for c in message]
    else:
        raise ValueError
    # XOR and multiplication in javascript implementation
    # simulates C uint32 behavior.
    digest = c_uint32(0x811c9dc5)
    for c in message:
        digest.value ^= c
        digest.value *= FNV_prime
    # The following is not a part of FNV_1A but modifictations suggested for
    # good avalance behavior and uniform distribution, see:
    #  http://home.comcast.net/~bretm/hash/6.html
    # Overflows for this part should behave like javascripts' number type
    digest = c_int32(digest.value)
    digest.value += digest.value << 13
    digest.value ^= digest.value >> 7
    digest.value += digest.value << 3
    digest.value ^= digest.value >> 17
    digest.value += digest.value << 5
    return digest.value

def fnv_1a_b(digest):
    if not isinstance(digest, c_int32):
        digest = c_int32(digest)
    digest.value += (digest.value << 1) + \
                    (digest.value << 4) + \
                    (digest.value << 7) + \
                    (digest.value << 8) + \
                    (digest.value << 24);
    digest.value += digest.value << 13;
    digest.value ^= digest.value >> 7;
    digest.value += digest.value << 3;
    digest.value ^= digest.value >> 17;
    digest.value += digest.value << 5;
    return digest.value


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

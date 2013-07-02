# -*- coding: utf-8 -*-
from ctypes import c_uint32 as uint32
from ctypes import c_int32 as int32

FNV_prime = 0x01000193

def fnv_1a(message):
    digest = uint32(2166136261) # C xor and multiplication
    if isinstance(message, str):
        message = [ord(c) for c in message]
    for c in message:
        digest.value ^= c
        digest.value *= FNV_prime
    # "mod" part
    digest = int32(digest.value) # JavaScript bitshift
    digest.value += digest.value << 13
    digest.value ^= digest.value >> 7
    digest.value += digest.value << 3
    digest.value ^= digest.value >> 17
    digest.value += digest.value << 5
    return digest.value

def fnv_1a_b(digest):
    if not isinstance(digest, int32):
        digest = int32(digest)
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
        n = m/32 + (1 if m%32 else 0)
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
        l = self.locations(value)
        for i in range(self.k):
            self.buckets[l[i]/32] |= 1 << (l[i] % 32)

    def test(self, value):
        l = self.locations(value)
        for i in range(self.k):
            b = l[i]
            if (self.buckets[b/32] & (1 << (b % 32))) == 0:
                return False
        return True


if __name__ == "__main__":
    bloom = BloomFilter(32, 16)
    bloom.add("foo")
    bloom.add("bar")

    print bloom.test("foo")
    print bloom.test("bar")
    print bloom.test("blah")

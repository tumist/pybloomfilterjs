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
    pass


if __name__ == "__main__":
    print fnv_1a("tumi")
    print fnv_1a("")

    print fnv_1a_b(fnv_1a("tumi"))
    print fnv_1a_b(fnv_1a(""))

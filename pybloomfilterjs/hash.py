# -*- coding: utf-8 -*-
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Port of bloomfilter-test.js"""
import unittest
from pybloomfilterjs import BloomFilter

class TestBloomFilter(unittest.TestCase):
    def test_basic(self):
        bf = BloomFilter(1000, 4)
        n1 = "Bess"
        n2 = "Jane"
        bf.add(n1)
        self.assertTrue(bf.test(n1))
        self.assertFalse(bf.test(n2))

    def test_jabberwocky(self):
        s1 = """`Twas brillig, and the slithy toves
  Did gyre and gimble in the wabe:
All mimsy were the borogoves,
  And the mome raths outgrabe.

"Beware the Jabberwock, my son!
  The jaws that bite, the claws that catch!
Beware the Jubjub bird, and shun
  The frumious Bandersnatch!"

He took his vorpal sword in hand:
  Long time the manxome foe he sought --
So rested he by the Tumtum tree,
  And stood awhile in thought.

And, as in uffish thought he stood,
  The Jabberwock, with eyes of flame,
Came whiffling through the tulgey wood,
  And burbled as it came!

One, two! One, two! And through and through
  The vorpal blade went snicker-snack!
He left it dead, and with its head
  He went galumphing back.

"And, has thou slain the Jabberwock?
  Come to my arms, my beamish boy!
O frabjous day! Callooh! Callay!'
  He chortled in his joy.

`Twas brillig, and the slithy toves
  Did gyre and gimble in the wabe;
All mimsy were the borogoves,
  And the mome raths outgrabe."""
        bf = BloomFilter(1000, 4)
        s2 = s1 + "\n"
        bf.add(s1)
        self.assertTrue(bf.test(s1))
        self.assertFalse(bf.test(s2))

    def test_wtf(self):
        bf = BloomFilter(20, 10)
        bf.add("abc")
        self.assertFalse(bf.test("wtf"))

    def test_works_with_int(self):
        bf = BloomFilter(1000, 4)
        bf.add(1)
        self.assertTrue(bf.test(1))
        self.assertFalse(bf.test(2))

if __name__ == '__main__':
    unittest.main()

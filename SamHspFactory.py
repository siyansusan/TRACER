# =========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
# Author: Siyan Liu
# =========================================================================
from __future__ import (absolute_import, division, print_function,
                        unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
                      chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

from SamHSP import SamHSP
from SamRecord import SamRecord
from CigarString import CigarString


class SamHspFactory:
    """
    This class manufactures HSPs from SAM records

    Attributes:
        keepOps : set of string
    Instance Methods:
        factory=SamHspFactory()
        HSPs=factory.makeHSPs(SamRecords)
    Private Methods:
        cigar=self.processCigar(cigar)
    Class Methods:
        none
    """

    def __init__(self):
        self.keepOps = set(["M", "I", "D", "=", "X"])

    def makeHSPs(self, reads):
        """
        Given a set of SamRecord objects, this function computes intervals of
        local alignments and manufactures a set of HSPs.
        """
        HSPs = []
        for read in reads:
            cigar = read.getCigar()
            cigar.computeIntervals(read.getRefPos())
            cigar = self.processCigar(cigar)
            hsp = SamHSP(read, cigar)
            HSPs.append(hsp)
        return HSPs

    def processCigar(self, cigar):
        """
        This processes a CIGAR string by removing soft-mask and other unwanted
        ops
        """
        keepOps = self.keepOps
        keep = []
        n = cigar.length()
        for i in range(n):
            op = cigar[i]
            if op.getOp() in keepOps:
                keep.append(op)
        new = CigarString("")
        new.setOps(keep)
        return new

#!/usr/bin/env python

# The MIT License (MIT)
# 
# Copyright (c) 2015 Brian Pursley
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys, argparse

class ComparisonNetwork(list):

    def sortBinarySequence(self, sequence):
        result = sequence
        for l in self:
            for c in l:
                if (result >> c[0]) & 1 < (result >> c[1]) & 1:
                    result = (result - 2**c[1]) | 2**c[0]
        return result
        
    def sortSequence(self, sequence):
        result = list(sequence)
        for l in self:
            for c in l:
                if result[c[0]] > result[c[1]]:
                    result[c[0]], result[c[1]] = result[c[1]], result[c[0]]
        return result


    #ugly implemention of drawing the network
    def svg(self, n):
        scale = 1
        xscale = scale * 35
        yscale = scale * 20
        
        innerResult = ''
        x = xscale
        for l in self:
            x += xscale
            usedInputs = []
            sa = 0
            hflag = 1
            for c in l:
                for ui in usedInputs:
                    if ui != []:
                        if ((c[0] > ui[0] and c[0] < ui[1] ) or (c[1] > ui[0] and c[1] < ui[1] )):
                            sa += 1
                            x += xscale / 3
                            hflag = 0
                            break
                        if (c[0] < ui[1]):
                            hflag = 0
                
                if usedInputs !=[] and hflag == 1 and sa > 0:
                    x -= sa * xscale /3
                    hflag = 0
                    sa = 0

                y0 = yscale + c[0] * yscale
                y1 = yscale + c[1] * yscale
                innerResult += "<circle cx='%s' cy='%s' r='%s' style='stroke:black;stroke-width:1;fill=yellow' />"%(x, y0, 3)
                innerResult += "<line x1='%s' y1='%s' x2='%s' y2='%s' style='stroke:black;stroke-width:%s' />"%(x, y0, x, y1, 1)
                innerResult += "<circle cx='%s' cy='%s' r='%s' style='stroke:black;stroke-width:1;fill=yellow' />"%(x, y1, 3)
                hflag = 1
                usedInputs.append(c)
            
        w = x + xscale
        h = (n + 1) * yscale
        result = "<?xml version='1.0' encoding='utf-8'?>"
        result += "<!DOCTYPE svg>"
        result += "<svg viewBox='0 0 %s %s' style='background: white' xmlns='http://www.w3.org/2000/svg'>"%(w, h)
        for i in range(0, n):
            y = yscale + i * yscale
            result += "<line x1='%s' y1='%s' x2='%s' y2='%s' style='stroke:black;stroke-width:%s' />"%(0, y, w, y, 1)
        result += innerResult
        result += "</svg>"
        return result

class SortingNetwork():
    def __init__(self, n):
        self.checkN(n)
        self.n = n

    #keep n = 2^k
    def checkN(self, n):
        while n > 1:
            assert n % 2 == 0, "suppose n = 2^k"
            n /= 2

    def half_cleaner(self, start, n):
        hc = []
        assert n % 2 ==0, "for a half cleaner, n should be an even"
        for i in range(0, n/2):
            hc += [[i+start,i+start+n /2]]
        return [hc]

    def bitonic_sorter(self, start, n):
        if n == 2:
            bs  = self.half_cleaner(start,n)
            return bs
        bs = []
        bs += self.half_cleaner(start, n)
        bs1 = self.bitonic_sorter(start, n/2)
        bs2 = self.bitonic_sorter(start + n/2, n/2)
        bs += self.merge2list(bs1,bs2)
        return bs

    def merge2list(self, l1,l2):
        assert len(l1) == len(l2), "merged two list should have the same length"
        for i in range(0, len(l1)):
            l1[i] += l2[i]
        return l1

    def merger(self, start, n):
        m = []
        hc = []
        for i in range(0,n/2):
            hc += [[i+start, start+n-i-1]]
        m += [hc]
        bs1 = self.bitonic_sorter(start,n/2)
        bs2 = self.bitonic_sorter(start+n/2,n/2)
        m += self.merge2list(bs1,bs2)
        return m

    def sorter(self,start,n):
        if n == 2:
            return [[[start,start + 1]]]
        s = []
        s1 = self.sorter(start,n/2)
        s2 = self.sorter(start+n/2,n/2)
        s += self.merge2list(s1,s2)
        s += self.merger(start,n)
        return s

    def sortingnetwork(self):
        return self.sorter(0, self.n)
        
def readComparisonNetwork(filename):
    cn = ComparisonNetwork()
    if filename:
        with open(filename, 'r') as f:
            for line in f:
                cn += eval(line)
    else:
        for line in sys.stdin:
            cn += eval(line)
    return cn

def generateComparisonNetwork(lists):
    cn = ComparisonNetwork(lists)
    return cn

        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", metavar="N", type=int, help="specify a file containing comparison network definition")
    parser.add_argument("-s", "--sort", metavar="list", nargs='?', const='', help="sorts the list using the input comparison network")
    parser.add_argument("--svg", metavar="outputfile", nargs='?', const='', help="generate SVG")
    args = parser.parse_args()

    n = args.input
    sn = SortingNetwork(n)
    cn = generateComparisonNetwork(sn.sortingnetwork())
    
    if args.svg or args.svg == "":
        if args.svg == "":
            print cn.svg(n)
        else:
            with open(args.svg, "w") as f:
                f.write(cn.svg(n))

    if args.sort or args.sort == "":
        if args.sort == "":
            inputSequence = eval(sys.stdin.readline())
        else:
            inputSequence = eval(args.sort)
        print cn.sortSequence(inputSequence)
        
if __name__ == "__main__":
    main()

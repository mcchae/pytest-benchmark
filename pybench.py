#!/usr/bin/env python
#coding=utf-8

##########################################################################################
import os
from random import randint, shuffle
from datetime import datetime
from tempfile import NamedTemporaryFile

##########################################################################################
LOOP=10000
IO_LOOP=(1024*1024/10) # if block=1024 then this means 1G (1024*1024*1024)
ITERATIONS=5
ROUNDS=3

##########################################################################################
class cpu_bench(object):
    #=====================================================================================
    @staticmethod
    def seq_sum_loop(loop=LOOP):
        _sum = 0
        for i in xrange(loop):
            _sum += i
        return loop, _sum
    #=====================================================================================
    @staticmethod
    def seq_sum_now_loop(loop=LOOP):
        _sum = 0
        for i in xrange(loop):
            _sum += i
            now = datetime.now()
        return loop, _sum
    #=====================================================================================
    @staticmethod
    def rnd_sum_loop(loop=LOOP):
        _sum = 0
        for i in xrange(loop):
            _sum += randint(i, loop)
        return loop, _sum
    #=====================================================================================
    @staticmethod
    def F(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return cpu_bench.F(n - 1) + cpu_bench.F(n - 2)
    #=====================================================================================
    @staticmethod
    def fiboncci_loop(loop=20):
        _sum = 0
        for i in xrange(loop):
            _sum += cpu_bench.F(loop)
        return loop, _sum

##########################################################################################
def get_rnd_ndx(loop):
    rndndx = range(loop)
    shuffle(rndndx)
    return rndndx

##########################################################################################
class mem_bench(object):
    rndndx = get_rnd_ndx(LOOP)
    #=====================================================================================
    @staticmethod
    def list_seq_op(loop=LOOP):
        l = []
        for i in xrange(loop):
            l.append(i)
        _sum = 0
        for i in xrange(loop):
            _sum += l[i]
    #=====================================================================================
    @staticmethod
    def list_rnd_op(loop=LOOP):
        l = []
        # rndndx = range(loop)
        # shuffle(rndndx)
        for i in xrange(loop):
            l.append(i)
        _sum = 0
        for i in mem_bench.rndndx:
            _sum += l[i]
    #=====================================================================================
    @staticmethod
    def hash_seq_op(loop=LOOP):
        l = {}
        for i in xrange(loop):
            l['<<<%s>>>'%i] = i
        _sum = 0
        for i in xrange(loop):
            _sum += l['<<<%s>>>'%i]
    #=====================================================================================
    @staticmethod
    def hash_rnd_op(loop=LOOP):
        l = {}
        for i in xrange(loop):
            l['<<<%s>>>'%i] = i
        _sum = 0
        for i in mem_bench.rndndx:
            _sum += l['<<<%s>>>'%i]

##########################################################################################
class io_bench(object):
    rndndx = get_rnd_ndx(IO_LOOP)
    tmpfile = None
    #=====================================================================================
    @staticmethod
    def write_seq_op(loop=IO_LOOP, block=1024):
        io_bench.tmpfile = NamedTemporaryFile(delete=False)
        with io_bench.tmpfile as ofp:
            for i in xrange(loop):
                ofp.write('%s\n'%(str(i%10)*(block-1),))
    #=====================================================================================
    @staticmethod
    def read_seq_op(loop=1024*1024, block=1024):
        with open(io_bench.tmpfile.name, 'r') as ifp:
            for i in xrange(loop):
                bk = ifp.read(1024)
    #=====================================================================================
    @staticmethod
    def read_rnd_op(loop=1024*1024, block=1024):
        with open(io_bench.tmpfile.name, 'r') as ifp:
            for i in io_bench.rndndx:
                ifp.seek(i * block)
                bk = ifp.read(1024)
    #=====================================================================================
    @staticmethod
    def write_rnd_op(loop=1024*1024, block=1024):
        with open(io_bench.tmpfile.name, 'w') as ofp:
            for i in io_bench.rndndx:
                ofp.seek(i * block)
                ofp.write('%s\n'%(str(i%10)*(block-1),))
        os.remove(io_bench.tmpfile.name)

##########################################################################################
def test_cpu_seq_sum_loop(benchmark):
    benchmark.pedantic(cpu_bench.seq_sum_loop, iterations=ITERATIONS, rounds=ROUNDS)
##########################################################################################
def test_cpu_seq_sum_now_loop(benchmark):
    benchmark.pedantic(cpu_bench.seq_sum_now_loop, iterations=ITERATIONS, rounds=ROUNDS)
##########################################################################################
def test_cpu_rnd_sum_loop(benchmark):
    benchmark.pedantic(cpu_bench.rnd_sum_loop, iterations=ITERATIONS, rounds=ROUNDS)
##########################################################################################
def test_cpu_fiboncci_loop(benchmark):
    benchmark.pedantic(cpu_bench.fiboncci_loop, iterations=ITERATIONS, rounds=ROUNDS)

##########################################################################################
def test_mem_list_seq_op(benchmark):
    benchmark.pedantic(mem_bench.list_seq_op, iterations=ITERATIONS, rounds=ROUNDS)
##########################################################################################
def test_mem_list_rnd_op(benchmark):
    benchmark.pedantic(mem_bench.list_rnd_op, iterations=ITERATIONS, rounds=ROUNDS)
##########################################################################################
def test_mem_hash_seq_op(benchmark):
    benchmark.pedantic(mem_bench.hash_seq_op, iterations=ITERATIONS, rounds=ROUNDS)
##########################################################################################
def test_mem_hash_rnd_op(benchmark):
    benchmark.pedantic(mem_bench.hash_rnd_op, iterations=ITERATIONS, rounds=ROUNDS)

##########################################################################################
def test_io_write_seq_op(benchmark):
    benchmark.pedantic(io_bench.write_seq_op, iterations=ITERATIONS, rounds=ROUNDS)
##########################################################################################
def test_io_read_seq_op(benchmark):
    benchmark.pedantic(io_bench.read_seq_op, iterations=ITERATIONS, rounds=ROUNDS)
##########################################################################################
def test_io_read_rnd_op(benchmark):
    benchmark.pedantic(io_bench.read_rnd_op, iterations=ITERATIONS, rounds=ROUNDS)
##########################################################################################
def test_io_write_rnd_op(benchmark):
    benchmark.pedantic(io_bench.write_rnd_op, iterations=ITERATIONS, rounds=ROUNDS)


# ##########################################################################################
# def mytest():
#     io_bench.write_seq_op()
#     io_bench.read_seq_op()
#
# ##########################################################################################
# if __name__ == '__main__':
#     mytest()

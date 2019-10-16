#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <mail@fabienm.eu>
# Created:  14/10/2019
#-----------------------------------------------------------------------------

from collections import namedtuple
import logging

from cocotb import SimLog, coroutine
from cocotb.drivers import Driver
from cocotb.monitors import Monitor
from cocotb.result import TestError
from cocotb.result import ReturnValue 
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.utils import get_time_from_sim_steps, get_sim_steps

SPISignals = namedtuple("SPISignals", ['miso', 'mosi', 'sclk', 'cs'])

class SPIConfig(object):
    """ SPI parameters """
    def __init__(self, *, cpol=False, cpha=True, baudrate=(1, "us"),
                 csphase=False, loglevel=logging.INFO):
        self.cpol = cpol
        self.cpha = cpha
        self.baudrate = baudrate
        self.csphase = csphase
        self.loglevel = loglevel


    def __setattr__(self, key, value):
        if key == "cpol":
            if value != False:
                raise TypeError("cpol = True not implemented yet")
        elif key == "cpha":
            if value != True:
                raise TypeError("cpha = False not implemented yet")
        self.__dict__[key] = value

class SPIModule(Driver, Monitor):
    """ test class for SPI """

    def __init__(self, config, signals, clk, *, clk_freq=None):
        self.log = SimLog("cocomod.spi.{}".format(self.__class__.__name__))
        self.log.setLevel(config.loglevel)
        self.config = config
        self.clk = clk
        if clk_freq is None:
            clk_freq = 1 / get_time_from_sim_steps(clk.period, "sec")
        self.miso = signals.miso
        self.mosi = signals.mosi
        self.cs = signals.cs
        self.sclk = signals.sclk

        Driver.__init__(self)
        Monitor.__init__(self)

    def sig_init(self):
        self.mosi <= 0
        self.sclk <= 0
        self.cs <= self.config.csphase

    def set_cs(self, enable):
        if enable:
            self.cs <= not self.config.csphase
        else:
            self.cs <= self.config.csphase

    @coroutine
    def read(self, address, sync=True):
        """ Reading value on SPI """
        raise Exception("TODO: read a value on SPI with read()")

    @coroutine
    def write(self, address, values_list):
        """ Writing value on SPI"""
        raise Exception("TODO: write values on SPI with write()")

    @coroutine
    def _driver_send(self, transaction, sync=True, **kwargs):
        #raise Exception("TODO: implement _driver_send for spi driver")
        yield Timer(1)

    @coroutine
    def _monitor_recv(self):
        miso_list = []
        mosi_list = []
        self.log.warning("TODO: implement spi monitor function _monitor_recv")
        while True:
            yield Timer(10, units="us") # XXX
            self._recv((miso_list, mosi_list))

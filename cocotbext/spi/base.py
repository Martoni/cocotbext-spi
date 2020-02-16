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
                raise NotImplementedError("cpol=True not fully implemented yet")
        elif key == "cpha":
            if value != True:
                raise NotImplementedError("cpha=False not fully implemented yet")
        self.__dict__[key] = value

class SPIModule(Driver, Monitor):
    """ Test class for SPI """

    def __init__(self, config, signals, clk, *, clk_freq=None):
        self.log = SimLog("cocotbext.spi.{}".format(self.__class__.__name__))
        self.log.setLevel(config.loglevel)
        self.config = config
        self.clk = clk
        if clk_freq is None:
            clk_freq = 1 / get_time_from_sim_steps(clk.period, "sec")
        self.miso = signals.miso
        self.mosi = signals.mosi
        self.cs = signals.cs
        self.sclk = signals.sclk

        # chip select Edging
        if self.config.csphase:
            self.csBeginEdge = RisingEdge(self.cs)
            self.csEndEdge = FallingEdge(self.cs)
        else:
            self.csBeginEdge = FallingEdge(self.cs)
            self.csEndEdge = RisingEdge(self.cs)

        # sclk edging
        # CPOL  | leading edge | trailing edge
        # ------|--------------|--------------
        # false | rising       | falling
        # true  | falling      | rising
        if self.config.cpol:
            self.sclkLeadEdge = FallingEdge(self.sclk)
            self.sclkTrailEdge = RisingEdge(self.sclk)
        else:
            self.sclkLeadEdge = RisingEdge(self.sclk)
            self.sclkTrailEdge = FallingEdge(self.sclk)

        # CPHA  | data change    | data read
        # ------|----------------|--------------
        # false | trailling edge | leading edge
        # true  | leading edge   | trailing edge
        if self.config.cpha:
            self.dataChangEdge = self.sclkLeadEdge
            self.dataReadEdge = self.sclkTrailEdge
        else:
            self.dataChangEdge = self.sclkTrailEdge
            self.dataReadEdge = self.sclkLeadEdge

        Driver.__init__(self)
        Monitor.__init__(self)

    def sig_init(self):
        self.mosi <= 0
        self.sclk <= 0
        self.cs <= int(not self.config.csphase)

    def set_cs(self, enable):
        if enable:
            self.cs <= int(self.config.csphase)
        else:
            self.cs <= int(not self.config.csphase)

    @coroutine
    def read(self, address, sync=True):
        """ Reading value on SPI """
        raise NotImplementedError("TODO: read a value on SPI with read()")

    @coroutine
    def write(self, address, values_list):
        """ Writing value on SPI"""
        raise NotImplementedError("TODO: write values on SPI with write()")

    @coroutine
    def _driver_send(self, transaction, sync=True, **kwargs):
        short_per = Timer(100, units="ns")
        sclk_per = Timer(self.config.baudrate[0],
                         units=self.config.baudrate[1])
        #initial state
        self.sclk <= 0
        yield sclk_per

        for i in range(8):
            self.sclk <= 1
            self.mosi <= (transaction >> (7-i)) & 0x01
            yield sclk_per
            self.sclk <= 0
            yield sclk_per

    @coroutine
    def _monitor_recv(self):
        while True:
            miso = ""
            mosi = ""
            yield self.csBeginEdge
            while int(self.cs) == int(self.config.csphase):
                trig = yield [self.dataReadEdge, self.csEndEdge]
                if trig == self.dataReadEdge:
                    miso = miso + self.miso.value.binstr
                    mosi = mosi + self.mosi.value.binstr
            values_recv = {"miso": miso, "mosi": mosi}
            self._recv(values_recv)

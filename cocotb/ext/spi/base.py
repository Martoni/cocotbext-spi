#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <mail@fabienm.eu>
# Created:  14/10/2019
#-----------------------------------------------------------------------------

from cocotb import SimLog, coroutine
from cocotb.drivers import Driver
from cocotb.monitors import Monitor
from cocotb.result import TestError
from cocotb.triggers import Timer, RisingEdge, FallingEdge

class SPIModule(Driver, Monitor):
    """ test class for SPI """

    def __init__(self, config, signals, clk, *, clk_freq=None):
        self.log = SimLog("cocomod.uart.{}".format(self.__class__.__name__))

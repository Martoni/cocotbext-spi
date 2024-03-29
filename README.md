
# /!\\ OBSOLETE /!\\
There is a cocotbext-spi concurent in pypi repository: https://pypi.org/project/cocotbext-spi/
How that's possible to have two project with same name in github ?

https://github.com/schang412/cocotbext-spi

schang412 seems to be more up-to-date module. I think mine will be deleted in futur. If you need spi simulation un cocotb, it's certainly safer to use schang412 module.


# cocotbext-spi
Protocol test extension for testing spi in cocotb


# install

To use this module the easyiest way is to

* clone the repository :
```shell
$ git clone https://github.com/Martoni/cocotbext-spi.git
```

* Then install it with pip (tested with python 3.7):
```shell
$ python -m pip install -e cocotbext-spi/
```

With this method if cocotbext-spi code is modified, modification will be taken
into account in your testbench directly. Without having to re-install module.

# How to use it

Simply include the module in your testbench :

```python
from cocotbext.spi import *
```

cocotbext-spi module include Master side test. The module SPIModule() is seen as a
SPI master and dut SPI interface as a slave.

## Master

cocotbext-spi is composed of two classes :
* `SPIConfig()`: to describe configuration
* `SPIModule()`: the test module inherit from Driver and Monitor.

And one Tuple for signals :
* `SPISignals` : used to give dut signals names.

Three steps should be done in initialization of your testbench (often in
`__init__()` function of your testbench).

1. Define dut pinout, filling the tuple :
```python
spi_sigs = SPISignals(miso=dut.miso,
                      mosi=dut.mosi,
                      sclk=dut.sclk,
                      cs=dut.csn)
```
2. Set configuration with class `SPIConfig`:
```python
self.spi_config = SPIConfig(cpol=False,
                            cpha=True,
                            baudrate=(1, "us"),
                            csphase=False)
```
3. Then instantiate the `SPIModule`:
```python
self.clock = cocotb.Clock(dut.clock, 10, units="ns")
self.spimod = SPIModule(self.spi_config, spi_sigs, self.clock)
```

In your reset procedure/function, init SPI signals with method
`sig_init()` without yield.

Once the bench started, a monitor will read permanently the two signals `mosi`
and `miso` and register values read.

Mosi is written with method `send(byte)` 8 bits by 8 bits. And chip select signal
must be toggled manually with `set_cs(True/False)`. For example to do a 16bits
data write with 7 bits addr + 1 bit R/W like for Spi2Wb components we will do :
```python
self.spimod.set_cs(True) # enable chip select
yield sclk_per
yield self.spimod.send(0x80|addr) # send 8 bits data 
yield self.spimod.send((value >> 8)&0x00FF) # value is 16bits then we
yield self.spimod.send(value&0x00FF)        # send it in two steps
yield sclk_per
self.spimod.set_cs(False) # disable chip select
```

For reading, we have to wait for monitor to receive values with :
```python
ret = yield self.spimod.wait_for_recv(1) # waiting for receive value
```

The return value is a dict of bitstring with mosi and miso value read in the
chip select interval :
```python
values_recv = {"miso": miso, "mosi": mosi}
```

A usage example can be seen for testbench part of project [Spi2Wb](https://github.com/Martoni/spi2wb/blob/master/cocotb/test_Spi2Wb.py).

## Slave

To be implemented

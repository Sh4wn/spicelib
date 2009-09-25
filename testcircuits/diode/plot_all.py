#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import popen2
import numpy
sys.path.append("../../../../scripts/")
import spice_read
from plotutils import load, plotter


def plot_forward_voltage():
    pp = plotter()
    labels = ["0C", "25C", "50C", "75C", "100C"]
    ret = 0

    plots = spice_read.spice_read("forward_voltage.data").get_plots()
    for n,pl in enumerate(plots):
        If = -pl.get_scalevector().get_data()
        Uf = pl.get_datavectors()[0].get_data()
        if numpy.any(Uf<0.0) or numpy.any(Uf>3.0):
            print "forward voltage out of expected range [0.0, 3.0]"
            ret = 1
        pp.semilogy(Uf, If*1000.0,label = labels[n])
    pp.ylabel("If [mA]")
    pp.xlabel("Uf [V]")
    pp.grid()
    pp.legend(loc="best")
    pp.savefig("dc_forward_voltage.png",dpi=80)
    pp.close()

    return ret


#################### MAIN

ME = sys.argv[0] + ": "

command = "gnetlist -g spice-sdb -l ../../../../scripts/geda-parts.scm -o dc_current.net dc_current.sch"

print ME, "creating netlist: ", command
pop = popen2.Popen4(command)
print pop.fromchild.read()
ret_gnetlist = pop.wait()
if ret_gnetlist != 0:
    print ME, "netlist creation failed with errorcode:", ret_gnetlist
else:
    print ME, "netlist creation was successful"

command = "ngspice -b ../../../../testcircuits/diode/simulate.ngspice"
print ME, "running simulation: ", command
pop = popen2.Popen4(command)
print pop.fromchild.read()
ret_simulation = pop.wait()
if ret_simulation != 0:
    print ME, "simulation failed with errorcode:", ret_simulation
else:
    print ME, "simulation run was successful"

print ME, "testing and plotting"
try:
    ret_plot = plot_forward_voltage()
except Exception, data:
    print ME, "plotting function died:"
    print data
    sys.exit(1)

if ret_plot == 0:
    print ME, "finished testing and plotting successfully"
    sys.exit(0)
else:
    print ME, "testing or plotting failed"
    sys.exit(2)

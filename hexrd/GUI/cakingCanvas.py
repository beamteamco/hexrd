#! /usr/bin/env python
# ============================================================
# Copyright (c) 2012, Lawrence Livermore National Security, LLC. 
# Produced at the Lawrence Livermore National Laboratory. 
# Written by Joel Bernier <bernier2@llnl.gov> and others. 
# LLNL-CODE-529294. 
# All rights reserved.
# 
# This file is part of HEXRD. For details on dowloading the source,
# see the file COPYING.
# 
# Please also see the file LICENSE.
# 
# This program is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License (as published by the Free Software
# Foundation) version 2.1 dated February 1999.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the terms and conditions of the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this program (see file LICENSE); if not, write to
# the Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA 02111-1307 USA or visit <http://www.gnu.org/licenses/>.
# ============================================================
#
"""Display for caking output.
"""
import wx

import numpy

from hexrd.XRD.Experiment  import PolarRebinOpts as prOpts

from hexrd.GUI.guiConfig import WindowParameters as WP
from hexrd.GUI.guiUtilities import makeTitleBar
from hexrd.GUI.canvasUtilities import *
#
# ---------------------------------------------------CLASS:  cakeCanvas
#
class cakeCanvas(wx.Panel):
    """cakeCanvas """
    def __init__(self, parent, id, cakeType, data, **kwargs):
	"""Constructor for cakeCanvas panel

        **INPUTS**
        *cakeType* - flag for type of analysis: full image caking, ring-based or spherical (omega-eta map)
        *data* - the object with data to be plotted caking, depending on *cakeType*
                 .. for rings case, a MultiRingBinned instance
                 .. for full image case, img_info (output of polarRebin)

        
        **OUTPUTS**
        *self* - this panel

        
        **DESCRIPTION**
        Shows data on output canvas.
"""
	#
	wx.Panel.__init__(self, parent, id, **kwargs)
	#
        #  Data
        #
        self.cakeType = cakeType
        self.data     = data
        #
	#  Window Objects.
	#
        self.__makeObjects()
	#
	#  Bindings.
	#
	self.__makeBindings()
	#
	#  Sizing.
	#
	self.__makeSizers()
	#
	self.SetAutoLayout(True)
        self.SetSizerAndFit(self.sizer)
        #
        self.opt_pan.update() # make initial plot
 	#
	return
    #
    # ============================== Internal Methods
    #
    def __makeObjects(self):
        """Add interactors"""

        self.tbarSizer = makeTitleBar(self, 'cakeCanvas')
        #
        #  see if we need cmPanel
        #
        #self.cmPanel = cmapPanel(self, wx.NewId())
        #self.cmPanel.Disable()
        #
        if   self.cakeType == prOpts.CAKE_IMG:
            self.opt_pan = imgOpts(self, wx.NewId())
            # full image caking panel
            pass
        elif self.cakeType == prOpts.CAKE_RNG:
            # multiring panel
            self.opt_pan = rngOpts(self, wx.NewId())
            pass
        elif self.cakeType == prOpts.CAKE_SPH:
            # omega-eta panel
            self.opt_pan = sphOpts(self, wx.NewId())
            pass
        
        self.__makeFigureCanvas()
        #

        return

    def __makeFigureCanvas(self):
        """Build figure canvas"""
        self.figure = Figure()
        self.canvas = FigureCanvas(self, wx.NewId(), self.figure)

        self.axes   = self.figure.gca()
        self.axes.set_aspect('equal')

        self.toolbar = NavigationToolbar2WxAgg(self.canvas)
        self.toolbar.Realize()
        self.toolbar.update()
        
        return

    def __makeBindings(self):
        """Bind interactors"""
        return

    def __makeSizers(self):
	"""Lay out the interactors"""
	
	self.sizer = wx.BoxSizer(wx.VERTICAL)
        #
	self.sizer.Add(self.tbarSizer, 0, wx.EXPAND|wx.ALIGN_CENTER)
        self.sizer.Show(self.tbarSizer, False)
	self.sizer.Add(self.opt_pan,   0, wx.EXPAND|wx.ALIGN_CENTER)
	self.sizer.Add(self.canvas,    1, wx.EXPAND|wx.ALIGN_CENTER)
	self.sizer.Add(self.toolbar,   0, wx.EXPAND|wx.ALIGN_CENTER)

	return
    #
    # ============================== API
    #
    #                     ========== *** Access Methods
    #
    #
    #                     ========== *** Event Callbacks
    #
    pass # end class
#
# -----------------------------------------------END CLASS:  cakeCanvas
# ---------------------------------------------------CLASS:  cakeDisplay
#
class cakeDisplay(wx.Frame):
    #
    def __init__(self, parent, id, cakeType, data, title=''):
        """
        INPUTS 
        cakeType -- full caking, ring-based or spherical (omega-eta map)
        data     -- caking output, depending on cakeType
        
        OUTPUTS
        
        DESCRIPTION
        Passes args to cakeCanvas
"""
        #
        #  Pass option dictionary or string.
        #
        wx.Frame.__init__(self, parent, id, title)
	#
        #  Data
        #
        self.cakeType = cakeType
        self.data     = data
        #
	#  Window Objects.
	#
        self.__makeObjects()
	#
	#  Bindings.
	#
	self.__makeBindings()
	#
	#  Sizing.
	#
	self.__makeSizers()
	#
	self.SetAutoLayout(True)    
        self.SetSizerAndFit(self.sizer)
        #
        self.Show(True)

	return
    #
    # ============================== Internal Methods
    #
    def __makeObjects(self):
        """Add interactors"""

        self.tbarSizer = makeTitleBar(self, 'Rebin Canvas')
        #
        #  Add canvas panel
        #
        self.cpan = cakeCanvas(self, wx.NewId(),  self.cakeType, self.data)    
	#
        # A Statusbar in the bottom of the window
        #
        self.CreateStatusBar()
	#
        # Creating the menubar.
        #
        # menuBar = wx.MenuBar()
        # self.CreateFileMenu()
        # menuBar.Append(self.filemenu,  "&File") 
        # self.CreateTableMenu()
        # menuBar.Append(self.tablemenu, "&Table")
        # 
        # self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        return

    def __makeBindings(self):
        """Bind interactors"""
        return

    def __makeSizers(self):
	"""Lay out the interactors"""
	
	self.sizer = wx.BoxSizer(wx.VERTICAL)
	self.sizer.Add(self.tbarSizer, 0, wx.EXPAND|wx.ALIGN_CENTER)
	self.sizer.Add(self.cpan,      1, wx.EXPAND|wx.ALIGN_CENTER)

	return
    #
    # ============================== API
    #
    #                     ========== *** Access Methods
    #

    #
    #                     ========== *** Event Callbacks
    #
    pass # class
#
# -----------------------------------------------END CLASS:  
# ---------------------------------------------------CLASS:  rngOpts
#
class rngOpts(wx.Panel):
    """rngOpts """
    unitList = ['d-spacing', 'radians', 'strain', 'degrees']
    
    def __init__(self, parent, id, **kwargs):
	"""Constructor for rngOpts."""
	#
	wx.Panel.__init__(self, parent, id, **kwargs)
	#
        #  Data
        #

        #
	#  Window Objects.
	#
        self.__makeObjects()
	#
	#  Bindings.
	#
	self.__makeBindings()
	#
	#  Sizing.
	#
	self.__makeSizers()
	#
	self.SetAutoLayout(True)
        self.SetSizerAndFit(self.sizer)
        
	return
    #
    # ============================== Internal Methods
    #
    def __makeObjects(self):
        """Add interactors"""

        self.tbarSizer = makeTitleBar(self, 'Multiring Rebinning Results')
        #
        self.unit_cho = wx.Choice(self, wx.NewId(), choices=rngOpts.unitList)
        self.exp_but  = wx.Button(self, wx.NewId(), 'Export')
	#self.Bind(wx.EVT_CHOICE, self.OnChoice, self.choice)
        
        return

    def __makeBindings(self):
        """Bind interactors"""
        self.Bind(wx.EVT_CHOICE, self.OnUpdate, self.unit_cho)
        self.Bind(wx.EVT_BUTTON, self.OnExport, self.exp_but)
        return

    def __makeSizers(self):
	"""Lay out the interactors"""
	
	self.sizer = wx.BoxSizer(wx.VERTICAL)
	self.sizer.Add(self.tbarSizer, 0, wx.EXPAND|wx.ALIGN_CENTER)
        self.sizer.Show(self.tbarSizer, False)
        self.sizer.Add(self.unit_cho, 0, wx.ALIGN_LEFT)
        self.sizer.Add(self.exp_but,  0, wx.ALIGN_LEFT|wx.TOP, 5)
        
	return
    #
    # ============================== API
    #
    #                     ========== *** Access Methods
    #
    def update(self):
        """Update canvas"""
        p = self.GetParent()
        u = self.unit_cho.GetStringSelection()
        
        self.errs = p.data.getTThErrors(units=u)
        
        p.figure.delaxes(p.axes)
        p.axes   = p.figure.gca()
        p.axes.plot(self.errs)
        p.axes.set_title('Errors')
        p.axes.set_ylabel(u)
        
        p.canvas.draw()
        
        return
    #
    #                     ========== *** Event Callbacks
    #
    def OnUpdate(self, e):
        """Update canvas"""
        self.update()
        return
    
    def OnExport(self, e):
        """Export results to a text file"""
        # export self.errs to a file
        dlg = wx.FileDialog(self, 'Export Binning Errors', style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            f = dlg.GetPath()
            try:
                numpy.savetxt(f, self.errs)
            except:
                wx.MessageBox('failed to save file:  %s' % f)
                pass
            pass


        dlg.Destroy()

        return
    
    pass # end class
#
# -----------------------------------------------END CLASS:  rngOpts
# ---------------------------------------------------CLASS:  imgOpts
#
class imgOpts(wx.Panel):
    """Options panel for IMG (standard) caking canvas"""

    def __init__(self, parent, id, **kwargs):
	"""Constructor for imgOpts."""
	#
	wx.Panel.__init__(self, parent, id, **kwargs)
	#
        #  Data
        #

        #
	#  Window Objects.
	#
        self.__makeObjects()
	#
	#  Bindings.
	#
	self.__makeBindings()
	#
	#  Sizing.
	#
	self.__makeSizers()
	#
	self.SetAutoLayout(True)
        self.SetSizerAndFit(self.sizer)

	return
    #
    # ============================== Internal Methods
    #
    def __makeObjects(self):
        """Add interactors"""

        self.tbarSizer = makeTitleBar(self, 'Full Image Rebinning Results')
        #

        return

    def __makeBindings(self):
        """Bind interactors"""
        return

    def __makeSizers(self):
	"""Lay out the interactors"""

	self.sizer = wx.BoxSizer(wx.VERTICAL)
	self.sizer.Add(self.tbarSizer, 0, wx.EXPAND|wx.ALIGN_CENTER)
        self.sizer.Show(self.tbarSizer, False)

	return
    #
    # ============================== API
    #
    #                     ========== *** Access Methods
    #
    def update(self):
        """Update canvas"""
        p = self.GetParent()

        intensity = p.data['intensity']

        p.axes = p.figure.gca()
        p.axes.set_aspect('equal')


        p.axes.images = []
        # show new image
        p.axes.imshow(intensity, origin='upper',
                      interpolation='nearest',
                      aspect='auto')
#                      cmap=self.cmPanel.cmap,
#                      vmin=self.cmPanel.cmin_val,
#                      vmax=self.cmPanel.cmax_val,
        p.axes.set_autoscale_on(False)

        p.canvas.draw()

        return
    #
    #                     ========== *** Event Callbacks
    #
    def OnUpdate(self, e):
        """Update canvas"""
        self.update()
        return

    def OnExport(self, e):
        """Export results to a text file"""
        # export self.errs to a file
        dlg = wx.FileDialog(self, 'Export Binning Data', style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            f = dlg.GetPath()
            try:
                wx.MessageBox('would save to file:  %s' % f)
                #exp.saveDetector(f)
            except:
                wx.MessageBox('failed to save file:  %s' % f)
                pass
            pass

        dlg.Destroy()

        return

    pass # end class
#
# -----------------------------------------------END CLASS:  imgOpts
# ---------------------------------------------------CLASS:  sphOpts
#
class sphOpts(wx.Panel):
    """Options panel for SPH (omega-eta) caking canvas"""

    def __init__(self, parent, id, **kwargs):
	"""Constructor for sphOpts."""
	#
	wx.Panel.__init__(self, parent, id, **kwargs)
	#
        #  Data
        #

        #
	#  Window Objects.
	#
        self.__makeObjects()
	#
	#  Bindings.
	#
	self.__makeBindings()
	#
	#  Sizing.
	#
	self.__makeSizers()
	#
	self.SetAutoLayout(True)
        self.SetSizerAndFit(self.sizer)

	return
    #
    # ============================== Internal Methods
    #
    def __makeObjects(self):
        """Add interactors"""

        self.tbarSizer = makeTitleBar(self, 'Full Image Rebinning Results')
        #

        return

    def __makeBindings(self):
        """Bind interactors"""
        return

    def __makeSizers(self):
	"""Lay out the interactors"""

	self.sizer = wx.BoxSizer(wx.VERTICAL)
	self.sizer.Add(self.tbarSizer, 0, wx.EXPAND|wx.ALIGN_CENTER)
        self.sizer.Show(self.tbarSizer, False)

	return
    #
    # ============================== API
    #
    #                     ========== *** Access Methods
    #
    def update(self):
        """Update canvas"""
        p = self.GetParent()

#omega#        print omeEta
#omega#        print dir(omeEta)
#omega#
#omega#        # Show some pole figures
#omega#        style = {'marker':'d',    'ls':'None', 'mec':'y',
#omega#                 'mfc'   :'None', 'ms':10.,    'mew':2}
#omega#
#omega#        res    = 100
#omega#        cmap   = self.cmPanel.cmap
#omega#        pt     = numpy.r_[1.0, 0.0, 0.0]
#omega#        pList  = [(pt, style)] # to do
#omega#        iHKL   = 0
#omega#        kwargs = dict(
#omega#            pfig=res,
#omega#            cmap=cmap,
#omega#            iData=iHKL,
#omega#            pointLists=pList,
#omega#            rangeVV=(0., 150.),
#omega#            drawColorbar=False,
#omega#            pfigDisplayKWArgs={'doY90Rot':False}          
#omega#            )
#omega#        pfig = omeEta.display(**kwargs)
#omega#
#omega#        print pfig, dir(pfig)
#omega#
#        intensity = p.data['intensity']
#
#        p.axes = p.figure.gca()
#        p.axes.set_aspect('equal')
#
#
#        p.axes.images = []
#        # show new image
#        p.axes.imshow(intensity, origin='upper',
#                      interpolation='nearest',
#                      aspect='auto')
##                      cmap=self.cmPanel.cmap,
##                      vmin=self.cmPanel.cmin_val,
##                      vmax=self.cmPanel.cmax_val,
#        p.axes.set_autoscale_on(False)
#
#        p.canvas.draw()
#
        return
    #
    #                     ========== *** Event Callbacks
    #
    def OnUpdate(self, e):
        """Update canvas"""
        self.update()
        return

    pass # end class
#
# -----------------------------------------------END CLASS:  sphOpts

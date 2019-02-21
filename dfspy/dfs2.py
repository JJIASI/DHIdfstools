# -*- coding: utf-8 -*-
"""
DHI dfs2 function for bathy

Author: Jiasi
"""

import numpy as np
import os
import clr
import datetime as dt

#MIKE SDK path
sdk_path = r'C:\Program Files (x86)\DHI\2016\MIKE SDK\bin'
dfs_dll = r'DHI.Generic.MikeZero.DFS.dll'
MIKE_EUM = r'DHI.Generic.MikeZero.EUM.dll'

# Set path to MIKE SDK
clr.AddReference(os.path.join(sdk_path, dfs_dll))
clr.AddReference('System')

# Import .NET libraries
import DHI.Generic.MikeZero.DFS as dfs


class dfs2():
    def __init__(self,filename=None):
        self.filename = filename
        
        if filename is not None:
            self.read_dfs2()
    
    def read_dfs2(self,filename=None):
        
        def ToNumpyArray(TwoDArray):
            xBound = TwoDArray.GetUpperBound(1)
            yBound = TwoDArray.GetUpperBound(0)
            npArray = np.zeros([xBound, yBound])
        
            for x in range(xBound):
                    for y in range(yBound):
                        npArray[x,y] = TwoDArray[y,x]
            return npArray
        if filename is None:
            filename = self.filename
        
        dfs2_data = dfs.DfsFileFactory.Dfs2FileOpen(filename)
        itemnames = [[n.Name, n.Quantity.UnitAbbreviation] for n in dfs2_data.ItemInfo]
        time_len = dfs2_data.FileInfo.TimeAxis.NumberOfTimeSteps
        time_step = dfs2_data.FileInfo.TimeAxis.TimeStep
        start_datetime = dt.datetime(year=dfs2_data.FileInfo.TimeAxis.StartDateTime.Year,
                              month=dfs2_data.FileInfo.TimeAxis.StartDateTime.Month,
                              day=dfs2_data.FileInfo.TimeAxis.StartDateTime.Day,
                              hour=dfs2_data.FileInfo.TimeAxis.StartDateTime.Hour,
                              minute=dfs2_data.FileInfo.TimeAxis.StartDateTime.Minute,
                              second=dfs2_data.FileInfo.TimeAxis.StartDateTime.Second)

        saxis = dfs2_data.SpatialAxis
        x = saxis.X0 + saxis.Dx*(np.array(range(0,saxis.XCount-1)))
        y = saxis.Y0 + saxis.Dy*(np.array(range(0,saxis.YCount-1)))
        for items,inames in enumerate(itemnames):
            
            for t in range(time_len):
                time_t = start_datetime+dt.timedelta(seconds=time_step*(t-1))
                time_str = time_t.strftime("%Y-%m-%d %H:%M:%S")
        
                dfs2_mat = dfs2_data.ReadItemTimeStep(items+1,t).To2DArray()            
                z_temp = {time_str:ToNumpyArray(dfs2_mat)}
            z = {inames[0]:z_temp}
            
        dfs2_data.Close()
        return x,y,z


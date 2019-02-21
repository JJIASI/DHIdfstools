# -*- coding: utf-8 -*-
"""
@author: Jiasi
"""

import numpy as np
import os
import clr
import pandas as pd
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


class dfs1():
    def __init__(self,filename=None):
        self.filename = filename
        
        if filename is not None:
            self.read_dfs1()
    def read_dfs1(self,filename=None):
        if filename is None:
            filename = self.filename
        #Open dfs1 data
        dfs1_data = dfs.DfsFileFactory.Dfs1FileOpen(filename)
        itemnames = [[n.Name, n.Quantity.UnitAbbreviation] for n in dfs1_data.ItemInfo]
        time_len = dfs1_data.FileInfo.TimeAxis.NumberOfTimeSteps
        time_step = dfs1_data.FileInfo.TimeAxis.TimeStep
        start_datetime = dt.datetime(year=dfs1_data.FileInfo.TimeAxis.StartDateTime.Year,
                                      month=dfs1_data.FileInfo.TimeAxis.StartDateTime.Month,
                                      day=dfs1_data.FileInfo.TimeAxis.StartDateTime.Day,
                                      hour=dfs1_data.FileInfo.TimeAxis.StartDateTime.Hour,
                                      minute=dfs1_data.FileInfo.TimeAxis.StartDateTime.Minute,
                                      second=dfs1_data.FileInfo.TimeAxis.StartDateTime.Second)
        
        #read data from dfs1
        output_data = pd.DataFrame([])
        for t in range(time_len):
            time_t = start_datetime+dt.timedelta(seconds=time_step*(t-1))
            time_str = time_t.strftime("%Y-%m-%d %H:%M:%S")
            for items,inames in enumerate(itemnames):
                data = dfs1_data.ReadItemTimeStep(items+1,t).Data
                data = np.array(data).tolist()
                Bound = data.GetUpperBound(0)
                npArray = []
                
                for i in range(Bound+1):
                    npArray.append(data[i])
                temp_data = pd.DataFrame({inames[0]:npArray})
                output_data =pd.concat([output_data,temp_data], axis=1, sort=False)
            output_data = {time_str:output_data}
        dfs1_data.Close()
        return output_data



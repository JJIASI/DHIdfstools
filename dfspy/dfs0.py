# -*- coding: utf-8 -*-
"""
DHI dfs0 read function

@author: Jiasi
"""

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
#import DHI.Generic.MikeZero.DFS.dfs0 as dfs0

class dfs0():
    def __init__(self,filename=None):
        self.filename = filename        
        
        if filename is not None:
            self.dfs0_data = self.dfs0_read(filename)
    def dfs0_read(self,filename = None):
        if filename is None:
            filename = self.filename
        
        #Open dfs0 data
        dfs_file = dfs.DfsFileFactory.DfsGenericOpen(filename)
        dfs0_data = dfs.dfs0.Dfs0Util.ReadDfs0DataDouble(dfs_file)
        start_datetime = dt.datetime(year=dfs_file.FileInfo.TimeAxis.StartDateTime.Year,
                              month=dfs_file.FileInfo.TimeAxis.StartDateTime.Month,
                              day=dfs_file.FileInfo.TimeAxis.StartDateTime.Day,
                              hour=dfs_file.FileInfo.TimeAxis.StartDateTime.Hour,
                              minute=dfs_file.FileInfo.TimeAxis.StartDateTime.Minute,
                              second=dfs_file.FileInfo.TimeAxis.StartDateTime.Second)
        #read data from dfs0
        output_data = pd.DataFrame([])
        cols = dfs0_data.GetUpperBound(1)
        for items in range(cols+1):
            Bound = dfs0_data.GetUpperBound(0)
            npArray = []    
            for i in range(1,Bound+1):
                npArray.append(dfs0_data[i,items])
            temp_data = pd.DataFrame(npArray)
            output_data =pd.concat([output_data,temp_data], axis=1, sort=False)
        
        #columns name
        cols_name = ['Time'];
        for i in range(0,dfs_file.ItemInfo.Count):
           cols_name.append(dfs_file.ItemInfo.Items[i].Name)
        output_data.columns = cols_name
        dfs_file.Close()        
        e_time = pd.DataFrame([start_datetime+dt.timedelta(seconds=output_data['Time'].iloc[i+1]) for i in range(len(output_data['Time'])-1)])
        output_data['Time'] = e_time
        return output_data



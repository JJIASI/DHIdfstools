# DHIdfsdools 
> Author: Jia-Si

--------------- 
### Read DHI MIKE dfs data, e.g. `dfs0`, `dfs1`, `dfs2`.
  
> DHI MIKE is commenly used in metocean analysis for harbor design, costal protection design...etc.  
> The `DHI MATLAB Toolbox` is complete, so I take this as my program reference.  
> And [`Rob Wall github`](https://github.com/robjameswall) program a good dhitools, I also take it as my reference.  

-------------------  
## Before use this tool.  
You have to install [MIKE SDK](https://www.mikepoweredbydhi.com/download/mike-2016/mike-sdk?ref=%7B181C63FF-2342-4C41-9F84-F93884595EF3%7D).  
And the requirement modules as follows.  
* `pandas`
* `numpy`
* `datetime`
  
## Setting  
Every `.py` files have a line to set MIKE SDK path in order to import SDK .NET libraries.
```
sdk_path = r'C:\Program Files (x86)\DHI\2016\MIKE SDK\bin'
```
In this line, you must fill in your `MIKE SDK` installation path.  

--------------------
## Example
* [dfs0](/demo/dfs0_demo.ipynb)
* [dfs1](/demo/dfs1_demo.ipynb)
* [dfs2](/demo/dfs2_demo.ipynb)

--------------------
  
  
If you have any other suggestions and recommendations, please feel free to contact.  
<jiasi.cv03g@g2.nctu.edu.tw>

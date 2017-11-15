import xarray as xr

from sausage import Reader


class NetcdfReader(Reader):


    def read(self):
        self._dataset = xr.open_dataset(self._filename)
        

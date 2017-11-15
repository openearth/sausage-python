from sausage import Writer


class NetcdfWriter(Writer):


    _ext = '.nc'


    def write(self, filename):
        filename = self.get_filepath(filename)
        self._dataset.to_netcdf(filename)

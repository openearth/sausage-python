import numpy as np

try:
    import oceanwaves as ow
    HAS_OCEANWAVES = True
except ModuleNotFoundError:
    HAS_OCEANWAVES = False

from sausage import Writer


class XBeachWaterlevelWriter(Writer):


    _ext = '.txt'
    _format = 'xbeach'
    _category = 'waterlevel'


    def write(self, filename):

        filename = self.get_filepath(filename)
        var = self._dataset
        data = np.hstack((var.coords['time'].values[:,np.newaxis],
                          var.values[:,0,:1]))

        np.savetxt(filename, data)

        self.register_file(filename)


class XBeachWaveSpectrumWriter(Writer):


    _ext = '.spc'
    _format = 'xbeach'
    _category = 'wavespectrum'


    def __init__(self, *args, **kwargs):
        if not HAS_OCEANWAVES:
            raise ModuleNotFoundError('Writing SWaN files is supported through the '
                                      '"oceanwaves" package, but the package is not '
                                      'installed.')
        super().__init__(*args, **kwargs)
    
                
    def write(self, filename):

        filename = self.get_filepath(filename)
        var = self._dataset
        data = ow.OceanWaves(
            frequency=var.coords['frequency'].values[1:],
            energy=var.values[:-1,0,:1]
        )
        data = data.as_directional(
            direction=np.arange(-180,180,15)
        )
        
        data.to_swan(filename)

        self.register_file(filename)
        

import subprocess
import numpy as np

from sausage import Compiler


class XBeachCompiler(Compiler):


    _filename = 'params.txt'
    
    _parameters = dict(
        wavemodel = 'surfbeat',
        wbctype = 'swan',
        tstop = 5 * 3600.,
        nx = 300,
        ny = 0,
        vardx = 1,
        xfile = 'x.txt',
        depfile = 'z.txt',
        thetamin = -180,
        thetamax = 180,
        dtheta = 360,
    )

    _files = dict(
        zs0file = 'waterlevel',
        bcfile = 'wavespectrum',
    )


    def compile(self):

        with open(self._filename, 'w') as fp:
            for k, v in self._parameters.items():
                self.writeln(fp, k, v)
            for k, v in self._files.items():
                if 'xbeach.%s' % v in self._config['files'].keys():
                    self.writeln(fp, k, self._config['files']['xbeach.%s' % v])

        # create dummy bathy
        x = np.arange(self._parameters['nx']+1).reshape((1,-1))
        z = np.zeros(x.shape)
        np.savetxt(self._parameters['xfile'], x)
        np.savetxt(self._parameters['depfile'], z)


    def run(self):
        subprocess.call('xbeach')


    def writeln(self, fp, key, value):
        fp.write('%-20s = %s\n' % (key, str(value)))



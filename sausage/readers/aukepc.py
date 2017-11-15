try:
    import aukepc
    HAS_AUKEPC = True
except ModuleNotFoundError:
    HAS_AUKEPC = False

from sausage import Reader


class AukepcReader(Reader):


    def __init__(self, *args, **kwargs):
        if not HAS_AUKEPC:
            raise ModuleNotFoundError('Reading AukePC files is supported through '
                                      'the "aukepc" package, but the package is not '
                                      'installed.')
        super().__init__(*args, **kwargs)

        
    def read(self):
        self._dataset = aukepc.Dataset(self._filename)
        

from abc import ABC, abstractmethod


class Compiler(ABC):
    '''Abstract Base Class for Compiler objects.

    Abstract Base Class to built Compiler objects. Any Writer should
    at least implement a `compile` and `run` method. These methods
    compile a fully described model schematization from registered
    files and run the newly generated model schematization
    respectively.

    '''


    _configfile = '.sausage' # compilation configuration file

    
    def __init__(self):
        '''Initialization'''
        
        self.config = dict()
        self.read_configuration()


    @abstractmethod
    def compile(self, filename):
        '''Implemnts compilation of registered files into model schematization'''
        
        pass


    @abstractmethod
    def run(self):
        '''Implements running of newly created model schematization'''
        
        pass    


    def load_configuration(self):
        '''Loads compilation configuration with registered files'''
        
        if os.path.exists(self._configfile):
            with open(self._configfile, 'r') as fp:
                self._config = json.load(fp)
        else:
            raise IOError('No compilation configuration found.')


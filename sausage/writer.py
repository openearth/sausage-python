from abc import ABC, abstractmethod
import json
import os


class Writer(ABC):
    '''Abstract Base Class for Writer objects.

    Abstract Base Class to built Writer objects. Any Writer should at
    least implement a `write` method. This method writes data from an
    `xarray.Dataset` object that is stored in the `_dataset`
    property.

    This class implements a `get_filepath` method that returns a
    proper file path for writing, including a class dependent
    extension. The class also implements a `register_file` method that
    can be used to register generated files to a local compilation
    configuration file.

    '''


    _ext = '.txt'            # file extension
    _format = None           # file format
    _category = None         # file category
    _configfile = '.sausage' # compilation configuration file

    
    def __init__(self, dataset):
        '''Initialization

        Parameters
        ----------
        dataset : xarray.Dataset
          Dataset to be written to file

        '''

        self._dataset = dataset


    @abstractmethod
    def write(self, filename):
        '''Implements writing of data to file'''

        pass


    def register_file(self, filename):
        '''Registers file in local compilation configuration

        Parameters
        ----------
        filename : str
          Name of file to be registered

        Raises
        ------
        ValueError
          If file format or category is not fully specified.

        '''

        if self._format is None:
            raise ValueError('Invalid writer object. Output format not specified.')
        if self._category is None:
            raise ValueError('Invalid writer object. Output category not specified.')

        # read existing configuration
        config = dict(
            files = dict(),
        )
        
        if os.path.exists(self._configfile):
            with open(self._configfile, 'r') as fp:
                config = json.load(fp)

        # update configuration
        key = '%s.%s' % (self._format, self._category)
        config['files'][key] = os.path.relpath(filename, os.getcwd())

        # write updated configuration
        with open(self._configfile, 'w') as fp:
            json.dump(config, fp, indent=4)

    
    def get_filepath(self, filename):
        '''Return absolute file path for output file

        Parameters
        ----------
        filename : str
          Input file path

        Returns
        -------
        str
          Output file path

        '''
        
        return os.path.abspath('%s%s' % (os.path.splitext(filename)[0], self._ext))
    

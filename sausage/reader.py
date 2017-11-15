from abc import ABC, abstractmethod


class Reader(ABC):
    '''Abstract Base Class for Reader objects.

    Abstract Base Class to built Reader objects. Any Reader should at
    least implement a `read` method. This method reads data into an
    `xarray.Dataset` object that is stored in the `_dataset`
    property. In case of a file pointer, the pointer should remain
    open after reading. The `close` method takes care of proper
    closing of any open pointers.

    This class implements in interface to be used with the `with`
    command. It also implements a `set_variable` method to select a
    specific variable from the dataset to be returned upon request.

    '''

    
    def __init__(self, filename):
        '''Initialization

        Parameters
        ----------
        filename : str
          Path to data file to be read

        '''
        
        self._filename = filename
        self._dataset = None
        self._variable = None

        self.read()


    def __enter__(self):
        pass


    def __exit__(self):
        self.close()


    def __repr__(self):
        return repr(self._dataset)


    @abstractmethod
    def read(self):
        '''Implements reading of data from file'''
        
        pass


    def close(self):
        '''Closes any open datasets'''
        
        if hasattr(self._dataset, 'close'):
            self._dataset.close()


    def set_variable(self, variable):
        '''Selects variable from dataset

        Checks is the given variable exists in the current dataset. If
        so, it registers that variable as the dataset so an
        `xarray.DataArray` is returned rather than an `xarray.Dataset`
        when the `dataset` property is requested. If not, it raises an
        exception.

        Parameters
        ----------
        variable : str
          Name of variable

        Raises
        ------
        ValueError
          If variable does not exist in dataset
        
        '''
        
        if variable in self._dataset.variables.keys():
            self._variable = variable
        else:
            raise ValueError('Variable "%s" not in dataset.' % variable)


    @property
    def dataset(self):
        '''Returns active dataset'''
        
        if self._variable is None:
            return self._dataset
        else:
            return self._dataset.data_vars[self._variable]


    @property
    def variable(self):
        '''Returns active variable'''
        
        return self._variable

    
    @classmethod
    def open_dataset(cls, filename):
        '''XArray comaptibility method'''
        
        return cls(filename)

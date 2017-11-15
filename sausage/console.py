import os
import json
import docopt
import logging

from sausage import readers
from sausage import writers
from sausage import compilers


def convert():
    '''sausage-convert : convert model input and output

    Usage:
        sausage-convert <path> <format_in> <format_out> [options]

    Positional arguments:
        path               path to input data
        format_in          input file format
        format_out         output file format

    Options:
        -h, --help         show this help message and exit
        --config=FILE      configuration file for conversion
        --verbose=LEVEL    write logging messages [default: 20]

    Supported input file formats are currently:
      - netcdf
      - aukepc
      - swan

    Supported output file formats are currently:
      - netcdf
      - swan
      - xbeach

    Input/output file formats can be namespaced. For example, to
    convert an AukePC file containing a water level time series to an
    XBeach water level input file the following *format_in* and 
    *format_out* can be specified:

        sausage-convert A1.SEQ aukepc:WHM01 xbeach:waterlevel

    '''

    arguments = docopt.docopt(convert.__doc__)

    # filenames
    if os.path.isdir(arguments['<path>']):
        logfile = os.path.join(arguments['<path>'], 'sausage.log')
    else:
        logfile = '%s.log' % os.path.splitext(arguments['<path>'])[0]
    
    # initialize file logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)-15s %(name)-8s %(levelname)-8s %(message)s',
                        filename=logfile)

    # initialize console logger
    console = logging.StreamHandler()
    console.setLevel(int(arguments['--verbose']))
    console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(console)

    # parse command line arguments
    format_in = arguments['<format_in>'].split(':', 1)
    format_out = arguments['<format_out>'].split(':', 1)
    path_out = os.path.split(arguments['<path>'])[1]
    
    # pick reader
    if format_in[0].upper() == 'NETCDF':
        reader = readers.NetcdfReader
    elif format_in[0].upper() == 'AUKEPC':
        reader = readers.AukepcReader
    elif format_in[0].upper() == 'SWAN':
        reader = readers.SwanReader
    else:
        raise ValueError('Unknown input file format: %s. Currently supported '
                         'formats are: netcdf, aukepc and swan.' % format_in[0])

    # pick writer
    writer = None
    if format_out[0].upper() == 'NETCDF':
        writer = writers.NetcdfWriter
    elif format_out[0].upper() == 'SWAN':
        writer = writers.SwanWriter
    elif format_out[0].upper() == 'XBEACH':
        if len(format_out) > 1:
            if format_out[1].upper() == 'WATERLEVEL':
                writer = writers.XBeachWaterlevelWriter
            elif format_out[1].upper() == 'WAVESPECTRUM':
                writer = writers.XBeachWaveSpectrumWriter
    if writer is None:
        raise ValueError('Unknown output file format: %s. Currently supported '
                         'formats are: netcdf, swan, xbeach:waterlevel, '
                         'xbeach:wavespectrum.' % format_out[1])

    # convert data
    reader = reader(arguments['<path>'])
    if len(format_in) > 1:
        reader.set_variable(format_in[1])
    writer(reader.dataset).write(path_out)
    reader.close()


def compile():
    '''sausage-compile : compile model schematization

    Usage:
        sausage-compile <format> [options]

    Positional arguments:
        format             output file format

    Options:
        -h, --help         show this help message and exit
        --run              run the model after compilation
        --config=FILE      configuration file for conversion
        --verbose=LEVEL    write logging messages [default: 20]

    Supported compiler formats are currently:
      - xbeach

    '''

    arguments = docopt.docopt(compile.__doc__)

    # filenames
    logfile = os.path.join('sausage.log')
    
    # initialize file logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)-15s %(name)-8s %(levelname)-8s %(message)s',
                        filename=logfile)

    # initialize console logger
    console = logging.StreamHandler()
    console.setLevel(int(arguments['--verbose']))
    console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(console)

    # pick compiler
    if arguments['<format>'].upper() == 'XBEACH':
        compiler = compilers.XBeachCompiler
    else:
        raise ValueError('Unknown compiler format: %s. Currently supported formats '
                         'are: xbeach.' % arguments['<format>'])

    # compile model schematization
    compiler = compiler()
    compiler.compile()

    # run model schematization
    if arguments['--run']:
        compiler.run()

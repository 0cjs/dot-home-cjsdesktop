#!/usr/bin/env python3

from    __future__ import print_function

from    configparser import ConfigParser, NoSectionError, NoOptionError
from    os.path import expanduser
import  sys

try:
    import  pytest
except ImportError: pass


def test_read_config():
    conf = parseconfig('sshmenus.inb4')
    assert 'Cynic Hosts' == conf.get('hosts-cynic', 'TITLE')
    with pytest.raises(NoOptionError):
        assert conf.get('hosts-cynic', 'badvalue')
    with pytest.raises(NoSectionError):
        assert conf.get('badsection', '')
    assert conf.get('hosts-cynic', '&dyadic')        # May use & in options
    assert 'TITLE' in conf.options('hosts-cynic')

def test_read_nonexistent_config():
    with pytest.raises(IOError):
        parseconfig(['/dev/null', '/not/a/file/i/am/pretty/sure'])

def parseconfig(files=None):
    if isinstance(files, str): files = [files]
    parser = ConfigParser()
    parser.optionxform = lambda opt: opt    # Disable converstion to lower case
    read = parser.read(files)
    unread = set(files) - set(read)
    if unread:
        raise IOError('File(s) not found: {}'.format(', '.join(unread)))
    return parser

REMOVE_AMP = str.maketrans('', '', '&')   # Remove all ampersands

def printsection(name, opts):
    print('DestroyMenu menu-{}'.format(name))
    print('AddToMenu menu-{}'.format(name))
    for key, value in opts:
        if key == 'TITLE':
            print('    + "{}"\tTitle'.format(value))
        elif value == 'NOP':
            print('    + ""\tNop')
        elif value.startswith('SUBMENU '):
            _, menuname = value.split(None, 1)
            print('    + "{}"\tPopup menu-{}'.format(key, menuname))
        else:
            print('    + "{}"\tExec choose xterm -title \'{}\' -e {}' \
                .format(key, key.translate(REMOVE_AMP), value))
    print()

def main(args=sys.argv[1:]):
    args = args or [expanduser('~/.fvwm/genconf/sshmenus')]
    conf = parseconfig(args)
    for section in conf.sections():
        printsection(section, conf.items(section))

if __name__ == '__main__':
    main()

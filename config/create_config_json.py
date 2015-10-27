import json
import os
import pprint
import sys

def main(bonfire_home, config_file):
    new_conf={}
    os.system('source {0}/bin/env'.format(bonfire_home))
    fd = open(config_file)
    input_conf=json.load(fd)
    pprint.pprint(input_conf)
    fd.close()
    new_conf=input_conf
    for k,v in input_conf['env'].items():
        print 'key = {0}, val = {1}'.format(k, os.environ.get(k, ''))
        new_conf['env'][k] = os.environ.get(k, '')
    fd2 = open(config_file, 'w')
    json.dump(new_conf, fd2, indent=4)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

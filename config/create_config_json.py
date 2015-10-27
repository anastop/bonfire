import json
import os
import pprint
import sys

def main(bonfire_home, config_file):

    with open(config_file) as fd:
        input_conf=json.load(fd)
    pprint.pprint(input_conf)
 
    bonfire_env = {}
    with open('{0}/setup_env_vars.sh'.format(bonfire_home)) as fd:
        for line in fd:
            if 'PATH' not in line:
                var = line.split(' ')[-1]
                k, v = var.split('=')
                bonfire_env[k] = v.strip()

    for k,v in bonfire_env.items():
        print 'key = {0}, val = {1}'.format(k, v)
        input_conf['env'][k] = v
 
    out = json.dumps(input_conf, indent=4, sort_keys=True)
    with open(config_file, 'w') as fd:
        fd.write(out)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

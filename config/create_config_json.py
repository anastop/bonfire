import json
import os

if __name__ == '__main__':

    new_conf={}

    fd = open('config.json')
    input_conf=json.load(fd)
    fd.close()
    new_conf=input_conf
    for k,v in input_conf['env']:
        new_conf['env'][k] = os.environ[k]
    fd2 = open('config.json', 'w')
    json.dump(new_conf,fd2)

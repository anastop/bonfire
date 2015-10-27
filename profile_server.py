#!/usr/bin/env python

import bottle
import profilers.flight_recorder as jfr_rec
import profilers.perf_recorder as perf_rec
import os
import logging
import argparse
import json

profilers = {
    'jfr': jfr_rec.FlightRecorder,
    'perf': perf_rec.LinuxPerfRecorder
}


profiler_list = None
profiler_id1 = 0


def init_env(env_conf):
    # recieves the initial opts and starts the deamon
    for key, value in env_conf:
        if key in os.environ:
            os.environ[key] += ' ' + value
        else:
            os.environ[key] = value


@bottle.route('/init/<profiler>', method='POST')
def init(profiler):
    global profiler_list
    global profiler_id1
    # receives the initial opts and starts the deamon
    profiler_conf = bottle.request.json
    profiler_list.append(profilers[profiler](profiler_conf))
    profiler_id1 += 1
    #bottle.response.data = profiler_id1
    # here we send the profiler_id
    return bottle.HTTPResponse(status=200, body=profiler_id1)


@bottle.route('/start/<profiler_id>', method='POST')
def start(profiler_id):
    # in order to start a recording we get an opts argument
    profiler_list[profiler_id].setup_karaf_env()
    profiler_list[profiler_id].start()


@bottle.route('/stop/<profiler_id>', method='POST')
def stop(profiler_id):
    profiler_list[profiler_id].stop()


@bottle.route('/get_data/<profiler_id>', method='POST')
def get_data(profiler_id):
    opts = profiler_list[profiler_id].opts
    return bottle.static_file(opts['recording_file'], opts['output_dir'])
    # here is the endpointa


@bottle.route('/get_flamegraph/<profiler_id>', method='POST')
def get_flamegraph(profiler_id):
    # here we should get the binary blobs
    opts = profiler_list[profiler_id].opts
    return bottle.static_file(opts['flamegraph_name'], opts['output_dir'])


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--json-config',
                        required=True,
                        type=str,
                        dest='json_config',
                        action='store',
                        help='Configuration file (JSON)')

    args = parser.parse_args()
    conf = {}
    with open(args.json_config) as conf_file:
        conf = json.load(conf_file)
    init_env(conf['env'])
    bottle.run(host=conf['master_ip'], port=conf['master_port'], debug=True)

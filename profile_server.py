#!/usr/bin/env python

import bottle
import profilers.flight_recorder as jfr_rec
import profilers.perf_recorder as perf_rec
import os
import logging
import argparse
import json
import uuid

AVAIL_PROFILERS = {
    'jfr': jfr_rec.FlightRecorder,
    'perf': perf_rec.LinuxPerfRecorder
}


ACTIVE_PROFILERS = {}

@bottle.route('/init/<profiler>', method='POST')
def init(profiler):
    global ACTIVE_PROFILERS
    # receives the initial opts and starts the deamon

    uid = uuid.uuid1().hex
    profiler_conf = bottle.request.json
    profiler_conf['profiler_id'] = uid
    prof_inst = AVAIL_PROFILERS[profiler](profiler_conf)
    
    ACTIVE_PROFILERS[uid] = prof_inst
    # here we send the profiler_id
    return bottle.HTTPResponse(status=200, body=json.dumps({'profiler_id': uid}))


@bottle.route('/setenv/<profiler_id>/<env>', method='POST')
def setenv(profiler_id, env):
    ACTIVE_PROFILERS[profiler_id].setup_env(env)


@bottle.route('/start/<profiler_id>', method='POST')
def start(profiler_id):
    # in order to start a recording we get an opts argument
    start_conf = bottle.request.json
    ACTIVE_PROFILERS[profiler_id].start(start_conf['pid'], start_conf['recording_name'])


@bottle.route('/stop/<profiler_id>', method='POST')
def stop(profiler_id):
    recording_file = ACTIVE_PROFILERS[profiler_id].stop()
    return bottle.HTTPResponse(status=200, body=json.dumps({'recording_file': recording_file}))


@bottle.route('/get_data/<profiler_id>/<filename>', method='GET')
def get_data(profiler_id, filename):
    out_dir = ACTIVE_PROFILERS[profiler_id].opts['output_dir']
    return bottle.static_file(filename, root=out_dir, download=filename)


@bottle.route('/generate_flamegraph/<profiler_id>/<src_file>', method='POST')
def generate_flamegraph(profiler_id, src_file):
    flamegraph_file = ACTIVE_PROFILERS[profiler_id].generate_flamegraph(src_file)
    return bottle.HTTPResponse(status=200, body=json.dumps({'flamegraph_file': flamegraph_file}))


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
    bottle.run(host=conf['server_ip'], port=conf['server_port'], debug=True)

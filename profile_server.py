

profiler_list = None
profiler_id = 0
#opts['recording_file']
#opts['output_dir']
#opts['recording_name']
#opts['pid']
#opts['karaf_home']
#opts['JAVA_HOME']
#opts['JAVA_opts']
#opts['karaf_profiling']
#opts['profiling_mode'] #jrf or perf
#opts['flamegraph_name']
#opts['generate_flamegraph']

@bottle.route('/init', method='POST')
def init(opts):
    global profiler_list
    #sends the initial opts and starts the deamon
    profiler_conf = bottle.request.json
    profiler_list.append(LinuxPerfRecorder(profiler_conf))
    profiler_id += 1

@bottle.route('/start/<profiler_id>', method='POST')
def start(opts):
    #in order to start a recording we get an opts argument
    profiler_list[profiler_id].setup_karaf_env()
    profiler_list[profiler_id].start()

@bottle.route('/stop/<profiler_id>', method='POST')
def stop(opts):
    profiler_list[profiler_id].stop()

@bottle.route('/get_data/<profiler_id>', method='POST')
def get_data(opts):
    #here is the endpoint
def get_flamegraph(opts):


if __name__ == '__main__':
	logging.getLogger().setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

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
    bottle.run(host=conf['master_ip'], port=host=conf['master_port'], debug=True)

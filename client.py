import argparse
import bottle
import logging


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--server-command',
                        required=True,
                        type=str,
                        dest='server_command',
                        action='store',
                        help='Command to send to the server')
    parser.add_argument('--output-dir',
                        required=True,
                        type=str,
                        dest='output_dir',
                        action='store',
                        help='Directory to save results in')

    parser.add_argument('--pid',
                        required=True,
                        type=int,
                        dest='pid',
                        action='store',
                        help='Process Id of the process to profile')
    parser.add_argument('--recording-name',
                        required=True,
                        type=str,
                        dest='output_dir',
                        action='store',
                        help='Name of the recording')
    parser.add_argument('--karaf-home',
                        required=False,
                        type=str,
                        dest='karaf_home',
                        action='store',
                        help='Karaf Directory')
    parser.add_argument('--java-home',
                        required=False,
                        type=str,
                        dest='java_home',
                        action='store',
                        help='JAVA_HOME')
    parser.add_argument('--java-opts',
                        required=False,
                        type=str,
                        dest='java_opts',
                        action='store',
                        help='JAVA_OPTS')

    parser.add_argument('--karaf-profiling',
                        required=True,
                        type=str,
                        dest='karaf_profiling',
                        action='store',
                        help='Whether we are profiling karaf of not')
    parser.add_argument('--profiling-mode',
                        required=True,
                        type=str,
                        dest='profiling_mode',
                        action='store',
                        help='perf or jfr')
    parser.add_argument('--flamegraph-name',
                        required=False,
                        type=str,
                        dest='flamegraph_name',
                        action='store',
                        help='Name of the resulting SVG')
    parser.add_argument('--flamegraph-name',
                        required=False,
                        type=str,
                        dest='flamegraph_name',
                        action='store',
                        help='Name of the resulting SVG')
    parser.add_argument('--generate-flamegraph',
                        required=True,
                        type=str,
                        dest='generate_flamegraph',
                        action='store',
                        help='Whether or not to generate flamegraph')
    parser.add_argument('--server-ip',
                        required=True,
                        type=str,
                        dest='server_ip',
                        action='store',
                        help='Remote server ip')
    parser.add_argument('--server-port',
                        required=True,
                        type=str,
                        dest='server_port',
                        action='store',
                        help='Remote server port')

    args = parser.parse_args()

    opts = {}

    opts['recording_file'] = args.recording_file
    opts['output_dir'] = args.output_dir
    opts['recording_name'] = args.recording_name
    opts['pid'] = args.pid
    opts['karaf_home'] = args.karaf_home
    opts['JAVA_HOME'] = args.java_home
    opts['JAVA_opts'] = args.java_opts
    opts['karaf_profiling'] = args.karaf_profiling
    opts['profiling_mode'] = args.profiling_mode
    opts['flamegraph_name'] = args.flamegraph_name
    opts['generate_flamegraph'] = args.generate_flamegraph


    session = requests.Session()
    session.trust_env = False
    url =
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    post_call = session.post(
        url,
        data=json.dumps(opts),
        headers=headers)


#    with open(args.json_config) as conf_file:
#      conf = json.load(conf_file)

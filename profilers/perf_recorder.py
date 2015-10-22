import os
import logging
import util.customsubprocess as cp
import profilers.abc_profiler


class LinuxPerfRecorder(profilers.abc_profiler.ABCProfiler):
    def __init__(self, opts):
        super(LinuxPerfRecorder, self).__init__(opts)

    def setup_java_opts(self):
        return super(LinuxPerfRecorder, self).setup_java_opts()

    def setup_karaf_env(self):
       return super(LinuxPerfRecorder, self).setup_karaf_env()

    def start(self):
        cmd = 'sudo perf record -F {0} -a -g'.format(self.opts['sample_rate'])
        logging.debug('[PERF CWD]' + os.getcwd())
        logging.debug('[PERF RECORD]' + cmd)
        cpid = os.fork()
        if cpid == 0:
            # in child
            sp.call(cmd, shell=True)
            os._exit(0)
        else:
            # in parent
            self.opts['pid'] = cpid

    def stop(self):
        self.opts['recording_file'] = self.opts['output_dir'] + '/perf.data.' + self.opts['recording_name']
        cpid = os.fork()
        if cpid == 0:
            cmd = 'sudo killall perf'
            cp.blockable_shell(cmd, block_shell=True)
            os._exit(0)
        else:
            self.opts['pid'], _ = os.waitpid(cpid, 0)
#            cmd = 'mv perf.data {0}'.format(self.opts['recording_file'])
#            cp.blockable_shell(cmd, block_shell=True)
#        logging.debug('[PERF FLAMEGRAPH]' + cmd)


    def generate_flamegraph(self, perf_data_file, flamegraph_name):
        flamegraph_file = self.opts['output_dir'] + '/' + flamegraph_name + '.perf.svg'
        cpid = os.fork()
        if cpid == 0:
            # in child
            cmd = 'sudo -u {0} {1}/utilities/jmaps_karaf'.format(os.environ['USER'], os.environ['ODLP2_HOME'])
            logging.debug('[PERF FLAMEGRAPH]' + cmd)
            sp.call(cmd, shell=True)
            os._exit(0)
        else:
            # in parent
            self.opts['pid'], _ = os.waitpid(cpid, 0)
            cmd = 'sudo perf script | {1}/stackcollapse-perf.pl | flamegraph.pl --color=java --hash > {2}'.format(
#                perf_data_file,
                os.environ['FLAMEGRAPH_HOME'],
                flamegraph_file)
#            cmd = 'mv perf.data {0}'.format(self.opts['recording_file'])
#            cp.blockable_shell(cmd, block_shell=True)
            logging.debug('[PERF FLAMEGRAPH]' + cmd)
            sp.call(cmd, shell=True)

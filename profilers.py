import os
import logging
import abc


class ABCProfiler(object):
    __metaclass__ = abc.ABCMeta

    opts = {}
    env_list = []
    def __init__(self, opts):
        self.opts = opts
        self.env_list = self.setup_java_opts()

    @abc.abstractmethod
    def setup_java_opts(self):
        export_jo = 'export JAVA_OPTS="$JAVA_OPTS {0}"'.format(self.opts['java_opts'])
        logging.debug("[JAVA OPTS] " + export_jo)
        return [export_jo]

    @abc.abstractmethod
    def setup_karaf_env(self):
        logging.debug('changing karaf env')
        with open(self.opts['karaf_home'] + '/bin/setenv', 'a') as setenv:
            print(self.opts['karaf_home'] + '/bin/setenv')
            for curr_variable in self.env_list:
                logging.debug('writing ' + curr_variable)
                setenv.write(curr_variable + '\n')
        return 0

    @abc.abstractmethod
    def start(self):
        return

    @abc.abstractmethod
    def stop(self):
        return

    @abc.abstractmethod
    def generate_flamegraph(self, in_file, flamegraph_name):
        return


class FlightRecorder(ABCProfiler):
    opts = {}
    env_list = []
    def __init__(self, opts):
        super(FlightRecorder, self).__init__(opts)

    def setup_java_opts(self):
        return super(FlightRecorder, self).setup_java_opts()

    def setup_karaf_env(self):
       return super(FlightRecorder, self).setup_karaf_env()

    def start(self):
        cmd = '{0}/bin/jcmd {1} JFR.start name={2} settings={0}/jre/lib/jfr/{3}'.format(
            os.environ['JAVA_HOME'],
            self.opts['pid'],
            self.opts['recording_name'],
            self.opts['jfr_profile'] + '.jfc')
        logging.debug('[starting profiler] '+cmd)
        cp.blockable_shell(cmd, block_shell=False)

    def stop(self):
        self.opts['recording_file'] = self.opts['output_dir'] + '/' + self.opts['recording_name'] + '.jfr'
        cmd = '{0}/bin/jcmd {1} JFR.stop name={2} filename={3}'.format(
            os.environ['JAVA_HOME'],
            self.opts['pid'],
            self.opts['recording_name'],
            self.opts['recording_file'])
        logging.debug('[stopping profiler] '+cmd)
        cp.blockable_shell(cmd, block_shell=False)

    def generate_flamegraph(self, jfr_file, flamegraph_name):
        flamegraph_file = self.opts['output_dir'] + '/' + flamegraph_name + '.jfr.svg'
        cmd = '{0}/bin/jfr2flame {1} {2}'.format(
            os.environ['JFR2FLAME_HOME'],
            jfr_file,
            flamegraph_file)
        logging.debug('[generating flamegraph] '+cmd)
        cp.blockable_shell(cmd, block_shell=True)
        return flamegraph_file


class LinuxPerfRecorder(ABCProfiler):
    opts = {}
    env_list = []
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

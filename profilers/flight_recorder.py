import os
import logging
import util.customsubprocess as cp
import profilers.abc_profiler


class FlightRecorder(profilers.abc_profiler.ABCProfiler):
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
            self.opts['JFR2FLAME_HOME'],
            jfr_file,
            flamegraph_file)
        logging.debug('[generating flamegraph] '+cmd)
        cp.blockable_shell(cmd, block_shell=True)
        return flamegraph_file




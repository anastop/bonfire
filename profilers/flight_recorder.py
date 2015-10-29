import os
import logging
import util.customsubprocess as cp
import profilers.abc_profiler


class FlightRecorder(profilers.abc_profiler.ABCProfiler):
    def __init__(self, opts):
        opts['output_dir'] = '{0}/{1}'.format(opts['output_dir'], opts['profiler_id'])
        os.makedirs(opts['output_dir'])
        super(FlightRecorder, self).__init__(opts)
        self.STARTED = False
        self.current_pid = -1
        self.current_recording_name = ''
        self.current_recording_file = ''
        self.last_recorded_file = ''

    def setup_java_opts(self):
        return super(FlightRecorder, self).setup_java_opts()

    def setup_karaf_env(self):
       return super(FlightRecorder, self).setup_karaf_env()

    def setup_java_env(self):
       return super(FlightRecorder, self).setup_java_env()

    def setup_env(self, env):
       return super(FlightRecorder, self).setup_env(env)

    def start(self, pid, recording_name):
        logging.info("Starting Java Flight Recording")
        self.current_pid = pid
        self.current_recording_name = recording_name
        cmd = '{0}/bin/jcmd {1} JFR.start name={2} settings={0}/jre/lib/jfr/{3}'.format(
            self.opts['env']['JAVA_HOME'],
            pid,
            recording_name,
            self.opts['jfr_profile'] + '.jfc')
        self.STARTED = True
        logging.debug('[starting profiler] '+cmd)
        cp.blockable_shell(cmd, block_shell=self.opts['blocking_shells'])

    def stop(self):
        if not self.STARTED:
            return ''
        recording_file = self.opts['output_dir'] + '/' + self.current_recording_name + '.jfr'
        cmd = '{0}/bin/jcmd {1} JFR.stop name={2} filename={3}'.format(
            self.opts['env']['JAVA_HOME'],
            self.current_pid,
            self.current_recording_name,
            recording_file)
        self.current_pid = -1
        self.current_recording_name = ''
        self.STARTED = False
        self.last_recorded_file = recording_file
        logging.debug('[stopping profiler] '+cmd)
        cp.blockable_shell(cmd, block_shell=self.opts['blocking_shells'])
        return recording_file.split('/')[-1]

    def generate_flamegraph(self, jfr_file):
        jfr_file = '{0}/{1}'.format(self.opts['output_dir'], jfr_file)
        flamegraph_file = '{0}/{1}.svg'.format(self.opts['output_dir'], jfr_file)
        cmd = 'JFR2FLAME_HOME={0} JAVA_HOME={1} FLAMEGRAPH_HOME={2} {0}/bin/jfr2flame {3} {4}'.format(
            self.opts['env']['JFR2FLAME_HOME'],
            self.opts['env']['JAVA_HOME'],
            self.opts['env']['FLAMEGRAPH_HOME'],
            jfr_file,
            flamegraph_file)
        logging.debug('[generating flamegraph] '+cmd)
        cp.blockable_shell(cmd, block_shell=True)
        return flamegraph_file.split('/')[-1]

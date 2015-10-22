"""
Utility module to parse the `ps aux` command output
with emphasis on java processes 
"""

import subprocess
import re

def get_running_processes():
    """Run `ps aux` to get a list of all running processes

    Returns:
        list: A list of all running processes as strings
    """
    processes = []
    ps_aux_out = subprocess.Popen('ps aux', shell=True, stdout=subprocess.PIPE).stdout
    for line in ps_aux_out:
        processes.append(line)
    return processes

def split_process_fields(ps):
    """Parse a `ps aux` line into the process fields
    Args:
        ps (str): The process string you you want to parse

    Returns:
        dict: A dictionary with all the fields and the respective values
    """
    ps_fields = ['user', 'pid', 'cpu_percent', 'mem_percent',
                 'vsz', 'rss', 'tty', 'stat', 'start', 'time']
    ps_split = re.split(' *', ps)
    ps_dict = dict(zip(ps_fields, ps_split[:len(ps_fields)]))
    ps_dict['cmd'] = ' '.join(ps_split[len(ps_fields):])
    return ps_dict

def summarize_java_cmd(cmd):
    """Split a java command into the fields and the java options used

    Args:
        cmd (str): The java command as a string

    Returns:
        dict: A dictionary containing the command summary and the java options
    """
    command = {}
    command['java_opts'] = []
    command['summary'] = []
    for term in re.split(' *', cmd):
        if term.startswith('-'):
            command['java_opts'].append(term)
        else:
            command['summary'].append(term)
    return command

def summarize_java_process(ps_fields):
    """Select only the `user`, `pid` and the summary of the command of a java process

    Args:
        ps_fields (dict): The process split into the appropriate fields

    Returns:
        dict: A dictionary with the process summary
    """
    ps_summary = {}
    cmd_summary = summarize_java_cmd(ps_fields['cmd'])
    ps_summary['user'] = ps_fields['user']
    ps_summary['pid'] = ps_fields['pid']
    ps_summary['cmd_summary'] = cmd_summary['summary']
    ps_summary['java_opts'] = cmd_summary['java_opts']
    return ps_summary

def get_java_processes():
    """Get all the running java process summaries

    Returns:
        list: a list of all the java process summaries
    """
    java_processes = []
    for process in get_running_processes():
        if re.search('java', process):
            ps_fields = split_process_fields(process)
            ps_summary = summarize_java_process(ps_fields)
            java_processes.append(ps_summary)
    return java_processes




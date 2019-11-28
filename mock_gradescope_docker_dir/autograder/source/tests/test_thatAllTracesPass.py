import unittest
import os
import subprocess
import signal

from gradescope_utils.autograder_utils.decorators import visibility, partial_credit
from parameterized import parameterized


trace_folder_relative_path = os.path.relpath('../malloclab-handout/traces')
executable_absolute_path = os.path.abspath('../malloclab-handout/mdriver')

all_graded_traces = [
    "amptjp-bal.rep",
    "cccp-bal.rep",
    "cp-decl-bal.rep",
    "expr-bal.rep",
    "coalescing-bal.rep",
    "random-bal.rep",
    "random2-bal.rep",
    "binary-bal.rep",
    "binary2-bal.rep"
]


def run_bash_command_in_new_process(command: str) -> subprocess.CompletedProcess:
    return subprocess.run(["/bin/bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class RunTraces(unittest.TestCase):
    def setUp(self):
        pass

    # Annotations mean its worth up to 5 points and these tests are never shown to students
    @parameterized.expand([
        ['amptjp-bal', os.path.join(trace_folder_relative_path, 'amptjp-bal.rep')],
        ['cccp-bal', os.path.join(trace_folder_relative_path, 'cccp-bal.rep')],
        ['cp-decl-bal', os.path.join(trace_folder_relative_path, 'cp-decl-bal.rep')],
        ['expr-bal', os.path.join(trace_folder_relative_path, 'expr-bal.rep')],
        ['coalescing-bal', os.path.join(trace_folder_relative_path, 'coalescing-bal.rep')],
        ['random-bal', os.path.join(trace_folder_relative_path, 'random-bal.rep')],
        ['random2-bal', os.path.join(trace_folder_relative_path, 'random2-bal.rep')],
        ['binary-bal', os.path.join(trace_folder_relative_path, 'binary-bal.rep')],
        ['binary2-bal', os.path.join(trace_folder_relative_path, 'binary2-bal.rep')]
    ])
    @partial_credit(5)
    @visibility('hidden')
    def test_no_segfault(self, name: str, relative_trace_path: os.PathLike, set_score=None):
        completed_process = run_bash_command_in_new_process('%s -f %s' % (executable_absolute_path,
                                                                          relative_trace_path))
        if completed_process.returncode != 0:
            failure_string = 'failed -- %s return code %s' % (name, completed_process.returncode)
            if completed_process.returncode < 0:
                failure_string += ', received signal %s' % signal.Signals(completed_process.returncode * -1).name
            failure_string += ', %s' % os.getcwd()
            self.fail(failure_string)
        else:
            set_score(5)

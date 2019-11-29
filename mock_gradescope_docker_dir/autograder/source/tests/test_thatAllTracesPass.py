import unittest
import os
import subprocess
import signal

from gradescope_utils.autograder_utils.decorators import visibility, partial_credit
from parameterized import parameterized

trace_folder_relative_path = os.path.relpath('../malloclab-handout/traces')
executable_absolute_path = os.path.abspath('../malloclab-handout/mdriver')
naive_implementation_absolute_path = os.path.abspath('../mm_naive.c')
student_implementation_absolute_path = os.path.abspath('../malloclab-handout/mm.c')

error_indicator_string = 'ERROR'  # looks for str.lower(error_indicator_string) in stdout or stderr from trace run

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
    # WARNING: This check relies on the fact that run_autograder moves the student's submission to
    # malloclab-handout/mm.c and will not work if that isn't happening
    #
    # WARNING: This check also relies on the packaged mm_naive.c being kept up to date with what is given in the handout
    #
    # Check whether student's submission has more than 50% lines in common with mm_naive.c
    # If they do, set a flag and fail all tests with a message warning the student/grader
    def setUp(self):
        import difflib

        lines_in_mm_naive = [line for line in open(naive_implementation_absolute_path, "r")]
        lines_in_submission_mm = [line for line in open(student_implementation_absolute_path)]

        diff_result = [*difflib.unified_diff(lines_in_mm_naive, lines_in_submission_mm)]
        num_lines_of_difference = len(diff_result)
        total_lines_in_submission = len(lines_in_submission_mm)
        lines_in_common_with_naive = total_lines_in_submission - num_lines_of_difference

        # if number of lines in common with naive implementation is greater than half of the submission
        if lines_in_common_with_naive / total_lines_in_submission > 0.5:
            self.fail("Check if submission is the provided mm_naive.c, when compared found only %s lines of difference "
                      "and %s lines in common" % (num_lines_of_difference, lines_in_common_with_naive))

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
        failure_string = 'failed -- %s return code %s' % (name, completed_process.returncode)
        if completed_process.returncode < 0:
            failure_string += ', received signal %s' % signal.Signals(completed_process.returncode * -1).name
        failure_string += ', %s' % os.getcwd()
        if completed_process.stdout is not None:
            failure_string += '%sstdout:%s%s' % (os.linesep, os.linesep, completed_process.stdout)
        if completed_process.stderr is not None:
            failure_string += '%sstderr:%s%s' % (os.linesep, os.linesep, completed_process.stdout)
        if completed_process.returncode != 0 or \
                error_indicator_string.lower() in str(completed_process.stdout).lower():
            self.fail(failure_string)
        else:
            set_score(5)

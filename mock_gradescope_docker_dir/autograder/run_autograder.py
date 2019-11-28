#!/usr/bin/env python3

# Scott Butler u0469078, Fall 2019
#
# Moves students' mm.c submission to the build folder and run make,
# then runs the grading tests with stdout redirected as necessary for autograding

import subprocess
import os
import re
import difflib
import sys

from typing import Dict


def run_bash_command_in_new_process(command: str,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                    env=None) -> subprocess.CompletedProcess:
    return subprocess.run(["/bin/bash", "-c", command], stdout=stdout, stderr=stderr, env=env)


autograder_source_absolute_path = os.path.abspath('./source')
build_dir_absolute_path = os.path.abspath('./source/malloclab-handout')
results_dir_absolute_path = os.path.abspath('./results')
submission_dir_absolute_path = os.path.abspath('./submission')
naive_implementation_absolute_path = os.path.abspath('./source/mm_naive.c')

submission_filename_to_absolute_path: Dict[str, os.PathLike] =\
    {filename: os.path.join(submission_dir_absolute_path, filename) for filename in
     os.listdir(submission_dir_absolute_path)}

already_found_mm_c = False
mm_c_abs_path = ''
mm_c_pattern = re.compile(r'^.*mm.*\.c$')

for filename, filename_abs_path in submission_filename_to_absolute_path.items():
    if mm_c_pattern.search(filename):
        if already_found_mm_c:
            raise Exception("Encountered multiple matching mm.c filenames (%s, %s)" %
                            (mm_c_abs_path, filename_abs_path))
        already_found_mm_c = True
        mm_c_abs_path = filename_abs_path

if not already_found_mm_c:
    raise Exception("Could not find any files in ../submission matching regex pattern %s\n" % str(mm_c_pattern))

lines_in_mm_naive = [line for line in open(naive_implementation_absolute_path, "r")]
lines_in_submission_mm = [line for line in open(mm_c_abs_path)]

diff_result = [*difflib.unified_diff(lines_in_mm_naive, lines_in_submission_mm)]
num_lines_of_difference = len(diff_result)
total_lines_in_submission = len(lines_in_submission_mm)
lines_in_common_with_naive = total_lines_in_submission - num_lines_of_difference

# if number of lines in common with naive implementation is greater than half of the submission
if lines_in_common_with_naive / total_lines_in_submission > 0.5:
    raise Exception("Check if submission is the provided naive mm.c,"
                    "found only %s lines of difference and %s lines in common" %
                    (num_lines_of_difference, lines_in_common_with_naive))

run_bash_command_in_new_process('cp %s %s/mm.c -f' % (mm_c_abs_path, build_dir_absolute_path))
run_bash_command_in_new_process('cd %s && make' % build_dir_absolute_path, stdout=subprocess.PIPE)

with open('%s/results.json' % results_dir_absolute_path, 'w') as results_file:
    orig_stdout = sys.stdout
    sys.stdout = results_file.fileno()
    test_execution = run_bash_command_in_new_process('cd %s/tests && %s ../run_tests.py' %
                                                     (autograder_source_absolute_path, sys.executable),
                                                     stdout=sys.stdout, stderr=sys.stderr)
    sys.stdout = orig_stdout

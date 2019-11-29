#!/usr/bin/env python3

# Scott Butler u0469078, Fall 2019
#
# Moves students' mm.c submission to the build folder and run make,
# then runs the grading tests with stdout redirected as necessary for autograding

import subprocess
import os
import re
import sys
import json

from typing import Dict

# This import gets moved to /root/..?../mock_gradescope_docker/autograder/
# dir by make_autograder_zip.sh to be next to run_autograder.py
from source import GradescopeAutograderDataObjects as gdo

# The script you're writing gets moved to /root/..?../mock_gradescope_docker_dir/autograder/
# in deployment so all paths are relative from there
autograder_source_absolute_path = os.path.abspath('./source')
build_dir_absolute_path = os.path.abspath('./source/malloclab-handout')
results_dir_absolute_path = os.path.abspath('./results')
submission_dir_absolute_path = os.path.abspath('./submission')

DEBUG = False


def run_bash_command_in_new_process(command: str,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                    env=None) -> subprocess.CompletedProcess:
    return subprocess.run(["/bin/bash", "-c", command], stdout=stdout, stderr=stderr, env=env)


submission_filename_to_absolute_path: Dict[str, os.PathLike] =\
    {filename: os.path.join(submission_dir_absolute_path, filename) for filename in
     os.listdir(submission_dir_absolute_path)}

already_found_mm_c = False
mm_c_abs_path = ''
mm_c_pattern = re.compile(r'^.*mm.*\.c$')

for filename, filename_abs_path in submission_filename_to_absolute_path.items():
    if mm_c_pattern.search(filename):
        if already_found_mm_c:
            raise Exception("Encountered multiple matching mm.c filenames in submission (%s, %s) for regex pattern %s" %
                            (mm_c_abs_path, filename_abs_path, str(mm_c_pattern)))
        already_found_mm_c = True
        mm_c_abs_path = filename_abs_path

if not already_found_mm_c:
    raise Exception("Could not find any files in student submission with names matching regex pattern %s\\n" %
                    str(mm_c_pattern))

run_bash_command_in_new_process('cp %s %s/mm.c -f' % (mm_c_abs_path, build_dir_absolute_path))
make_process = run_bash_command_in_new_process('cd %s && make' % build_dir_absolute_path,
                                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

orig_stdout = sys.stdout

with open('%s/results.json' % results_dir_absolute_path, 'w') as sys.stdout:
    if make_process.returncode != 0:
        result = gdo.AutograderResult(0.0, 0.0, 'Make process returned %d for file %s%sstdout:%s%sstderr:%s%s' %
                                      (make_process.returncode, os.path.basename(mm_c_abs_path),
                                          os.linesep, make_process.stdout,
                                          os.linesep, make_process.stderr, os.linesep),
                                      gdo.AutograderResult.VISIBILITY_VISIBLE,
                                      gdo.AutograderResult.VISIBILITY_VISIBLE)
        if DEBUG:
            sys.stdout = orig_stdout
        print(json.dumps(result.__dict__))
        exit(0)
    test_execution = run_bash_command_in_new_process('cd %s/tests && %s ../run_tests.py' %
                                                     (autograder_source_absolute_path, sys.executable),
                                                     stdout=sys.stdout, stderr=sys.stderr)
    sys.stdout = orig_stdout

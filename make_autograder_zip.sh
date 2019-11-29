#!/usr/bin/env bash

rm -rf autograder
rm -f autograder.zip
mkdir autograder
cp -rf ./mock_gradescope_docker_dir/autograder/source/* ./autograder
cp ./mock_gradescope_docker_dir/autograder/run_autograder.py ./autograder/run_autograder
cp ./mock_gradescope_docker_dir/autograder/GradescopeAutograderDataObjects.py ./autograder/GradescopeAutograderDataObjects.py
cd autograder || exit 1
zip -r ../autograder.zip setup.sh run_autograder GradescopeAutograderDataObjects.py run_tests.py requirements.txt mm_naive.c tests/*.py malloclab-handout/*
cd ..
rm -rf autograder

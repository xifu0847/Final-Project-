#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_pystyle pycodestyle *.py --ignore=E402
assert_no_stdout

run test_bad_input python driver.py --input_file=bad_input.txt
assert_in_stderr 'Input file not found'

run test_bad_sample_number python driver.py --input_file=merged_gene_counts.txt --sample_num=10000
assert_in_stderr 'sample number should be 1-50'

run test_good_usage python driver.py --input_file=merged_gene_counts.txt
assert_no_stderr

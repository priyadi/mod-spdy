#!/usr/bin/env python
#
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Runs both the Python and Java tests."""

import sys
import time

from pylib import apk_info
from pylib import test_options_parser
from pylib import run_java_tests
from pylib import run_python_tests
from pylib import run_tests_helper
from pylib.test_result import TestResults


def SummarizeResults(java_results, python_results, annotation):
  """Summarize the results from the various test types.

  Args:
    java_results: a TestResults object with java test case results.
    python_results: a TestResults object with python test case results.
    annotation: the annotation used for these results.

  Returns:
    A tuple (all_results, summary_string, num_failing)
  """
  all_results = TestResults.FromTestResults([java_results, python_results])
  summary_string = all_results.LogFull('Instrumentation', annotation)
  num_failing = (len(all_results.failed) + len(all_results.crashed) +
                 len(all_results.unknown))
  return all_results, summary_string, num_failing


def DispatchInstrumentationTests(options):
  """Dispatches the Java and Python instrumentation tests, sharding if possible.

  Uses the logging module to print the combined final results and
  summary of the Java and Python tests. If the java_only option is set, only
  the Java tests run. If the python_only option is set, only the python tests
  run. If neither are set, run both Java and Python tests.

  Args:
    options: command-line options for running the Java and Python tests.

  Returns:
    An integer representing the number of failing tests.
  """
  start_date = int(time.time() * 1000)
  java_results = TestResults()
  python_results = TestResults()

  if options.run_java_tests:
    java_results = run_java_tests.DispatchJavaTests(
        options,
        [apk_info.ApkInfo(options.test_apk_path, options.test_apk_jar_path)])
  if options.run_python_tests:
    python_results = run_python_tests.DispatchPythonTests(options)

  all_results, summary_string, num_failing = SummarizeResults(
      java_results, python_results, options.annotation)
  return num_failing


def main(argv):
  options = test_options_parser.ParseInstrumentationArgs(argv)
  run_tests_helper.SetLogLevel(options.verbose_count)
  return DispatchInstrumentationTests(options)


if __name__ == '__main__':
  sys.exit(main(sys.argv))

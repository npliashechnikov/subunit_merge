A simple testrepository stream merger.
No dependencies, no anything, just merges the testrepository streams.

Intended audience: QA engineers using subunit / testrepository tools in their work.
Intended use: Merging the test results from multiple test runs (particularly useful if multiple test configurations are used),
or in conjunction with --failing/--partial testrepository run.
Running the tool will replace failed/skipped testcases with successful ones in case if there are any. If new testcases had been
executed in following streams, they will be also added to the resulting stream, no matter if they passed or failed.

The review.py script also gives you a way to remove failing test cases manually if you want.

How to use:
1. Place merge.py and review.py to the .testrepository folder in your test suite.
2. Run all tests how many times you want.
3. Run merge.py
4. Run review.py
5. Grab resulting stream do whatever you need to do with it.

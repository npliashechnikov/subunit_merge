#!/usr/bin/python
enable_manual_edit = False
streams = {}
base_stream = 0
def test_in_stream(test, stream):
    global streams
    test_name = ''
    for line in test:
        if line.startswith('test:'):
            test_name = line
    for test_data in streams[stream]:
        if test_name in test_data:
            return streams[stream].index(test_data)
    return False

def is_successful(test):
    for line in test:
        if "successful" in line:
            return True
    return False

def is_skipped(test):
    for line in test:
        if "skip:" in line:
            return True
    return False

def get_test_name(test):
    for line in test:
        if line.startswith("test:"):
            cp = line
            cp = cp.replace("test: ", "")
            cp = cp.split('[')[0]
            return cp
    raise RuntimeError("Test name not found")

def get_full_name(test_name):
    if '(' in test_name:
    	test_name_and_class = test_name.split(' (')
    else:
        test_split = test_name.split('.')
        test_name = test_split[-1]
        test_class = reduce(lambda x, l: x + '.' + l, test_split[:-1], "")[1:]
        test_name_and_class = [test_name, test_class]
    test_name = test_name_and_class[0].replace(' ', '')
    test_class = test_name_and_class[1].replace(')', '').replace(' ', '')

    return test_name, test_class

def is_failing(test):
    for line in test:
        if "failure:" in line:
            return True
    return False

with open("result", "rt") as f:
    raw_tests = f.readlines()
    raw_tests = map(lambda m: m.replace("\n", ''), raw_tests)
    tests = []
    current_test = []
    for line in raw_tests:
        if line.startswith("tags: -worker"):
            #print "found test"
            current_test.append(line)
            tests.append(current_test)
            current_test = []
        else:
            current_test.append(line)
new_tests = []

#for test in tests:
#     if is_failing(test):
#         remove = raw_input("Test %s is failing. Delete from run? (Y/n)" % get_test_name(test))
#         if 'Y' in remove:
#             continue
#         else:
#             new_tests.append(test)
#     else:
#         new_tests.append(test)

#with open('result-new', 'wt') as f:
#    for test in new_tests:
#        for line in test:
#            f.write("%s\n" % line)

#tests = new_tests
test_map = {}

for test in tests:
    test_name, test_class = get_full_name(get_test_name(test))
    if is_successful(test):
        test_map[test_class] = 's'
    elif is_failing(test) and test_class not in test_map:
        test_map[test_class] = 'f'

for test in tests:
    test_name, test_class = get_full_name(get_test_name(test))
    if test_name == 'setUpClass' and is_skipped(test) and test_class in test_map:
        print 'Deleting skipped setUpClass from %s because it has been executed later.' % test_class
    elif test_name == 'setUpClass' and is_failing(test) and test_class in test_map and (test_map[test_class] == 's'):
        print 'Deleting failing setUpClass from %s because it has succeded lated.' % test_class
    elif 'object_storage' in test_class and is_failing(test):
        print 'Object storage test %s:%s deleted: RadosGW is not fully conformant with Swift API.' % (test_class, test_name)
    else:
        new_tests.append(test)       

with open('result-new', 'wt') as f:
    for test in new_tests:
        for line in test:
            f.write("%s\n" % line)

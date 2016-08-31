#!/usr/bin/python
with open("next-stream", "rt") as f:
    next = int(f.read())

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

def is_failing(test):
    for line in test:
        if "failure:" in line:
            return True
    return False

for stream in range(next):
    if base_stream not in streams:
        base_stream = stream
    try:
        with open(str(stream), "rt") as f:
            print "reading stream %s" % stream
            raw_tests = f.readlines()
            raw_tests = map(lambda m: m.replace('\n', ''), raw_tests)
    except:
        print "Stream %s not found, continuing" % stream
        continue

    tests = []
    current_test = []
    streams[stream] = tests
    for line in raw_tests:
        if line.startswith("tags: -worker"):
            #print "found test"
            current_test.append(line)
            tests.append(current_test)
            current_test = []
        else:
            current_test.append(line)
    print "%s tests found"%len(tests)
    if stream > base_stream:
        n_added = 0
        n_replaced = 0
        for test in tests:
            if not test_in_stream(test, base_stream):
                #print "Added new test"   
                n_added += 1
                streams[base_stream].append(test)
            elif is_successful(test):
                #print "Replaced test"
                n_replaced += 1
                streams[base_stream][test_in_stream(test, base_stream)] = test
            elif is_failing(test):
                old_test = streams[base_stream][test_in_stream(test, base_stream)]
                if is_failing(old_test):
                    streams[base_stream][test_in_stream(test, base_stream)] = test
        print "Stream %s: added %s, replaced %s tests" % (stream, n_added, n_replaced)
    print "Total discovered so far: %s" % len(streams[base_stream])
with open("result", "wt") as f:
    for test in streams[base_stream]:
        for line in test:
            f.write("%s\n"%line)

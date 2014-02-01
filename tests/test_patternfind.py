from patternfind import internal_cmp, suffix_array, lcp_array, pattern_to_remove
from nose.tools import assert_true
import time
import random


def makelambda(o1, o2, l1, l2):
    def fn(occ, leng):
        if not o1 <= occ <= o2:
            return -1
        if not l1 <= leng <= l2:
            return -1
        return occ * leng
    return fn


def test_speed():
    p = ['b', 'a']*100000
    random.shuffle(p)
    p = ''.join(p)
    t = time.time()
    sa = suffix_array(p)
    assert_true(time.time() < 5 + t)
    t = time.time()
    lcp = lcp_array(p, sa)
    assert_true(time.time() < 5 + t)
    t = time.time()
    pattern_to_remove(p, sa, lcp, makelambda(2, 18, 5, 100000))
    assert_true(time.time() < 5 + t)
    t = time.time()


def test_accuracy():
    for step in range(1, 15):
        assert_true(internal_cmp('hello', 0, 5, step) == cmp('hello', ''))
        assert_true(internal_cmp('hello', 0, 6, step) == cmp('hello', ''))
        assert_true(internal_cmp('appleappl', 0, 5, step) == cmp('apple', 'appl'))
        assert_true(internal_cmp('applebpple', 0, 5, step) == cmp('apple', 'bpple'))
        assert_true(internal_cmp('appleappee', 0, 5, step) == cmp('apple', 'appee'))
        assert_true(internal_cmp('appleappee', 5, 0, step) == cmp('appee', 'apple'))
    p = 'banana'
    sa = suffix_array(p)
    assert_true(sa == [5, 3, 1, 0, 4, 2])
    lcp = lcp_array(p, sa)
    assert_true(lcp == [0, 1, 3, 0, 0, 2])


def test_small_input_endtoend():
    st = '\n'
    st += '<bb>a</bb><cat>\n'
    st += '<bb>j</bb><dog>\n'
    st += '<bb>bob</bb><man>\n'
    st += '<bb>to</bb><go>\n'
    pats = []
    for i in range(3):
        sa = suffix_array(st)
        lcp = lcp_array(st, suffix_array(st))
        pat = pattern_to_remove(st, sa, lcp, makelambda(3, 6, 2, float('inf')))
        if '\n' in pat:
            pat = max(pat.split('\n'), key=lambda kk: len(kk))
        pats.append(pat)
        st = st.replace(pat, '\n')
    assert_true(st.replace('\n', '').strip() == 'acatjdogbobmantogo')
    assert_true(pats == ['</bb><', '<bb>', '>'])

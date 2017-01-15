def expect_eq(exp, val):
  if exp != val:
    print "exp {} doesn't equal val {}".format(exp, val)
    assert(False)

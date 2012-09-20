from dexy.doc import Doc
from dexy.tests.utils import assert_in_output
from dexy.tests.utils import wrap

def test_clj_filter():
    assert_in_output('cljint', '1+1', "user=> 1+1")

def test_ksh_filter():
    assert_in_output('kshint', 'ls', "example.txt")

def test_php_filter():
    assert_in_output('phpint', '1+1', "php > 1+1")

def test_rhino_filter():
    assert_in_output('rhinoint', '1+1', "js> 1+1")

def test_irb_filter():
    assert_in_output('irb', "puts 'hello'", ">> puts 'hello'")

def test_pycon_filter_single_section():
    assert_in_output('pycon', "print 'hello'", ">>> print 'hello'")

def test_ipython_filter():
    assert_in_output('ipython', "print 'hello'", ">>> print 'hello'")

def test_r_filter():
    assert_in_output('r', '1+1', '> 1+1')

def test_shint_filter():
    with wrap() as wrapper:
        src = """
### @export "touch"
touch newfile.txt

### @export "ls"
ls
"""
        doc = Doc("example.sh|idio|shint|pyg",
                contents = src,
                wrapper=wrapper)
        wrapper.docs = [doc]
        wrapper.run()

        assert doc.output().keys() == ['1', 'touch', 'ls']

def test_pycon_filter():
    with wrap() as wrapper:
        src = """
### @export "vars"
x = 6
y = 7

### @export "multiply"
x*y

"""
        doc = Doc("example.py|idio|pycon",
                contents=src,
                wrapper=wrapper)

        wrapper.docs = [doc]
        wrapper.run()

        assert doc.output().keys() == ['1', 'vars', 'multiply']
        assert doc.output().as_sectioned()['vars'] == """
>>> x = 6
>>> y = 7"""

        assert doc.output().as_sectioned()['multiply'] == """
>>> x*y
42"""

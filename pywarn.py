import warnings
import sys

IGNORE_WARNINGS = 'ignore'
ALWAYS_WARNINGS = 'always'
ERROR_FROM_WARNING = 'error'
WARN_OPT = (IGNORE_WARNINGS, ALWAYS_WARNINGS, ERROR_FROM_WARNING)

class LastShowwarning:
    last = None

class CustomWarning (Warning):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return self.message

def set_showwarning (func):
    LastShowwarning.last = warnings.showwarning
    warnings.showwarning = func

def reset_showwarning ():
    warnings.showwarning = LastShowwarning.last

def set_filter (opt, category):
    warnings.simplefilter(opt, category=category)

def warn (thing):
    warnings.warn(thing)

def bare_showwarning (message, cat, *a, **k):
    print('{}: {}'.format(cat.__name__, message), file=sys.stderr)

#warnings.simplefilter('ignore', CustomWarning)

if __name__ == '__main__':
    try:
        assert sys.argv[1:] and all(opt in WARN_OPT for opt in sys.argv[1:])
    except AssertionError:
        print("Usage: %prog [{}]...".format(WARN_OPT))
    for n, opt in enumerate(sys.argv[1:], start=1):
        if n % 2: # switching warnings format
            set_showwarning(bare_showwarning)
        print('arg no. {} ({}) [{}]'.format(n, opt, warnings.showwarning.__name__))
        set_filter(opt, CustomWarning)
        warn(CustomWarning(opt))
        if n % 2:
            reset_showwarning()


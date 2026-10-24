"""Run224 independent oracle-reversal counterexample (Python stdlib).

Pinned PyBaMM BatchStudy initializes sims in solve(), not __init__.
BatchStudy has no _solution field; Simulation does. This demonstrates why
the previous Run223 state harness could invert repair rankings.
"""
import types

METHOD = '''def create_gif(self):
    if GUARD(self):
        raise ValueError("not solved")
    if self.quick_plot is None:
        self.quick_plot = pybamm.QuickPlot(self.sims)
    self.quick_plot.create_gif()
'''

def trial(guard, solved, cached, faithful):
    events = []
    class Plot:
        def __init__(self, value):
            events.append('construct')
        def create_gif(self):
            events.append('gif')
    ns = {'pybamm': types.SimpleNamespace(QuickPlot=Plot), 'GUARD': guard}
    exec(METHOD, ns)
    obj = types.SimpleNamespace(quick_plot=Plot('cached') if cached else None)
    events.clear()
    if faithful:
        if solved:
            obj.sims = [object()]
    else:
        obj.sims = [object()] if solved else None
        obj._solution = object() if solved else None
    error = None
    try:
        ns['create_gif'](obj)
    except Exception as exc:
        error = type(exc).__name__
    return ((error is None and events.count('gif') == 1 and
             events.count('construct') == (0 if cached else 1)) if solved
            else (error == 'ValueError' and not events))

def score(guard, faithful):
    return sum(trial(guard, solved, cached, faithful)
               for solved in (False, True) for cached in (False, True))

if __name__ == '__main__':
    good = lambda obj: not hasattr(obj, 'sims')
    wrong = lambda obj: obj._solution is None
    historical = (score(good, False), score(wrong, False))
    faithful = (score(good, True), score(wrong, True))
    print({'historical': {'reference': historical[0], 'wrong_field': historical[1]},
           'faithful': {'reference': faithful[0], 'wrong_field': faithful[1]}})
    assert historical == (2, 4) and faithful == (4, 0)

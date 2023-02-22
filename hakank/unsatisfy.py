import random
from time import time

import cpmpy as cp

from cpmpy.transformations.get_variables import get_variables
from cpmpy.expressions.core import Operator, Comparison
from cpmpy.expressions.utils import is_any_list

TIME_LIMIT = 60


def make_model_unsat(constraints, p_change=0.1, seed=0):
    random.seed(seed)

    model = cp.Model(constraints)
    callback = callback_factory(model)

    while callback():
        for cons in constraints:
            if callback():
                change_constraint_with_prob(cons, p_change,
                                            should_continue=callback)

    return constraints

def callback_factory(model):

    history = dict()
    def callback():
        print(model)
        if str(model.constraints) not in history:
            history[str(model.constraints)] = model.solve()
        return history[str(model.constraints)]

    return callback


def change_constraint_with_prob(cpm_expr, p_change=0.1, should_continue=lambda:False):

    if is_any_list(cpm_expr):
        [change_constraint_with_prob(e) for e in cpm_expr]

    try:
        # sample action
        if not should_continue():
            return
        action = random.choice([swap_variables, replace_constraint])
        if random.random() <= p_change:
            action(cpm_expr)
    except RuleNotApplicableError:
        # chosen rule was not applicable, continue
        pass
    if hasattr(cpm_expr, "args"):
        for arg in cpm_expr.args:
            change_constraint_with_prob(arg, p_change, should_continue)





def swap_variables(cpm_expr, var1=None, var2=None):
    """
        Swaps two variables in constraint
        Changes constraint inplace
    """
    if var1 is None or var2 is None:
        vars = get_variables(cpm_expr)
        if len(vars) <= 1:
            raise RuleNotApplicableError()
        var1, var2 = random.choices(vars, k=2)

    # if we change the names of variables inplace, it will also change in other constraints...
    #   this might actually undo previous swaps... so lets replace the variables in this constraint only
    #   requires to walk through the expression tree and change variables everywhere in the arguments
    if hasattr(cpm_expr, "args"):
        for i, arg in enumerate(list(cpm_expr.args)):
            if str(arg) == str(var1):
                cpm_expr.args[i] = var2
            elif str(arg) == str(var2):
                cpm_expr.args[i] = var1
            else:
                swap_variables(arg, var1, var2)


def replace_constraint(cpm_expr):
    if isinstance(cpm_expr, Operator):
        replace_operator(cpm_expr)
    if isinstance(cpm_expr, Comparison):
        replace_comparison(cpm_expr)

def replace_operator(cpm_expr):
    """
        Replace (numerical) operator with another one
        Ensures arity is correct so no obvious error
    """
    if not isinstance(cpm_expr, Operator):
        raise RuleNotApplicableError()

    arity, is_bool = Operator.allowed[cpm_expr.name]
    if arity == 0:
        arity = len(cpm_expr.args) # so we also allow 'and' to be replaced with -> for example

    options = []
    for n, (a,ib) in Operator.allowed.items():
        if (a == arity or a == 0) and cpm_expr.name != n and ib == is_bool and \
                n != "mod" and n != "pow" and n != "div": # these operators are annoying
            options += [n]

    new_op = random.choice(options)
    if new_op == "wsum":
        weights = [random.randint(0,100) for _ in cpm_expr.args]
        cpm_expr.args = [weights, cpm_expr.args]
    elif cpm_expr.name == "wsum":
        cpm_expr.args = cpm_expr.args[1] # drop weights

    cpm_expr.name = new_op


def replace_comparison(cpm_expr):
    """
        Replace comparison with another comparison
    """
    if not isinstance(cpm_expr, Comparison):
        raise RuleNotApplicableError()

    options = [n for n in Comparison.allowed if n != cpm_expr.name]
    cpm_expr.name = random.choice(options)




class RuleNotApplicableError(Exception):
    pass




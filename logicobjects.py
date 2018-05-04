from symbol_convert import LogicSymbols
import copy


class Statement(object):

    def __init__(self, n=0, s=[]):
        self.negations = 0
        self.steps = copy.deepcopy(s)

    def get_steps(self):
        return self.steps

    def get_negations(self):
        return self.negations

    def set_negations(self, n):
        self.negations = n

    def get_step_count(self):
        return len(self.get_steps())

    def add_step(self, step):
        self.steps.append(step)

    def negate(self):
        self.negations += 1

    def clean(self):
        if self.negations > 2:
            self.negations %= 2

    def trueVal(self):
        pass


class Sentence(Statement):
    LEGAL_OPERATIONS = ['&', '|', '$']

    def __init__(self, l, r, o, n=0, s=[]):
        Statement.__init__(self, n, s)
        if type(l) is not Atom and type(l) is not Sentence and type(l) is not str:
            raise ValueError(
                'Unexpected type: ' + str(type(l)) + ', expected ' + str(Atom) + ' or ' + str(Sentence) + ' or ' + str(str))

        if type(l) is str:
            if l[0] is '~':
                l = Atom(l[1:], 1)
            else:
                l = Atom(l)

        if type(r) is str:
            if r[0] is '~':
                r = Atom(r[1:], 1)
            else:
                r = Atom(r)

        self.left_sen = l
        self.right_sen = r
        self.oper = o

    def trueVal(self):
        return Sentence(self.left_sen, self.right_sen, self.oper, 0)

    def recursiveClean(self):
        if type(self.left_sen) is Sentence:
            self.left_sen.recursiveClean()

        if type(self.right_sen) is Sentence:
            self.right_sen.recursiveClean()

        self.left_sen.clean()
        self.right_sen.clean()

        self.clean()

    def get_steps(self):
        all_steps = copy.deepcopy(super().get_steps())
        all_steps.extend(self.left_sen.get_steps())
        all_steps.extend(self.right_sen.get_steps())

        return all_steps

    def get_step_count(self):
        count = self.left_sen.get_step_count()
        count += self.right_sen.get_step_count()

        return count + len(self.steps)

    def __eq__(self, other):

        if isinstance(self, other.__class__):
            return self.left_sen == other.left_sen \
                and self.right_sen == other.right_sen \
                and str(self.oper) == str(other.oper) \
                and self.get_negations() == other.get_negations()

    def __hash__(self):
        return hash((self.left_sen, self.right_sen, self.oper, self.get_negations()))

    def __str__(self):
        left = self.left_sen.__str__()
        right = self.right_sen.__str__()

        if type(self.left_sen) is Sentence:
            left = ''

            if self.left_sen.get_negations() > 0:
                left = self.left_sen.__str__()
            else:
                left = '(' + self.left_sen.__str__() + ')'

        if type(self.right_sen) is Sentence:
            right = ''

            if self.right_sen.get_negations() > 0:
                right = self.right_sen.__str__()
            else:
                right = '(' + self.right_sen.__str__() + ')'

        return_val = left + ' ' + \
            LogicSymbols.OP_CONVERT[self.oper] + ' ' + right

        if self.get_negations() > 0:
            return_val = self.get_negations() * chr(172) + '(' + return_val + ')'

        return return_val


class Atom(Statement):

    def __init__(self, val, n=0, s=[]):
        Statement.__init__(self, n)
        if type(val) is not str:
            raise ValueError('Unexpected type: ',
                             type(val), ', expected ', type(str))

        if type(n) is not int:
            raise ValueError('Unexpected type: ',
                             type(t), ', expected ', type(int))

        self.value = val

    def trueVal(self):
        return Atom(self.value, 0)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return str(self.value) == str(other.value) and str(self.get_negations() == other.get_negations())

    def __hash__(self):
        return hash((self.value, self.get_negations()))

    def __str__(self):
        return chr(172) * self.get_negations() + self.value

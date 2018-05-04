from logicobjects import Sentence
from logicobjects import Atom
from symbol_convert import LogicSymbols


class SentenceParser(object):

    def _recurInput(self, iter):
        sens = []
        for c in iter:
            if c == '(':
                result, legal = self._recurInput(iter)
                if not legal:
                    raise ValueError('Bad expression: unbalanced parenthesis')
                sens.append(result)
            elif c == ')':
                return sens, True
            else:
                sens.append(c)
        return sens, False

    def _filterNegations(self, input_list):
        count = 0
        for i in range(len(input_list)):
            sen = copy.deepcopy(input_list[i - count])
            sen.replace('~', '')
            if len(sen) == 0:
                neg = input_list[i - count]
                del input_list[i - count]
                input_list[i - count] = neg + input_list[i - count]
                count += 1

    def _createSentences(self, input_list):
        if type(input_list) is not list:
            return Atom(input_list)

        negations = 0
        i = 0

        while input_list[i] == '~':
            negations += 1
            i += 1

        left_sen = self._createSentences(input_list[i])
        if left_sen is None:
            return None

        i += 1

        while negations > 0:
            left_sen.negate()
            negations -= 1

        # If given a negated atom
        if i == len(input_list):
            return left_sen

        oper = input_list[i]
        if oper not in LogicSymbols.OP_CONVERT:
            self.forget_all()
            self.add_text('Unrecognized operator: ' + oper, 0)
            return None
        i += 1

        while input_list[i] == '~':
            negations += 1
            i += 1

        right_sen = self._createSentences(input_list[i])
        if right_sen is None:
            return None

        while negations > 0:
            right_sen.negate()
            negations -= 1

        return Sentence(left_sen, right_sen, oper)

    def parseInput(self, user_in):
        results_list = self._recurInput(iter(user_in))[0]

        return self._createSentences(results_list)

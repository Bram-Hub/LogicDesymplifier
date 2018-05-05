from logicobjects import Sentence
from logicobjects import Atom
import copy


class CondEquiv(object):

    def implication(sen):
        if type(sen) is not Sentence or sen.get_negations() != 0:
            return sen

        if sen.oper is '$':
            if sen.get_negations() == 0:
                left_new = copy.deepcopy(sen.left_sen)
                left_new.negate()

                new_sen = Sentence(left_new, sen.right_sen,
                                   '|', sen.get_negations(), sen.get_steps())
                new_sen.add_step('IMPLI')
                return new_sen
            else:
                right_new = copy.deepcopy(sen.right_sen)
                right_new.negate()

                new_sen = Sentence(sen.left_sen, right_new,
                                   '&', sen.get_negations(), sen.get_steps())
                new_sen.add_step('IMPLI')
                return new_sen
        elif sen.oper is '|':
            if sen.get_negations() == 0:
                left_new = copy.deepcopy(sen.left_sen)
                left_new.negate()

                new_sen = Sentence(left_new, sen.right_sen,
                                   '$', sen.get_negations(), sen.get_steps())
                new_sen.add_step('IMPLI')
                return new_sen
            else:
                return sen
        elif sen.oper is '&':
            if sen.get_negations() == 0:
                right_new = copy.deepcopy(sen.right_sen)
                right_new.negate()

                new_sen = Sentence(sen.left_sen, right_new,
                                   '$', 1, sen.get_steps())
                new_sen.add_step('IMPLI')
                return new_sen
            else:
                return sen

    def contrapostion(sen):
        if type(sen) is not Sentence or sen.get_negations() != 0:
            return sen

        if sen.oper is not '$':
            return sen

        left_new = copy.deepcopy(sen.right_sen)
        left_new.negate()

        right_new = copy.deepcopy(sen.left_sen)
        right_new.negate()

        new_sen = Sentence(left_new, right_new, '$',
                           sen.get_negations(), sen.get_steps())
        new_sen.add_step('CONTR')
        return new_sen

    def exportation(sen):
        if type(sen) is not Sentence or sen.get_negations() != 0:
            return sen

        if sen.oper is not '$':
            return sen

        sen = copy.deepcopy(sen)

        if type(sen.right_sen) is Sentence and sen.right_sen.oper is '$' and sen.right_sen.get_negations() == 0:

            new_sen = Sentence(
                Sentence(sen.left_sen, sen.right_sen.left_sen, '&'), sen.right_sen.right_sen, '$', sen.get_negations(), sen.get_steps())
            new_sen.add_step('EXPOR')
        elif type(sen.left_sen) is Sentence and sen.left_sen.oper is '&' and sen.left_sen.get_negations() == 0:
            new_sen = Sentence(sen.left_sen.left_sen, Sentence(
                sen.left_sen.right_sen, sen.right_sen, '$'), '$', sen.get_negations(), sen.get_steps())
            new_sen.add_step('EXPOR')

        return sen

    # TODO: write reverse rules
    def distribution(sen):
        if type(sen) is not Sentence or sen.get_negations() != 0:
            return sen

        sen = copy.deepcopy(sen)
        if sen.oper is '$':
            if type(sen.right_sen) is Sentence and sen.right_sen.get_negations() == 0:
                if sen.right_sen.oper is '&':
                    left_new = Sentence(
                        sen.left_sen, sen.right_sen.left_sen, '$')
                    right_new = Sentence(
                        sen.left_sen, sen.right_sen.right_sen, '$')

                    new_sen = Sentence(left_new, right_new,
                                       '&', sen.get_negations(), sen.get_steps())
                    new_sen.add_step('DISTR')
                    return new_sen

                elif sen.right_sen.oper is '|':
                    left_new = Sentence(
                        sen.left_sen, sen.right_sen.left_sen, '$')

                    right_new = Sentence(sen.left_sen,
                                         sen.right_sen.right_sen, '$')

                    new_sen = Sentence(left_new, right_new,
                                       '|', sen.get_negations(), sen.get_steps())
                    new_sen.add_step('DISTR')
                    return new_sen

            elif type(sen.left_sen) is Sentence and sen.left_sen.get_negations() == 0:
                if sen.left_sen.oper is '&':
                    left_new = Sentence(
                        sen.left_sen.left_sen, sen.right_sen, '$')
                    right_new = Sentence(
                        sen.left_sen.right_sen, sen.right_sen, '$')

                    new_sen = Sentence(
                        left_new, right_new, '|', sen.get_negations(), sen.get_steps())
                    new_sen.add_step('DISTR')
                    return new_sen

                elif sen.left_sen.oper is '|':
                    left_new = Sentence(
                        sen.left_sen.left_sen, sen.right_sen, '$')
                    right_new = Sentence(
                        sen.left_sen.right_sen, sen.right_sen, '$')

                    new_sen = Sentence(
                        left_new, right_new, '&', sen.get_negations(), sen.get_steps())
                    new_sen.add_step('DISTR')
                    return new_sen

        return sen

    # TODO: write reverse rules
    def reduction(sen):
        if type(sen) is not Sentence or sen.get_negations() != 0:
            return sen

        if sen.oper is '&':
            if type(sen.left_sen) is Sentence \
                    and sen.left_sen.oper is '$' and sen.left_sen.get_negations() == 0:

                if sen.right_sen == sen.left_sen.left_sen:

                    sen = copy.deepcopy(sen)

                    new_sen = Sentence(
                        sen.right_sen, sen.left_sen.right_sen, '&', sen.get_negations(), sen.get_steps())
                    new_sen.add_step('REDUC')
                    return new_sen

                elif sen.right_sen.trueVal() == sen.left_sen.right_sen.trueVal() \
                        and sen.right_sen.get_negations() % 2 != sen.left_sen.right_sen.get_negations() % 2:
                    sen = copy.deepcopy(sen)

                    sen.left_sen.left_sen.negate()

                    new_sen = Sentence(
                        sen.right_sen, sen.left_sen.left_sen, '&', sen.get_negations(), sen.get_steps())
                    new_sen.add_step('REDUC')
                    return new_sen

            elif type(sen.right_sen) is Sentence \
                    and sen.right_sen.oper is '$' and sen.right_sen.get_negations() == 0:

                if sen.left_sen == sen.right_sen.left_sen:

                    sen = copy.deepcopy(sen)

                    new_sen = Sentence(
                        sen.left_sen, sen.right_sen.right_sen, '&', sen.get_negations(), sen.get_steps())
                    new_sen.add_step('REDUC')
                    return new_sen

                elif sen.left_sen.trueVal() == sen.right_sen.right_sen.trueVal() \
                        and sen.left_sen.get_negations() % 2 != sen.right_sen.right_sen.get_negations() % 2:

                    sen = copy.deepcopy(sen)

                    sen.right_sen.left_sen.negate()
                    sen.right_sen.left_sen.clean()

                    new_sen = Sentence(
                        sen.left_sen, sen.right_sen.left_sen, '&', sen.get_negations(), sen.get_steps())
                    new_sen.add_step('REDUC')
                    return new_sen

        return sen

    def idempotence(sen):
        if type(sen) is Atom:
            left_new = copy.deepcopy(sen)
            right_new = copy.deepcopy(sen)
            left_new.negate()

            new_sen = Sentence(left_new, right_new, '$',
                               sen.get_negations(), sen.get_steps())

            new_sen.add_step('IDEMP')

            return new_sen
        elif sen.oper is '$' and sen.get_negations() == 0:
            if sen.left_sen.trueVal() == sen.right_sen.trueVal() \
                    and sen.left_sen.get_negations() % 2 != sen.right_sen.get_negations() % 2:
                sen = copy.deepcopy(sen.left_sen)
                sen.negate()
                sen.add_step('IDEMP')
                return sen

        return sen


class BoolEquiv(object):

    def association(sen):
        if type(sen) is not Sentence:
            return sen

        if sen.oper is '&' or sen.oper is '|':
            if type(sen.left_sen) is Sentence and sen.left_sen.oper is sen.oper:
                sen = copy.deepcopy(sen)
                new_sen = Sentence(sen.left_sen.left_sen, Sentence(
                    sen.left_sen.right_sen, sen.right_sen, sen.oper), sen.oper, sen.get_negations(), sen.get_steps())
                new_sen.add_step('ASSOC')
                return new_sen
            elif type(sen.right_sen) is Sentence and sen.right_sen.oper is sen.oper:
                sen = copy.deepcopy(sen)
                new_sen = Sentence(Sentence(sen.left_sen, sen.right_sen.left_sen,
                                            sen.oper), sen.right_sen.right_sen, sen.oper, sen.get_negations(), sen.get_steps())
                new_sen.add_step('ASSOC')
                return new_sen

        return sen

    def commutation(sen):
        if type(sen) is not Sentence:
            return sen

        if sen.oper is '&' or sen.oper is '|':
            sen = copy.deepcopy(sen)

            new_sen = Sentence(sen.right_sen, sen.left_sen,
                               sen.oper, sen.get_negations(), sen.get_steps())
            new_sen.add_step('COMMU')
            return new_sen

        return sen

    def doubleNegation(sen):
        if sen.get_negations() == 2:
            sen = copy.deepcopy(sen)
            sen.set_negations(0)
            sen.add_step('DNEGA')
            return sen

        return sen

    def deMorgan(sen):
        if type(sen) is not Sentence:
            return sen

        if (sen.oper is '&' or sen.oper is '|') and sen.get_negations() > 0:
            sen = copy.deepcopy(sen)
            sen.set_negations(1)

            sen.left_sen.negate()
            sen.right_sen.negate()
            sen.oper = '&' if sen.oper is '|' else '|'
            sen.add_step('DEMORG')
            return sen

        return sen

    # TODO: write reverse rules
    def distribution(sen):
        if type(sen) is not Sentence:
            return sen

        sen = copy.deepcopy(sen)

        if sen.oper is '&':
            if type(sen.left_sen) is Sentence and sen.left_sen.oper is '|':
                new_sen = Sentence(Sentence(sen.right_sen, sen.left_sen.left_sen, '&'), Sentence(
                    sen.right_sen, sen.left_sen.right_sen, '&'), '|', sen.get_negations(), sen.get_steps())
                new_sen.add_step('DISTR')
                return new_sen
            elif type(sen.right_sen) is Sentence and sen.right_sen.oper is '|':
                new_sen = Sentence(Sentence(sen.left_sen, sen.right_sen.left_sen, '&'), Sentence(
                    sen.left_sen, sen.right_sen.right_sen, '&'), '|', sen.get_negations(), sen.get_steps())
                new_sen.add_step('DISTR')
                return new_sen
        elif sen.oper is '|':
            if type(sen.left_sen) is Sentence and sen.left_sen.oper is '&':
                new_sen = Sentence(Sentence(sen.right_sen, sen.left_sen.left_sen, '|'), Sentence(
                    sen.right_sen, sen.left_sen.right_sen, '|'), '&', sen.get_negations(), sen.get_steps())
                new_sen.add_step('DISTR')
                return new_sen
            elif type(sen.right_sen) is Sentence and sen.right_sen.oper is '&':
                new_sen = Sentence(Sentence(sen.left_sen, sen.right_sen.left_sen, '&'), Sentence(
                    sen.left_sen, sen.right_sen.right_sen, '|'), '&', sen.get_negations(), sen.get_steps())
                new_sen.add_step('DISTR')
                return new_sen

        return sen

    def absorption(sen):
        pass

    def reduction(sen):
        pass

    def adjaceny(sen):
        pass

from logicobjects import Sentence
from logicobjects import Atom
from equivalencerules import CondEquiv
from equivalencerules import BoolEquiv
import copy
import inspect


def runAll(sen):
    sentences = []

    cond_equiv = inspect.getmembers(CondEquiv, predicate=inspect.isfunction)

    for method in cond_equiv:
        result = method[1](sen)

        if result != sen and result is not None:
            sentences.append(result)

    return sentences


def recurseRunAll(sen):
    print('Received ', sen)
    if type(sen) is Atom:
        return [sen]

    sentences = []
    sen = copy.deepcopy(sen)

    left_sens = recurseRunAll(sen.left_sen)
    right_sens = recurseRunAll(sen.right_sen)

    for left_sen in left_sens:
        for right_sen in right_sens:
            new_sen = Sentence(left_sen, right_sen, sen.oper)

            results = runAll(new_sen)

            for result in results:
                if result not in sentences:
                    sentences.append(result)

    return sentences

if __name__ == "__main__":
    solutions = []

    print('CONDITIONAL EQUIVALENCES')

    implic = Sentence(Sentence('P', 'Q', '$', 2), 'R', '$')
    sen = CondEquiv.implication(implic)

    print('Implication')
    print(implic)
    print(sen)
    print()

    contra = Sentence('P', 'Q', '$')
    sen = CondEquiv.contrapostion(contra)
    sen2 = CondEquiv.contrapostion(sen)

    print('Contraposition')
    print(contra)
    print(sen)
    print()
    print(sen)
    print(sen2)
    print()

    export = Sentence('P', Sentence('Q', 'R', '$'), '$')
    sen = CondEquiv.exportation(export)
    sen2 = CondEquiv.exportation(sen)

    print('Exportation:')
    print(export)
    print(sen)
    print()
    print(sen)
    print(sen2)
    print()

    distrib = Sentence('P', Sentence('Q', 'R', '&'), '$')
    sen = CondEquiv.distribution(distrib)
    distrib2 = Sentence('P', Sentence('Q', 'R', '|'), '$')
    sen2 = CondEquiv.distribution(distrib2)
    distrib3 = Sentence(Sentence('P', 'Q', '|'), 'R', '$')
    sen3 = CondEquiv.distribution(distrib3)
    distrib4 = Sentence(Sentence('P', 'Q', '&'), 'R', '$')
    sen4 = CondEquiv.distribution(distrib4)

    print('Distribution')
    print(distrib)
    print(sen)
    print()
    print(distrib2)
    print(sen2)
    print()
    print(distrib3)
    print(sen3)
    print()
    print(distrib4)
    print(sen4)
    print()
    print()

    reduc = Sentence('P', Sentence('P', 'Q', '$'), '&')
    sen = CondEquiv.reduction(reduc)

    reduc2 = Sentence(Sentence('P', 'Q', '$'), 'P', '&')
    sen2 = CondEquiv.reduction(reduc2)

    reduc3 = Sentence('~Q', Sentence('P', 'Q', '$'), '&')
    sen3 = CondEquiv.reduction(reduc3)

    reduc4 = Sentence(Sentence('P', 'Q', '$'), '~Q', '&')
    sen4 = CondEquiv.reduction(reduc4)

    print('Reduction')
    print(reduc)
    print(sen)
    print(reduc2)
    print(sen2)
    print(reduc3)
    print(sen3)
    print(reduc4)
    print(sen4)
    print()
    print()

    idempo = Sentence('P', '~P', '$')
    sen = CondEquiv.idempotence(idempo)
    idempo2 = Sentence('~P', 'P', '$')
    sen2 = CondEquiv.idempotence(idempo2)
    idempo3 = Atom('P', 1)
    sen3 = CondEquiv.idempotence(idempo3)

    print('Idempotence')
    print(idempo)
    print(sen)
    print()
    print(idempo2)
    print(sen2)
    print()
    print(idempo3)
    print(sen3)
    print()
    print()

    print('BOOLEAN EQUIVALENCES')

    assoc = Sentence('P', Sentence('Q', 'R', '&'), '&')
    sen = BoolEquiv.association(assoc)

    print('Association')
    print(assoc)
    print(sen)
    print()
    print()

    sen1 = Sentence('P', Sentence('Q', 'R', '$'), '&')
    sen2 = Sentence('P', Sentence('Q', 'R', '$'), '&')

    print('Equivalency Test')
    if sen1 == sen2:
        print(sen1, ' equals', sen2)
    else:
        print(sen1, ' does not equal ', sen2)

    print()
    sentences = recurseRunAll(sen1)
    print('Run all conditional equivalences for ', sen1, ':')
    for sentence in sentences:
        print(sentence)

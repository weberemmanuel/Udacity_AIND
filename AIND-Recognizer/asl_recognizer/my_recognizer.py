import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    xl = test_set.get_all_Xlengths()
    for n in range(0,len(xl)):
        X, lengths = xl[n]

        best_score = None
        best_word  = None
        prob_dict = dict()

        for word,model in models.items():
            try:
                score = model.score(X, lengths)
            except:
                score = float("-Inf")

            if best_score == None or score > best_score:
                best_score = score
                best_word  = word

            prob_dict[word] = score
        probabilities.append(prob_dict)
        guesses.append(best_word)

    return (probabilities , guesses)

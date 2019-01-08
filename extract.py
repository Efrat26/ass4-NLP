#Osnat Drien 302673298 & Efrat Sofer 304855125
import sys

def getWordsCOnnctedByHyphen(sentence, word_index):
    word_ind_in_list = word_index - 1
    if len(sentence) == word_index:#if it's the last word in sentence:
        return [False, '']
    current_word = sentence[word_ind_in_list]
    splitted_word = current_word.split('\t')
    next_sentence = sentence[word_ind_in_list + 1]
    splitted_next = next_sentence.split('\t')
    if len(splitted_next) < 8:
        print('hello')
    if splitted_next[1] == '-':
        word = ''
        end_of_entity = int(splitted_word[5])
        if end_of_entity < word_index:
            return [False, '']
        for i in range(word_ind_in_list, end_of_entity):
            temp_sentece = sentence[i]
            splitted_temp = temp_sentece.split('\t')
            word += splitted_temp[1]
        return [True, word]
    else:
        return [False, '']

def handleConjunction(whole_sentence, current_sentence_splitted):
    #check the head of it
    head_conj = int(current_sentence_splitted[5])
    if head_conj != 0:  # conj is the root - not likely
        #current_sentence = input_lines_as_sentences[counter]
        head_part = whole_sentence[head_conj - 1]
        splitted_head = head_part.split('\t')
        real_classifcation = None
        if splitted_head[-1].lower() == 'person' or splitted_head[-1].lower() == 'gpe':
            if head_conj < int(current_sentence_splitted[0]):  # head is before this line - search after
                start_ind = int(current_sentence_splitted[0])
                end_ind = len(whole_sentence)
                real_classifcation = splitted_head[-1]
            else:
                for j in range(int(current_sentence_splitted[0]) - 1, 0, -1):# search for the real classification
                    temp_sentence_for_real_classification = whole_sentence[j]
                    temp_sentence_for_real_classification_splitted = \
                        temp_sentence_for_real_classification.split('\t')
                    if temp_sentence_for_real_classification_splitted[-1] == 'GPE' or \
                            temp_sentence_for_real_classification_splitted[-1] == 'PERSON':
                        real_classifcation = temp_sentence_for_real_classification_splitted[-1]
                        break
                    return [splitted_head[1], real_classifcation]
                start_ind = 0
                end_ind = int(current_sentence_splitted[0])
            for i in range(start_ind, end_ind):
                temp_sentence = whole_sentence[i]
                splitted_temp = temp_sentence.split('\t')
                if int(splitted_temp[5]) == head_conj:
                    if splitted_head[-1] != splitted_temp[-1]:
                        if real_classifcation != None:
                            #real_classifcation = splitted_temp[-1]
                            return [splitted_temp[1], real_classifcation]
                        else:
                            print('should not happen')
    return None

def main():
    #get input file name & open it
    try:
        input_file_name = sys.argv[1]# input should be a file in the .processed form
    except(ValueError, IndexError):
        print("no input file given")
        input_file_name = 'Corpus.TRAIN.processed'
    #output file
    output_file_name = 'predicted_results'
    if input_file_name.lower().__contains__('train'):
        output_file_name+= '_TRAIN'
    elif input_file_name.lower().__contains__('dev'):
        output_file_name += '_DEV'
    else:
        output_file_name += '_other'
    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')
    #read lines
    input_lines = input_file.read().splitlines()
    result_dict = {}
    #split to sentences
    place = None
    person = None
    sentence_id = None
    whole_sentence = None
    person_relates_to_dict = {}  # addition - round 2
    person_index = None
    place_relates_to_dict = {}  # addition - round 3
    place_index = None
    # check the input lines into sentences:
    input_lines_as_sentences = []
    gathered_sentence = []
    for sentence in input_lines:
        if sentence.startswith('#id') or sentence.startswith("#text:"):
            continue
        if sentence != "":
            gathered_sentence.append(sentence)
        else:
          #  copied_list = gathered_sentence.copy()
            input_lines_as_sentences.append(gathered_sentence)
            gathered_sentence = []


    problematic_ner_tags = set()
    counter = 0
    conj_error = False
    word_to_real_classification = {}
    for sentence in input_lines:
        if sentence.startswith('#id: sent27'):
            print('hello')
        if sentence.startswith('#id'):
            splitted_sentence = sentence.split(" ")
            sentence_id = splitted_sentence[1]
        elif sentence.startswith("#text:"):
            #splitted_sentence = sentence.split("#text")
            whole_sentence = sentence[6:]
        else:
            splitted_sentence = sentence.split('\t')
            if len(splitted_sentence) == 9:
               # if splitted_sentence[1].lower() == 'lazio':
                 #   print('hello')
                if splitted_sentence[-1] == 'GPE' and splitted_sentence[1] not in problematic_ner_tags:
                    place = splitted_sentence[1]
                    # '''#changes for round3
                    place_index = int(splitted_sentence[0])
                    if place not in place_relates_to_dict:
                        relations_place = set()
                        relations_place.add(int(splitted_sentence[5]))
                        place_relates_to_dict[place] = relations_place
                    else:
                        place_relates_to_dict[place].add(int(splitted_sentence[5]))
                        # '''
                    ret_val = getWordsCOnnctedByHyphen(input_lines_as_sentences[counter], place_index)
                    if ret_val[0] == True:
                        place = ret_val[1]
                elif splitted_sentence[-1] == 'PERSON' and splitted_sentence[1] not in problematic_ner_tags:
                    person = splitted_sentence[1]
                    #'''#changes for round2
                    person_index = int(splitted_sentence[0])
                    if person not in person_relates_to_dict:
                        relations = set()
                        relations.add(int(splitted_sentence[5]))
                        person_relates_to_dict[person] = relations
                    else:
                        person_relates_to_dict[person].add(int(splitted_sentence[5]))
                        #'''
                    ret_val = getWordsCOnnctedByHyphen(input_lines_as_sentences[counter], person_index)
                    if ret_val[0] == True:
                        person = ret_val[1]
                #handling conjunction
                elif splitted_sentence[1].lower() == 'and' or splitted_sentence[1].lower() == 'or':
                   ret_val = handleConjunction(input_lines_as_sentences[counter], splitted_sentence)
                   if ret_val != None:
                       word_to_real_classification[ret_val[0]] = ret_val[1]
            elif sentence == '': #new sentence
                #find the persons that relates to the person selected and concat them
               # '''#changes for round2
                if person != None:
                    new_person = ''
                    for key in person_relates_to_dict:
                        other_person_set = person_relates_to_dict[key]
                        if person_index in other_person_set:
                            new_person += key + ' '
                    person = new_person + person
                    #'''

                    # '''#changes for round3
                    if place != None:
                        new_place = ''
                        for key in place_relates_to_dict:
                            other_place_set = place_relates_to_dict[key]
                            if place_index in other_place_set:
                                new_place += key + ' '
                        place = new_place + place
                        # '''
                #person_index < place_index and - addition for round 4 which we took out
                if conj_error == False and place!= None and person != None and sentence_id!= None and whole_sentence!= None:
                    if person in word_to_real_classification and word_to_real_classification[person] != 'PERSON':
                        print('person: ' +person +   ' is a place!')
                    if place in word_to_real_classification and word_to_real_classification[place] != 'GPE':
                        print('place: ' + place + ' is a person!')
                    else:
                        sentence_to_write = sentence_id + '\t' + person + '\t' + 'Live_In' + \
                                            '\t' + place + '\t' + '('+ whole_sentence + ')\n'
                        output_file.write(sentence_to_write)
                        result_dict[sentence_id] = person + '\t' + 'Live_In' + '\t' + place
                # round 4- correction to the algorithm
                person_relates_to_dict = {}  # addition - round 2
                person_index = None
                place_relates_to_dict = {}  # addition - round 3
                place_index = None
                person = None
                place = None
                sentence_id = None
                whole_sentence = None
                counter += 1
                conj_error = False
                problematic_ner_tags.clear()
                word_to_real_classification = {}

    ###try parser
    ''''
    parser = DependencyParser(nlp.vocab)
    losses = {}
    optimizer = nlp.begin_training()
    parser.update([doc1, doc2], [gold1, gold2], losses=losses, sgd=optimizer)
'''


if __name__ == "__main__":
    main()
#Osnat Drien 302673298 & Efrat Sofer 304855125
import sys
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
    for sentence in input_lines:
        if sentence.startswith('#id'):
            splitted_sentence = sentence.split(" ")
            sentence_id = splitted_sentence[1]
        elif sentence.startswith("#text:"):
            #splitted_sentence = sentence.split("#text")
            whole_sentence = sentence[6:]
        else:
            splitted_sentence = sentence.split('\t')
            if len(splitted_sentence) == 9:
                if splitted_sentence[1].lower() == 'lazio':
                    print('hello')
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
                #handling conjunction
                elif splitted_sentence[1].lower() == 'and' or  splitted_sentence[1].lower() == 'or':
                    #check the head of it
                    head_conj = int(splitted_sentence[5])
                    if head_conj == 0: # conj is the root - not likely
                        print("root")
                    else:
                        current_sentence = input_lines_as_sentences[counter]
                        head_part = current_sentence[head_conj - 1]
                        splitted_head = head_part.split('\t')
                        if splitted_head[-1].lower() == 'person' or splitted_head[-1].lower() == 'gpe':
                            if head_conj < int(splitted_sentence[0]): # head is before this line - search after
                                start_ind = int(splitted_sentence[0])
                                end_ind = len(current_sentence)
                            else:
                                start_ind = 0
                                end_ind = int(splitted_sentence[0])
                            for i in range(start_ind, end_ind):
                                temp_sentence = current_sentence[i]
                                splitted_temp = temp_sentence.split('\t')
                                if int(splitted_temp[5]) == head_conj:
                                    if splitted_head[-1] != splitted_temp[-1]:
                                        conj_error = True
                                        problematic_ner_tags.add(splitted_head[1])
                                        problematic_ner_tags.add(splitted_temp[1])
                                    else:
                                        conj_error = False
                                    break
                            #conj_error = True

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

    ###try parser
    ''''
    parser = DependencyParser(nlp.vocab)
    losses = {}
    optimizer = nlp.begin_training()
    parser.update([doc1, doc2], [gold1, gold2], losses=losses, sgd=optimizer)
'''


if __name__ == "__main__":
    main()
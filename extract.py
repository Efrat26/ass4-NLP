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
                if splitted_sentence[-1] == 'GPE':
                    place = splitted_sentence[1]
                elif splitted_sentence[-1] == 'PERSON':
                    person = splitted_sentence[1]

                    person_index = int(splitted_sentence[0])
                    if person not in person_relates_to_dict:
                        relations = set()
                        relations.add(int(splitted_sentence[5]))
                        person_relates_to_dict[person] = relations
                    else:
                        person_relates_to_dict[person].add(int(splitted_sentence[5]))

            elif sentence == '': #new sentence
                #find the persons that relates to the person selected and concat them
                if person != None:
                    new_person = ''
                    for key in person_relates_to_dict:
                        other_person_set = person_relates_to_dict[key]
                        if person_index in other_person_set:
                            new_person += key + ' '
                    person = new_person + person
                if place!= None and person != None and sentence_id!= None and whole_sentence!= None:
                    sentence_to_write = sentence_id + '\t' + person + '\t' + 'Live_In' + \
                                        '\t' + place + '\t' + '('+ whole_sentence + ')\n'
                    output_file.write(sentence_to_write)
                    result_dict[sentence_id] = person + '\t' + 'Live_In' + '\t' + place
                    place = None
                    person = None
                    sentence_id = None
                    whole_sentence = None
                person_relates_to_dict = {}  # addition - round 2
                person_index = None



if __name__ == "__main__":
    main()
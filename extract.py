#Osnat Drien 302673298 & Efrat Sofer 304855125
import sys
def main():
    #get input file name & open it
    try:
        input_file_name = sys.argv[1]
    except(ValueError, IndexError):
        print("no input file given")
        input_file_name = 'Corpus.TRAIN.processed'
        # get output file name & open it
    try:
        output_file_name = sys.argv[2]
    except(ValueError, IndexError):
        print("no output file given")
        output_file_name = 'predicted_results'
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
    #compare to the real relations
    try:
        gold_file_name = sys.argv[3]
    except(ValueError, IndexError):
        print("no gold label file given")
        gold_file_name = 'TRAIN.annotations'
    gold_label_file = open(gold_file_name, 'r')
    gold_lines = gold_label_file.read().splitlines()
    total_number_of_lines_with_livein = 0
    correct_predicted_lines = 0
    for line in gold_lines:
        splitted_sentence = line.split('\t')
        if splitted_sentence[2].lower() == 'live_in':
            total_number_of_lines_with_livein += 1
            if splitted_sentence[0] in result_dict:
                temp = splitted_sentence[1] + '\t' + splitted_sentence[2] + '\t' + splitted_sentence[3]
                if temp == result_dict[splitted_sentence[0]]:
                    correct_predicted_lines += 1
    accuracy = (float(correct_predicted_lines)/float(total_number_of_lines_with_livein))*100.0
    print("accuracy percentage is: " + str(accuracy))




if __name__ == "__main__":
    main()
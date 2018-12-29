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
            elif sentence == '': #new sentence
                if place!= None and person != None and sentence_id!= None and whole_sentence!= None:
                    sentence_to_write = sentence_id + '\t' + person + '\t' + 'Live_In' + \
                                        '\t' + place + '\t' + '('+ whole_sentence + ')\n'
                    output_file.write(sentence_to_write)
                    place = None
                    person = None
                    sentence_id = None
                    whole_sentence = None



if __name__ == "__main__":
    main()
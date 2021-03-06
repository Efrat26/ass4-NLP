#Osnat Drien 302673298 & Efrat Sofer 304855125
import sys
from collections import defaultdict
def main():
    #file names
    gold_file_name = sys.argv[1]
    predict_file_name = sys.argv[2]
    #create file object
    gold_file = open(gold_file_name, 'r')
    predict_file = open(predict_file_name, 'r')
    #read & split the lines
    gold_lines = gold_file.read().splitlines()
    predicted_lines = predict_file.read().splitlines()
    #if len(gold_lines) != len(predicted_lines):
        #print("result files aren't the same length")
    relation = 'live_in'
    gold_num_of_lines_has_relation = 0
    #predict_num_of_lines_has_relation = 0
    num_of_predicted_correctly = 0
    num_of_precision_mistakes = 0
    num_of_recall_mistakes = 0
    predicted_lines_dict = defaultdict(set)
    gold_lines_dict = defaultdict(set)
    #preprocess: make a dictionary which maps a sentence num to the value:

    num_of_all_predictions = len(predicted_lines)
    for line in predicted_lines:
        splitted_line = line.split('\t')
        if splitted_line[3].endswith('.'):#ignore names end with dot
            splitted_line[3] = (splitted_line[3])[:-1]
        predicted_lines_dict[splitted_line[0]].add(splitted_line[1] + '\t' + splitted_line[2] + '\t' + splitted_line[3])
    for line in gold_lines:
        splitted_line = line.split('\t')
        if splitted_line[3].endswith('.'):#ignore names end with dot
            splitted_line[3] = (splitted_line[3])[:-1]
        gold_lines_dict[splitted_line[0]].add(splitted_line[1] + '\t' + splitted_line[2] + '\t' + splitted_line[3])
    ''''    
    precision mistakes: relations that are in the predicted file but not in the gold file.
    recall mistakes: relations that are not in the predicted file but are in the gold file.
    F1 = 2*(precision*recall/precision+recall)
    '''
    #compare:
    for key in gold_lines_dict:
        current_gold_line_set = gold_lines_dict[key]
        for line in current_gold_line_set:
            splitted_gold_line = line.split('\t')
            if splitted_gold_line[1].lower() == relation:#number of lines in the gold file has the relation we're intrested in
                gold_num_of_lines_has_relation += 1
                # check if the sentence is also in the predicted file using dictionary:
                if key in predicted_lines_dict:
                    # check if predicted correctly:
                    if line in predicted_lines_dict[key] :  # predicted correctly
                        num_of_predicted_correctly += 1
                    else:  # recall mistake
                        num_of_recall_mistakes += 1
    #check for precision mistakes
    for key in predicted_lines_dict:
        current_pred_line_set = predicted_lines_dict[key]
        for line in current_pred_line_set:
            splitted_pred_line = line.split('\t')
            if splitted_pred_line[1].lower() == relation and line not in gold_lines_dict[key]: #precision mistake
                num_of_precision_mistakes += 1

    ''''
    precision = num correct predictions / num all predictions
    recall = num correct predictions / num of gold segments
    F1 = precision*recall / precision + recall
    '''
    #calculations:
    recall = float(num_of_predicted_correctly) / float(gold_num_of_lines_has_relation)
    precision = float(num_of_predicted_correctly) / float(num_of_all_predictions)
    f1 = (2.0*float(recall*precision)) / float(recall + precision)
    print("value of recall is: " + str(recall))
    print("value of precision is: " + str(precision))
    print("F1 is: " + str(f1))



if __name__ == "__main__":
    main()
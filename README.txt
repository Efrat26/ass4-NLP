To run extract script you should enter a file of type .processed.
The script outputs a file with predictions in the annotations format. The name of the output file will be one of the followings:
•	If the input file contains the word train in it, them the name will be predicted_results_TRAIN.
•	If the input file contains the word dev in it, then the name will be predicted_results_dev.
•	In any other case - the name will be predicted_results_other.
It was easier for us to run the script on both the train&dev and keep the results for comparison instead of override each other.
To run the eval script you should enter 2 files as explained in the instructions (assuming the first one is the gold file and the second one is the file contains the predictions).
The program will print to screen the result of each measure (recall, precision, f1).

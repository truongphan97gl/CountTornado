import gzip
from matplotlib import pyplot as plt
import operator
import sys
import pandas as pd
def main(argv):
    """
    This functions reads weather file,
    calls functions to accumulate, 
    displays tornado totals by state 
    @param argv: command line arguments
    """    
    
    infile = gzip.open(argv[0], 'rt')   
    infile1 = gzip.open(argv[1], 'rt')  
    #infile1 = gzip.open(argv[1], 'rt')  # open gzipped file in read text mode 
    print("Processing file:", argv[0]) 
    year = argv[0][37:41]
    df = generate_file_stats(infile,year)
    # state_counts = accumulate_tornadoes(infile)
   # display_state_counts(state_counts)
   # build_histogram(state_counts)
    print("Processing file:", argv[1]) 
    year = argv[1][37:41]
    df1 = generate_file_stats(infile1,year)

    frame = [df,df1]
    result = pd.concat(frame)
    generate_boxplot(result)
    return
    

def accumulate_tornadoes(infile):
    """
    This functions takes in the weather file, parses it, 
    and builds a dict that contains the tornado counts by state,
    i.e. [state:count].
    Make sure to account for states that may have no tornados.
    @param infile: weather file object
    @return: dictionary of state tornado counts; key= state, value = tornado count for that state.
    """
    myDict = dict()
    for line in infile:
        line = line.split(",")   

        if(line[12].strip('"') == 'Tornado'):
            myDict[line[8]] = myDict.get(line[8],0) + 1
    return myDict

    
def display_state_counts(state_counts):
    """ 
    This functions takes in dictionary of state tornado counts,
    sorts them by count descending, and
    print the top 5 states and counts to the console.
    @param state_counts: dictionary of state tornado counts.
    @return: None
    """
    count = 0
    sorted_dict = sorted(state_counts.items(), key=operator.itemgetter(1), reverse=True)
    #print(sorted_dict)
    for state in sorted_dict:
        if(count < 5):
            print(state[0] + " : " + str(state[1]))
            count +=1
    return
def build_histogram(state_counts):
    """
    This functions takes in a dictionary of (state:tornado_counts),
    It builds a list of just the counts.
    It then creates a histogram grouping the states by how many tornados they had (in blocks of 20).
    It then displays the histogram in a pop-up.
    @param state_counts: dictionary of state tornado counts.
    @return: None
    """

    tornado_counts = []
    for count in state_counts.values():
        tornado_counts.append(count)
    bins = range(0,180,20)
    plt.hist(tornado_counts, bins,histtype='bar',rwidth=0.8)
    plt.xlabel("Tornado Count Ranges")
    plt.ylabel("State Counts") 
    plt.title("State Counts by Number of Tornados")
    
    plt.show() 
    return 
def compute_5_number_summary(sorted_counts,year):

    df = pd.DataFrame(sorted_counts,columns = ["State", "Count"])
    df['Year'] = year
    print(df.describe())
    print(df)
    return df

def generate_file_stats(file,year):
    state_counts = accumulate_tornadoes(file)
    sorted_counts = sorted(state_counts.items(), key=operator.itemgetter(1), reverse=True)
    df =  compute_5_number_summary(sorted_counts,year)
    return df

def generate_boxplot(cat_frame):
    cat_frame.boxplot(column = 'Count', by = 'Year',figsize = (7,7))
    plt.title("Tonardo Counts by Year")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.suptitle("")
    plt.show()
    return
if __name__ == "__main__":
    main(sys.argv[1:])
    

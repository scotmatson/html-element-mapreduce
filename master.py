from crawler import Crawler
from mapreduce import MapReduce
import os
import operator
import csv

"""
   Author(s):
       - Scot Matson

   This is the master process that delegates all other processes.
   The overall purpose is to ensure that data is continously coming in,
   being parsed, and being condensed, until some condition is met at which
   point the results shall be evaluated.

   Note: This is actually only executes sequentially. A true MapReduce
   should use parallelism.
"""
def main():
    """
        Contributors:
            - Scot Matson
    """
    # TODO: This needs to be dynamically generated. The data gets destroyed
    #       during runtime - GitHub does not store empty directories.
    #       
    #       Going parallel, we may want to use multiple directories to help
    #       separate data sets, i.e., web1, web2, web3....... etc.
    data_directory = './web_pages/'

    # This is the biggest bottleneck in the application
    # Parallelizing this piece would give a major efficiency boost
    Crawler.crawl_web('http://www.sjsu.edu', 10)

    # Build a list of the files we have
    filepaths = list()
    for filename in os.listdir(data_directory):
        filepaths.append(data_directory + filename)

    map_data = list()
    for filepath in filepaths:
        fh = open(filepath, 'r')
        map_data.append(MapReduce.map(filepaths[0], fh))
        fh.close()
        # Remove files after parsing
        os.remove(filepath)

    intermediate_data = dict()
    # Shuffle data set
    intermediate_data = MapReduce.unshuffle(map_data)

    # Reduce should be condensing the data
    reduced_data = dict()
    reduced_data = MapReduce.reduce(intermediate_data)

    # Output results in reverse sequential ordering by value
    csvfile = open('out/results.csv', 'w')
    writer = csv.writer(csvfile, delimiter=',')
    for tag in sorted(reduced_data, key=reduced_data.get, reverse=True):
        print(tag + ': '+ str(reduced_data[tag]))
        writer.writerow([tag, reduced_data[tag]])
    csvfile.close()

################################################################################
if __name__ == '__main__':
    main()

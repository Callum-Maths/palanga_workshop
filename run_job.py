import os
import numpy as np
import logging
import argparse
from categories_API import response
import csv

if __name__ == "__main__":
    #parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--line", type=float, help = "line of csv file")
    #parser.add_argument("--cuda_device", type=int, default=0, help="CUDA device to use")

    args = parser.parse_args()
    
    #set args
    line = args.line
    #cuda_device = args.cuda_device

    #do the actual training
    res, name = response(line)
    csv_file = "genres_output1.csv"

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([line, name, res])
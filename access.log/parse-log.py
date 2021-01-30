#!/usr/bin/python -tt

"""
Simple program to parse and apache logfile
"""
from __future__ import division
import sys
import os
import operator
file_name = 'ip_date.txt'
# Gets the unique year/month pairs
def unique_months(filename):
  monthly_count = []
  unique_list = []
  input_file = azk(filename)
  for line in input_file:
    mth_ip = line[3].split('/')[1] + " " + line[3].split('/')[2][:4]
    monthly_count.append(mth_ip)
  for line in monthly_count:
    # Special case if we're seeing this word for the first time.
    if line not in unique_list: 
      unique_list.append(line)
  return unique_list
# Top 10 visited urls
def top_urls(final_array):
  # Utility to return the top urls
  url_count = {}  # Map each word to its count
  input_file = azk(final_array)
  print ("\nTop 10 uris accessed (Hits --- uri)" )
  print(50 * "-")
  for line_full in input_file:
    # Special case if we're seeing this word for the first time.
    line = line_full[6]
    if not line in url_count:
      url_count[line] = 1
    else:
      url_count[line] = url_count[line] + 1
  url_count = dict(url_count)
  sorted_visits = sort_visits(url_count)
  x = len(str(sorted_visits[0][1]))
  for i in sorted_visits[:10]:
    y = x - len(str(i[1]))
    z = str(i[1])
    # The following appends space for the shorer ip strings so that hashes are alligned
    while (y > 0):
      z = z + " "
      y = y - 1
    print (z, "\t ---", i[0])
def sort_visits(visits):
  # Sorts the the visitor array by second fie;d
  sorted_visits = sorted(visits.items(), key=operator.itemgetter(1), reverse=True)
  return sorted_visits
def count_visits(final_array):
  """Returns a visitor - visit count for this filename."""
  visitor_count = {}
  input_file = azk(final_array)
  for line_full in input_file:
    line = line_full[0]
    if not line in visitor_count:
     visitor_count[line] = 1
    else:
     visitor_count[line] = visitor_count[line] + 1
  return visitor_count
def azk(filename):
  # Extracts the lines from the log file and adds them to an array - was trying to make sth similar to awk
  final_array = []
  lineList = [line.rstrip('\n') for line in open(filename)]
  for line in lineList:
    temp_list = [x for x in line.strip().split()]
    if len(temp_list) > 0:  # don't append an empty list (blank line)
      final_array.append(temp_list)
  return final_array
def export_f(filename):
  #I will use it for the last function only to speed it up
  final_array = []
  monthly_count = []
  lineList = [line.rstrip('\n') for line in open(filename)]
  for line in lineList:
    temp_list = [x for x in line.strip().split()]
    if len(temp_list) > 0:  # don't append an empty list (blank line)
      final_array.append(temp_list)
  for line in final_array:
    mos_ip = line[3].split('/')[1] + " " + line[3].split('/')[2][:4],",",line[0]
    monthly_count.append(mos_ip)
  with open(file_name, 'w') as f:
    for item in monthly_count:
        f.write("".join(item) + "\n")
  f.close()
def top_visitors(filename):
  print ("\n\n\nTop 10 visitors(Hits --- IP)")
  print(50 * "-")
  visitor_count = count_visits(filename)
  items = sort_visits(visitor_count)
  for item in items[0:10]:
    print item[1], "\t ---", item[0]
def hits_monthly(filename):
  #Total hits per month sorted by month
  monthly_count = []
  unique_list = [] 
  monthly = {}
  print("\n\n\nHits per month(Month --- Hits)")
  print(50 * "-")
  input_file = azk(filename)
  for line in input_file:
    # string 3 is the date string, which we split by /
    if line[7][0:4]== "HTTP":
      count = line[3].split('/')[1] + " " + line[3].split('/')[2][:4]
      monthly_count.append(count)
  # check the number of unique months in the log file
  for line in monthly_count:
    if line not in unique_list:
      unique_list.append(line)

  for x in unique_list:
    print x, "---", monthly_count.count(x)
def unique(filename):
  monthly_count = []
  unique_list = []
  unique = {}
  date_list = []
  input_file = azk(filename)
  print ("\n\n\nUnique visits(Month --- Number of visits)")
  print(50 * "-")
  for line in input_file:
    dates = line[3].split('/')[1] + " " + line[3].split('/')[2][:4]
    mth_ip = line[3].split('/')[1] + " " + line[3].split('/')[2][:4], line[0]
    date_list.append(dates)
    monthly_count.append(mth_ip)
  for line in date_list:
    if line not in unique_list:
      unique_list.append(line)
  # Get unique tuples from list 
  # using set() + list() 
  res = list(set(monthly_count))
  for line in res:
    for x in unique_list:
      if not x in unique:
        unique[x] = 0
      elif x == line[0]:
        unique[x] = unique[x] + 1
  for i in unique_list:
    print i, 'hits count -', unique[i]
def barchart(filename):
  z= {}
  bar = []
  monthly_ip = []
  unique_mos=unique_months(filename)
  export_f(filename)
  mos_ip = open(file_name, 'r')
  # loads the file to list of tuples
  with mos_ip as inputFile:
    ipDateTuples = [tuple(line.strip('\n').split(',')) for line in inputFile.readlines()]
  for mos in unique_mos:
    top_hits = calculate_hits(mos, ipDateTuples)
    #print top10(top_hits)
def calculate_hits(mos, mos_ip):
  list_hits = {}
  total = 0
  print "\n", mos
  print(50 * "-")
  z = ''
  for i in mos_ip:
    if i[0] == mos:
      j = i[1]
      if not j in list_hits:
        list_hits[j] = 1
      else:
        list_hits[j] = list_hits[j] + 1
  list_hits1 = sorted(list_hits.items(), key=operator.itemgetter(1), reverse=True)
  del list_hits1[10:]
  # gets the total number of hits for the current month that is needed for the percentage calc
  for y in list_hits1:
    #total = total + int(y)
    total += int(y[1])
  print "The total hists from top 10 IPs is -", total
  print(50 * "-")
  # this calculates the percentage and will print # for any 1%
  for x in list_hits1:
    y = 15 - len(x[0])
    z = str(x[0])
    #The following appends space for the shorer ip strings so that hashes are alligned
    while (y > 0):
      z = z + " "
      y = y - 1
    # counts the hashes - x is the count for particular ip, total is the sum of hits for top 10
    hashes = x[1] * 100 / total
    print x[1], "\t", z, "\t", int(round(hashes))*"#"
# Define a main() function.
def main():
    filename = raw_input("Enter file to be parsed: ")
    print("What do you need to check? ")
    option = raw_input("1 - urls | 2 - topvisitors| 3 - hits-monthly | 4 - unique-monthly | 5 - barchart | 0 - all: ")
    print ('Parsing', filename)
    print ('Selected option is', option)    
    
    if option == '1':
      top_urls(filename)
    elif option == '2':
      top_visitors(filename)
    elif option == '3':
      hits_monthly(filename)
    elif option == '4':
      unique(filename)
    elif option == '5':
      barchart(filename)
    elif option == '0':
      top_urls(filename)
      top_visitors(filename)
      hits_monthly(filename)
      unique(filename)
      barchart(filename)
    else:
      print('Unknown option')
      sys.exit(1)
if __name__ == '__main__':
  main()	

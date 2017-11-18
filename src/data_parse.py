import csv

csv_file = open("/home/vaquierm/Documents/Sports/Baseball/TeamStats.csv")
 
csv_reader = csv.reader(csv_file, delimiter=',')
 
reduced_set = []
 
for row in csv_reader:
    year_ID = row[0]
    team_ID = row[2]
    rank = row[5]
    win = row[8]
    loss = row[9]
    reduced_set.append([year_ID, team_ID, rank, win, loss])
 
csv_file = open("../data/data.csv", "w")

csv_writer = csv.writer(csv_file, delimiter=',')

csv_writer.writerows(reduced_set)

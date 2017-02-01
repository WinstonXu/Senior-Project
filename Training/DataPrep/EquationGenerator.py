import csv
import os

#
# def makeAllTestData():
#     eq_test = open('eq_test.txt', 'w')
#     with open('all_equations.csv', newline='') as all_equations:
#         equations_reader = csv.reader(all_equations)
#         for row in equations_reader:
#             n1, op, n2 = row[1], row[3], row[5]
#             nf1, of, nf2 = row[0], row[2], row[4]
#             eq_test.write(n1 + op + n2 + '\n')
#             eq_test.write(nf1 + '   ' + of + '   ' + nf2 + '\n')
#
#     all_equations.close()
#
# makeAllTestData()


mnist_dir = 'DatasetPictures/MnistPics'
operators_dir = 'DatasetPictures/Operators'

mnist_nums = open('all_nums.csv', 'w')
operators = open('all_ops.csv', 'w')

for filename in os.listdir(mnist_dir):
    if '.jpg' in filename:
        number = filename.split("-")[1][0]
        mnist_nums.write(filename + ',' + number + '\n')


for filename in os.listdir(operators_dir):
    if '.jpg' in filename:
        operator = filename.split(" ")[0]
        operators.write(filename + ',' + operator + '\n')







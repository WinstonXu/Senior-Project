import os

for i in range(0, 10):
    open(str(i) + '_filenames.csv', 'w')

operators = ['+', '-', 'x', 'd']

for operator in operators:
    open(operator + '_filenames.csv', 'w')

mnist_dir = 'DatasetPictures/MnistPics'
operators_dir = 'DatasetPictures/Operators'

for filename in os.listdir(mnist_dir):
    if '.jpg' in filename:
        number = filename.split("-")[1][0]
        num_file = open(number + '_filenames.csv', 'a')
        num_file.write(filename + ',' + number + '\n')


for filename in os.listdir(operators_dir):
    if '.jpg' in filename:
        operator = filename.split(" ")[0]
        op_file = open(operator + '_filenames.csv', 'a')
        op_file.write(filename + ',' + operator + '\n')







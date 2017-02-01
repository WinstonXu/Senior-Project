import csv


def makeAllTestData():
    eq_test = open('eq_test.txt', 'w')
    with open('all_equations.csv', newline='') as all_equations:
        equations_reader = csv.reader(all_equations)
        for row in equations_reader:
            n1, op, n2 = row[1], row[3], row[5]
            nf1, of, nf2 = row[0], row[2], row[4]
            eq_test.write(n1 + op + n2 + '\n')
            eq_test.write(nf1 + '   ' + of + '   ' + nf2 + '\n')

    all_equations.close()

makeAllTestData()

# for i in range(0, 10):
#     open(str(i) + '_filenames.csv', 'w')
#
# operators = ['+', '-', 'x', 'd']
#
# for operator in operators:
#     open(operator + '_filenames.csv', 'w')
#
# mnist_dir = 'DatasetPictures/MnistPics'
# operators_dir = 'DatasetPictures/Operators'
#
# for filename in os.listdir(mnist_dir):
#     if '.jpg' in filename:
#         number = filename.split("-")[1][0]
#         num_file = open(number + '_filenames.csv', 'a')
#         num_file.write(filename + ',' + number + '\n')
#
#
# for filename in os.listdir(operators_dir):
#     if '.jpg' in filename:
#         operator = filename.split(" ")[0]
#         op_file = open(operator + '_filenames.csv', 'a')
#         op_file.write(filename + ',' + operator + '\n')
#
#





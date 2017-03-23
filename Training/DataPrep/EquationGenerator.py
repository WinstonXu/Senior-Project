import csv
import os
import json
import random
from random import randint

# directories of mnist and operator images
mnist_dir = 'DatasetPictures/mnist_imgs/alpha'
operators_dir = 'DatasetPictures/operator_imgs/alpha'

# json to hold mnist training info
mnist_json = 'mnist_json.txt'


# insert an mnist file into the train, test, or validate datasets
def insertAtTrainType(data_dict, key, _filename):
    if 'train' in _filename:
        data_dict[key]['train'].append(_filename)
    elif 'test' in _filename:
        data_dict[key]['test'].append(_filename)
    else:
        data_dict[key]['val'].append(_filename)

# counts how many of each digit in mnist dataset
mnist_count = {}
counter = 0
# iterates through mnist image directory & adds filenames to respective train, test, val set
for filename in os.listdir(mnist_dir):
    if '.png' in filename:
        counter += 1
        number = filename.split("-")[1][0]
        # if the num is already in dict, insert filename into train type list @ mnist_count[number][traintype]
        if number in mnist_count:
            insertAtTrainType(mnist_count, number, filename)
        # create train type dictionary then insert filename
        else:
            mnist_count[number] = {}
            mnist_count[number]['train'] = []
            mnist_count[number]['test'] = []
            mnist_count[number]['val'] = []

            insertAtTrainType(mnist_count, number, filename)

# print mnist dictionary
with open(mnist_json, 'w') as mnist_file:
    json.dump(mnist_count, mnist_file)

print('********FINAL**********')
# hold the counts of mnist images in each training set
total_count = 0
total_test_count = 0
total_train_count = 0
total_val_count = 0
mnist_train_dict = {}
mnist_test_dict = {}
mnist_val_dict = {}

for mnist_number, training_types in mnist_count.items():
    test_count = 0
    train_count = 0
    val_count = 0
    print('\nnumber: ' + mnist_number)
    for training_type, file_list in training_types.items():
        training_type_count = len(file_list)
        if training_type == 'test':
            mnist_test_dict[mnist_number] = file_list
            test_count = training_type_count
            total_test_count += training_type_count
        elif training_type == 'train':
            mnist_train_dict[mnist_number] = file_list
            train_count = training_type_count
            total_train_count += training_type_count
        else:
            mnist_val_dict[mnist_number] = file_list
            val_count = training_type_count
            total_val_count += training_type_count
        total_count += training_type_count
    print('train count: ' + str(train_count))
    print('test count: ' + str(test_count))
    print('val count: ' + str(val_count))

print('\nmnist total train count: ' + str(total_train_count))
print('mnist total test count: ' + str(total_test_count))
print('mnist total validation count: ' + str(total_val_count))

print('all mnist numbers count: ' + str(total_count))


# extracts the operator from filename
def parseOperatorFilename(_filename):
    file_parts = _filename.split('_')
    orig = file_parts[0].split('.')[0]
    _operator = orig.split('-')[0]
    return _operator, orig

# operator image file dict
operator_dict = {'+': [], 'm': [], 'x': [], 'd': []}
# operator counts
operator_count = {'+': 0, 'm': 0, 'x': 0, 'd': 0}
counter = 0
# add operator filenames to their respective list in dict
for filename in os.listdir(operators_dir):
    if '.png' in filename:
        operator, orig_name = parseOperatorFilename(filename)
        if counter % 200 == 0:
            print(operator)
        operator_dict[operator].append(filename)

        operator_count[operator] += 1
        counter += 1

print('operator count: ' + str(operator_count))
print('*************************************** counter: ' + str(counter) + ' *****************************************')


with open('operators_json.txt', 'w') as operator_file:
    json.dump(operator_dict, operator_file)

# randomize operators within respective lists
for operator, operator_files in operator_dict.items():
    # print('operator: ' + operator)
    operator_dict[operator] = random.sample(operator_files, len(operator_files))

# list to hold all of the different equation permutations
eq_perms = []
# create eq permutations
for i in range(0, 10):
    # first digit in eq
    first = str(i)
    for j in range(0, 10):
        # second digit in eq
        second = str(j)
        # add 4 eqs with (+, -, x, /)
        eq_perms.append((first, '+', second))
        eq_perms.append((first, 'm', second))
        eq_perms.append((first, 'x', second))
        eq_perms.append((first, 'd', second))


# create unique eq images for given training type
def makeTrainingTypeEqs(training_type_dict, op_dict, eq_list, eq_times, new_filename):
    # dict to hold train, test, and validate eqs
    train_type_eqs = {}
    # add the 400 eq permutations to a dict with a list at eq -> train_type_eqs[eqn] = []
    for eq in eq_perms:
        train_type_eqs[''.join(eq)] = []

    # 400 eqs
    eq_size = len(eq_list)
    '''
        if eq_times large enough, we will run through all mnist images
        before we finish making the requested number of each equation
        therefore, we index into the equation number mod the number of equations we need
    '''
    for eq_num in range(eq_size * eq_times):
        # parse eqn
        first_num, op, second_num = eq_perms[eq_num % eq_size]

        # grab first num file & put it at end of queue
        first_num_files = training_type_dict[first_num]
        first_file = first_num_files[0]
        first_num_files.remove(first_file)
        first_num_files.insert(randint(0, len(first_num_files)), first_file)

        # grab operator file & put it at end of queue
        op_list = op_dict[op]
        op_file = op_list[0]
        op_list.remove(op_file)
        op_list.append(op_file)

        # grab second num file & put it at end of queue
        second_list = training_type_dict[second_num]
        second_file = second_list[0]
        second_list.remove(second_file)
        second_list.insert(randint(0, len(second_list)), second_file)

        train_type_eqs[''.join((first_num, op, second_num))].append((first_file, op_file, second_file))

    for eqn, eqn_vars in train_type_eqs.items():
        print('eq: ' + eqn + ' count: ' + str(len(eqn_vars)))

    with open(new_filename, 'w') as eq_file:
        eq_file.write(json.dumps(train_type_eqs, indent=4, sort_keys=True))

# create the train, test, and validate equation datasets
makeTrainingTypeEqs(mnist_train_dict, operator_dict, eq_perms, 100, 'training_eqs.json')
makeTrainingTypeEqs(mnist_test_dict, operator_dict, eq_perms, 20, 'test_eqs.json')
makeTrainingTypeEqs(mnist_val_dict, operator_dict, eq_perms, 20, 'validate_eqs.json')

with open('test_eqs.json') as test_eqs_file:
    test_eqs = json.load(test_eqs_file)
    print('test_eqs type: ' + str(type(test_eqs)))
    # print(str(test_eqs))


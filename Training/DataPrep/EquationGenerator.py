import csv
import os
import json
import random
from random import randint


mnist_dir = 'DatasetPictures/mnist_imgs/alpha'
operators_dir = 'DatasetPictures/operator_imgs/alpha'


def insertAtTrainType(data_dict, key, _filename):
    if 'train' in _filename:
        data_dict[key]['train'].append(_filename)
    elif 'test' in _filename:
        data_dict[key]['test'].append(_filename)
    else:
        data_dict[key]['val'].append(_filename)

mnist_count = {}
counter = 0
for filename in os.listdir(mnist_dir):
    if '.png' in filename:
        counter += 1
        number = filename.split("-")[1][0]
        if number in mnist_count:
            insertAtTrainType(mnist_count, number, filename)
        else:
            mnist_count[number] = {}
            mnist_count[number]['train'] = []
            mnist_count[number]['test'] = []
            mnist_count[number]['val'] = []

            insertAtTrainType(mnist_count, number, filename)


with open('mnist_json.txt', 'w') as mnist_file:
    json.dump(mnist_count, mnist_file)

print('********FINAL**********')
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


def parseOperatorFilename(_filename):
    file_parts = _filename.split('_')
    orig = file_parts[0].split('.')[0]
    _operator = orig.split('-')[0]
    return _operator, orig


all_operators_dict = {'+': [], 'm': [], 'x': [], 'd': []}
operator_count = {'+': 0, 'm': 0, 'x': 0, 'd': 0}
counter = 0
for filename in os.listdir(operators_dir):
    if '.png' in filename:
        operator, orig_name = parseOperatorFilename(filename)
        if counter % 200 == 0:
            print(operator)
        all_operators_dict[operator].append(filename)

        operator_count[operator] += 1
        counter += 1

print('operator count: ' + str(operator_count))
print('*************************************** counter: ' + str(counter) + ' *****************************************')

with open('operators_json.txt', 'w') as operator_file:
    json.dump(all_operators_dict, operator_file)

# print('********FINAL**********')
# total_count = 0
# source_dict = {}
# training_dict = {'train': [], 'test': [], 'val': []}
# for op, sources in operator_dict.items():
#     # print('operator: ' + op)
#     for source, source_files in sources.items():
#         # print('source: ' + str(source))
#         source_dict[source] = {'train': [], 'test': [], 'val': []}
#         counter = 0
#         for og_file, og_file_versions in source_files.items():
#             if counter % 14 == 3 or counter % 14 == 8:
#                 source_dict[source]['val'].extend(og_file_versions)
#                 training_dict['val'].extend(og_file_versions)
#             elif counter % 14 == 4 or counter % 14 == 9:
#                 source_dict[source]['test'].extend(og_file_versions)
#                 training_dict['test'].extend(og_file_versions)
#             else:
#                 source_dict[source]['train'].extend(og_file_versions)
#                 training_dict['train'].extend(og_file_versions)
#             counter += 1
#             op_count = len(og_file_versions)
#             # print('\t\t\t\t\tog_file: ' + og_file + ' count: ' + str(op_count))
#             total_count += op_count
            # for file_version in og_file_versions:
            #     print('\t\t\t\t\t\t\t\t\t\t' + file_version)


# for source, training_types in source_dict.items():
#     print('source: ' + source)
#     for training_type, files in training_types.items():
#         print('\t\t\t\t training type: ' + training_type)
#         counter = 0
#         for file in files:
#             if counter % 300 == 0:
#                 print('\t\t\t\t\t\t\t\t' + file)
#             counter += 1

# training_count = {'train': 0, 'test': 0, 'val': 0}
# for training_type, op_files in training_dict.items():
#     print('\ntraining type: ' + training_type)
#     count = len(op_files)
#     training_count[training_type] = count
#     print('count: ' + str(count))
#     ratio = (float(count) / total_count) * 100
#     print('%: ' + str(ratio))
    # counter = 0
    # for file in op_files:
    #     if counter % 1000 == 0:
    #         print('\t\t\t' + file)
    #     counter += 1

# print('all operators count: ' + str(total_count))
#
# print('minus operator files:')
# print('sources: ' + str(operator_dict.keys()))
# for source, og_files in operator_dict['m'].items():
#     print('\t\t\t\t source: ' + source + ' count: ' + str(len(og_files)))
#     counter = 0
#     for og_file, variations in og_files.items():
#         if counter % 500 == 0:
#             print('\t\t\t\t\t\t\t\t' + og_file + ' count: ' + str(len(variations)))
#             for var in variations:
#                 print('\t\t\t\t\t\t\t\t\t\t\t\t' + var)
#         counter += 1
#
#
# print(str(operator_count))

# for operator in all_operators_dict:
#     print('operator: ' + operator)
#     counter = 0
#     for file in all_operators_dict[operator]:
#         if counter % 500 == 0:
#             print('\t\t\t' + file)
#         counter += 1

for operator, operator_files in all_operators_dict.items():
    # print('operator: ' + operator)
    all_operators_dict[operator] = random.sample(operator_files, len(operator_files))

# # print('type(all_operators_dict): ' + str(type(all_operators_dict)))
# for operator in all_operators_dict:
#     print('operator: ' + operator)
#     # print('type(all_operators_dict[operator]): ' + str(type(all_operators_dict[operator])))
#     counter = 0
#     for file in all_operators_dict[operator]:
#         if counter % 1000 == 0:
#             print('\t\t\t' + file)
#         counter += 1

# for mnist_int in train_dict:
#     print('number: ' + str(mnist_int))
#     counter = 0
#     for file in train_dict[mnist_int]:
#         if counter % 1000 == 0:
#             print('\t\t\t' + file)
#         counter += 1
#
# for mnist_int in test_dict:
#     print('number: ' + str(mnist_int))
#     counter = 0
#     for file in test_dict[mnist_int]:
#         if counter % 1000 == 0:
#             print('\t\t\t' + file)
#         counter += 1
#
# for mnist_int in val_dict:
#     print('number: ' + str(mnist_int))
#     counter = 0
#     for file in val_dict[mnist_int]:
#         if counter % 1000 == 0:
#             print('\t\t\t' + file)
#         counter += 1

eq_perms = []
for i in range(0, 10):
    first = str(i)
    for j in range(0, 10):
        eq_perms.append((first, '+', str(j)))
        eq_perms.append((first, 'm', str(j)))
        eq_perms.append((first, 'x', str(j)))
        eq_perms.append((first, 'd', str(j)))


def makeTrainingTypeEqs(training_type_dict, op_dict, eq_list, eq_times, new_filename):
    train_type_eqs = {}
    for eq in eq_perms:
        train_type_eqs[''.join(eq)] = []

    eq_size = len(eq_list)
    for eq in range(eq_size * eq_times):
        first_mnist, op, second_mnist = eq_perms[eq % eq_size]

        first_list = training_type_dict[first_mnist]
        first_file = first_list[0]
        first_list.remove(first_file)
        first_list.insert(randint(0, len(first_list)), first_file)

        op_list = op_dict[op]
        op_file = op_list[0]
        op_list.remove(op_file)
        op_list.append(op_file)

        second_list = training_type_dict[second_mnist]
        second_file = second_list[0]
        second_list.remove(second_file)
        second_list.insert(randint(0, len(second_list)), second_file)

        train_type_eqs[''.join((first_mnist, op, second_mnist))].append((first_file, op_file, second_file))
        # train_type_eqs[''.join((second_mnist, op, first_mnist))].append((second_file, op_file, first_file))

    for eqn, eqn_vars in train_type_eqs.items():
        print('eq: ' + eqn + ' count: ' + str(len(eqn_vars)))

    with open(new_filename, 'w') as eq_file:
        eq_file.write(json.dumps(train_type_eqs, indent=4, sort_keys=True))


makeTrainingTypeEqs(mnist_train_dict, all_operators_dict, eq_perms, 100, 'training_eqs.json')
makeTrainingTypeEqs(mnist_test_dict, all_operators_dict, eq_perms, 20, 'test_eqs.json')
makeTrainingTypeEqs(mnist_val_dict, all_operators_dict, eq_perms, 20, 'validate_eqs.json')

with open('test_eqs.json') as test_eqs_file:
    test_eqs = json.load(test_eqs_file)
    print('test_eqs type: ' + str(type(test_eqs)))
    # print(str(test_eqs))


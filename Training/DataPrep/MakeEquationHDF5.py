import os
from PIL import Image
from PIL import ImageOps
import numpy as np
import h5py
from os.path import dirname, join
import json
from random import randint


_default_name = join(dirname(__file__), "mnist.h5")
parent_dir = os.path.join(os.path.dirname(__file__), 'DatasetPictures')
mnist_dir = os.path.join(parent_dir, 'mnist_imgs/alpha')
op_dir = os.path.join(parent_dir, 'operator_imgs/alpha')

'''
    Creates sparse vector of the single digit operations
    first 10 indices are for first number
    next 4 are for the operations-say addition, subtraction, mult, division
    next 10 are the second number
'''
def resultVector(num1, num2, operator):
    result = np.zeros((24))
    result[num1] = 1
    result[len(result)-(10-num2)] = 1
    if operator == "+":
        result[10] = 1
    if operator == "m":
        result[11] = 1
    if operator == "x":
        result[12] = 1
    if operator == "d":
        result[13] = 1
    return result


def makeHDF5(image, label):
    pixelData = image.getdata()
    pixelData = np.asarray(pixelData, dtype=np.float64).reshape((image.size[1], image.size[0]))
    return pixelData, label


def makeDataset():
    print(os.getcwd())

    equation_images = []
    equation_labels = []

    makeTestData(equation_images, equation_labels)

    equation_images = np.asarray(equation_images)
    equation_labels = np.asarray(equation_labels)
    equation_labels = np.reshape(equation_labels, (len(equation_labels), 24))
    print(equation_images.shape, equation_labels.shape)

    os.chdir(os.path.join(os.path.dirname(__file__), os.pardir))
    f = h5py.File("Dataset.hdf5", "w")
    f.create_dataset('img', data=equation_images)
    f.create_dataset('label', data=equation_labels)


# Stitches two digit and one operand picture together, creates dataset and labels for those images
def makeTestData(equation_images, equation_labels):

    with open('training_eqs.json') as training_eqs_file:
        training_eqs = json.load(training_eqs_file)
        makeTestImages(training_eqs, equation_images, equation_labels)

    with open('test_eqs.json') as test_eqs_file:
        test_eqs = json.load(test_eqs_file)
        makeTestImages(test_eqs, equation_images, equation_labels)

    with open('validate_eqs.json') as validate_eqs_file:
        validate_eqs = json.load(validate_eqs_file)
        makeTestImages(validate_eqs, equation_images, equation_labels)


def makeTestImages(eq_dict, equation_images, equation_labels):
    pic_size = 28
    count = 0
    for eq, unq_eqs in eq_dict.items():
        num1, op, num2 = eq
        for unq_eq in unq_eqs:
            num1_file = unq_eq[0]
            op_file = unq_eq[1]
            num2_file = unq_eq[2]

            num1_img = Image.open(os.path.join(mnist_dir, num1_file))
            op_img = Image.open(os.path.join(op_dir, op_file))
            num2_img = Image.open(os.path.join(mnist_dir, num2_file))

            final_image = ImageOps.invert(Image.new('L', (3 * pic_size, pic_size)))
            r_flux = randint(0, 10)
            final_image.paste(num1_img, box=(5, r_flux))
            # final_image.show()
            if op == 'm':
                r_flux = randint(-5, 2)
                final_image.paste(op_img, box=(pic_size, (int(pic_size/2)) + r_flux))
            else:
                r_flux = randint(0, 5)
                final_image.paste(op_img, box=(pic_size, r_flux))
            # final_image.show()
            r_flux = randint(0, 10)
            final_image.paste(num2_img, box=(2 * pic_size, r_flux))
            # final_image.show()

            pic, label = makeHDF5(final_image, resultVector(int(num1), int(num2), op))
            equation_images.append(pic)
            equation_labels.append(label)

            count += 1
            if count % 5000 == 0:
                    print(label)
                    final_image.show()

if __name__ == "__main__":
    makeDataset()

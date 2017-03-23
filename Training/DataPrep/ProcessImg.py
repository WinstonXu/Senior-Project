import os
from PIL import Image
from PIL import ImageOps
from PIL import ImageEnhance
import PIL.ImageOps
import h5py
import sys
import numpy as np
import h5py
import _pickle as cPickle
import gzip
from os.path import dirname, join
import random
import csv
import json
from random import randint


_default_name = join(dirname(__file__), "mnist.h5")
parent_dir = os.path.join(os.path.dirname(__file__), 'DatasetPictures')
mnist_dir = os.path.join(parent_dir, 'mnist_imgs/alpha')
op_dir = os.path.join(parent_dir, 'operator_imgs/alpha')

# mnist_dir = os.path.join(parent_dir, 'mnist_imgs')
# op_dir = os.path.join(parent_dir, 'operator_imgs')

def get_store(fname=_default_name):
    print("Loading from store {}".format(fname))
    return h5py.File(fname, 'r')


def build_store(store=_default_name, mnist="mnist.pkl.gz"):
    """Build a hdf5 data store for MNIST.
    """
    # os.chdir("/Users/Winston/PycharmProjects/ImgProcessing")
    print("Reading {}").format(mnist)
    mnist_f = gzip.open(mnist,'rb')
    train_set, valid_set, test_set = cPickle.load(mnist_f)
    mnist_f.close()

    print("Writing to {}").format(store)
    h5file = h5py.File(store, "w")

    print("Creating train set.")
    grp = h5file.create_group("train")
    dset = grp.create_dataset("inputs", data = train_set[0])
    dset = grp.create_dataset("targets", data = train_set[1])

    print("Creating validation set.")
    grp = h5file.create_group("validation")
    dset = grp.create_dataset("inputs", data = valid_set[0])
    dset = grp.create_dataset("targets", data = valid_set[1])

    print("Creating test set.")
    grp = h5file.create_group("test")
    dset = grp.create_dataset("inputs", data = test_set[0])
    dset = grp.create_dataset("targets", data = test_set[1])

    print("Closing {}").format(store)
    h5file.close()


def makeHDF5(image, label):
    pixelData = image.getdata()
    pixelData = np.asarray(pixelData, dtype=np.float64).reshape((image.size[1], image.size[0]))
    return pixelData, label


# Needs to be changed
def loadData(filename):
    # os.chdir("/Users/Winston/PycharmProjects/ImgProcessing")
    f = h5py.File(filename, 'r')
    x = f['img']
    y = f['label']
    print (x.shape, y.shape)
    return x, y


# Create jpg files from hdf5 file
def getMNIST():
    f = h5py.File("mnist.h5", 'r')
    if not os.path.exists("MnistPics"):
        os.makedirs("MnistPics")
    os.chdir("MnistPics")
    for key in f.keys():
        imgs = np.reshape(f[key]['inputs'], (f[key]['inputs'].shape[0], 28, 28))
        imgs = imgs*255
        imgs = imgs.astype('uint8')
        print (len(imgs))
        # print imgs[0]
        # pic = Image.fromarray(imgs[1], 'L')
        # pic.show()
        for i in range(len(imgs)):
            pic = Image.fromarray(imgs[i],'L')
            name = key+"-"+str(f[key]['targets'][i])
            if os.path.isfile(name+".jpg"):
                i = 0
                temp = name
                while os.path.isfile(temp+".jpg"):
                    temp = name+str(i)
                    i+=1
                pic.save(temp+".jpg")
            else:
                pic.save(name+".jpg")

'''
no repeats && every combo && every image
'''


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


# Rotates pictures somewhere between 10 degrees clock and counterclockwise
def makeSlantData(samplesize, picarr, labelarr, numlist, oplist, img_file_count):
    picsize = 28
    for i in range(samplesize):
        num1_filename = random.choice(numlist)
        num2_filename = random.choice(numlist)
        rotations = range(-10,10)
        operator_filename = random.choice(oplist)
        if num1_filename in img_file_count:
            img_file_count[num1_filename] += 1
        else:
            img_file_count[num1_filename] = 1

        if num2_filename in img_file_count:
            img_file_count[num2_filename] += 1
        else:
            img_file_count[num2_filename] = 1

        if operator_filename in img_file_count:
            img_file_count[operator_filename] += 1
        else:
            img_file_count[operator_filename] = 1
        target1 = int(num1_filename.split("-")[1][0])
        target2 = int(num2_filename.split("-")[1][0])
        target3 = operator_filename.split(" ")[0]
        part1 = Image.open(os.path.join(parent_dir, 'MnistPics', num1_filename)).rotate(random.choice(rotations))
        part2 = Image.open(os.path.join(parent_dir, 'MnistPics', num2_filename)).rotate(random.choice(rotations))
        part3 = Image.open(os.path.join(parent_dir, 'Operators', operator_filename)).rotate(random.choice(rotations))
        finalIm = Image.new('L', (3*picsize, picsize))
        finalIm.paste(part1, box=(0,0))
        finalIm.paste(part3,box=(picsize,0))
        finalIm.paste(part2, box=(2*picsize,0))
        pic,label = makeHDF5(finalIm, resultVector(target1,target2,target3))
        picarr.append(pic)
        labelarr.append(label)
        # if i%10000 == 0:
        #   print (label)
        #   # finalIm.show()


# Enlarges picture and then crops out middle 28x28
def makeZoomData(samplesize, picarr, labelarr, numlist, oplist, img_file_count):
    picsize = 28
    for i in range(samplesize):
        num1file = random.choice(numlist)
        num2file = random.choice(numlist)
        opfile = random.choice(oplist)
        target1 = int(num1file.split("-")[1][0])
        target2 = int(num2file.split("-")[1][0])
        target3 = opfile.split(" ")[0]
        part1 = Image.open(os.path.join(parent_dir, 'MnistPics', num1file)).resize((35, 35)).crop((1, 1, 29, 29))
        part2 = Image.open(os.path.join(parent_dir, 'MnistPics', num2file)).resize((35, 35)).crop((1, 1, 29, 29))
        part3 = Image.open(os.path.join(parent_dir, 'Operators', opfile)).resize((35, 35)).crop((1, 1, 29, 29))
        finalIm = Image.new('L', (3 * picsize, picsize))
        finalIm.paste(part1, box=(0, 0))
        finalIm.paste(part3, box=(picsize, 0))
        finalIm.paste(part2, box=(2 * picsize, 0))
        pic, label = makeHDF5(finalIm, resultVector(target1, target2, target3))
        picarr.append(pic)
        labelarr.append(label)
        # if i % 10000 == 0:
        #     print (label)
        #     # finalIm.show()


#Shifts Picture in a direction, resize to 28x28
def makeTranslateData(samplesize, picarr, labelarr, numlist, oplist, img_file_count):
    picsize = 28
    for i in range(samplesize):
        num1file = random.choice(numlist)
        num2file = random.choice(numlist)
        opfile = random.choice(oplist)
        target1 = int(num1file.split("-")[1][0])
        target2 = int(num2file.split("-")[1][0])
        target3 = opfile.split(" ")[0]
        part1 = translate(Image.open(os.path.join(parent_dir, 'MnistPics', num1file))).resize((28, 28))
        part2 = translate(Image.open(os.path.join(parent_dir, 'MnistPics', num2file))).resize((28, 28))
        part3 = translate(Image.open(os.path.join(parent_dir, 'Operators', opfile))).resize((28, 28))
        finalIm = Image.new('L', (3 * picsize, picsize))
        finalIm.paste(part1, box=(0, 0))
        finalIm.paste(part3, box=(picsize, 0))
        finalIm.paste(part2, box=(2 * picsize, 0))
        pic, label = makeHDF5(finalIm, resultVector(target1, target2, target3))
        picarr.append(pic)
        labelarr.append(label)
        # if i % 10000 == 0:
        #     print (label)
        #     # finalIm.show()


def translate(image):
    direction = random.choice([1,2,3,4])
    if direction == 1:
        result = image.crop((5,0,28,28))
    elif direction == 2:
        result = image.crop((0,5,28,28))
    elif direction == 3:
        result = image.crop((0,0,23,28))
    else:
        result = image.crop((0,0,28,23))
    return result


#Creates sparse vector of the single digit operations
#first 10 indices are for first number
#next 4 are for the operations-say addition, subtraction, mult, division
#next 10 are the second number
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


def InvertOps():
    allpics = [j for j in os.listdir(os.path.join(parent_dir, 'Operators')) if ".jpg" in j]
    for pic in allpics:
        image = Image.open(pic)
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save(pic)

#need to figure out where test photos will be...may be out of this directory
def realLifeTest():
    os.chdir("Senior-Project/TestPhotos")
    allpics = [j for j in os.listdir(os.getcwd()) if "copy.jpg" in j]
    samplesize = len(allpics)
    picsize = 28
    pictures = np.zeros((samplesize, picsize,3*picsize))
    labels = np.zeros((samplesize, 1,24))
    for i in range(samplesize):
        #make values more extreme
        image = Image.open(allpics[i], 'r')
        # image = image.resize((84,28))
        # image = image.convert('L')
        # newim = ImageEnhance.Contrast(image)
        # newim = newim.enhance(2.5).save(allpics[i][:-4]+"copy.jpg")
        pixelData = image.getdata()
        pixelData = np.asarray(pixelData, dtype=np.float64).reshape((image.size[1], image.size[0]))
        pictures[i] =pixelData
        title = allpics[i].split("_")
        res = resultVector(int(title[0][0]), int(title[0][2]), title[0][1])
        print (title[0])
        print (res)
        labels[i] =res
    os.chdir("Senior-Project")
    f = h5py.File("Dataset.hdf5", "a")
    labels = np.reshape(labels, (len(labels),24))
    f.create_dataset('real-img', data=pictures)
    f.create_dataset('real-label', data=labels)



if __name__ == "__main__":
    # build_store()
    # getMNIST()
    # InvertOps()
    # loadData("Dataset.hdf5")
    #realLifeTest()
    makeDataset()

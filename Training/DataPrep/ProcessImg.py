import os
from PIL import Image
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


_default_name = join(dirname(__file__), "mnist.h5")
parent_dir = os.path.join(os.path.dirname(__file__), 'DatasetPictures')


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

# def makeHDF5(folder, filename, label):
#     # os.chdir("/Users/Winston/PycharmProjects/ImgProcessing")
#     f = h5py.File(filename, "w")
#     minsize = 28
#     os.chdir(folder)
#     files = os.listdir(os.getcwd())
#     pixels = np.zeros((len(files), minsize, minsize))
#     #search only for images
#     for i in range(len(files)):
#         if ".jpg" in files[i]:
#             im = Image.open(files[i], 'r')
#             im = im.resize((minsize,minsize))
#             im = im.convert('L')
#             # im.show()
#             pixelData = im.getdata()
#             pixelData = np.asarray(pixelData, dtype=np.float64).reshape((im.size[1], im.size[0]))
#             pixels[i] = pixelData
#     pic = f.create_dataset('img', data=pixels)
#     pic.attrs["LABEL"] = label
#


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


def makeDataset(samplesize):
    print(os.getcwd())

    img_file_count = {}

    equation_images = []
    equation_labels = []

    mnist_dir = os.path.join(parent_dir, 'MnistPics')
    mnist_pics = [j for j in os.listdir(mnist_dir) if ".jpg" in j]
    operators_dir = os.path.join(parent_dir, 'Operators')
    operator_pics = [j for j in os.listdir(operators_dir) if ".jpg" in j]

    makeTestData(samplesize, equation_images, equation_labels, mnist_pics, operator_pics, img_file_count)
    makeSlantData(samplesize, equation_images, equation_labels, mnist_pics, operator_pics, img_file_count)
    makeZoomData(samplesize, equation_images, equation_labels, mnist_pics, operator_pics, img_file_count)
    makeTranslateData(samplesize, equation_images, equation_labels, mnist_pics, operator_pics, img_file_count)

    makeAllTestData(28, equation_images, equation_labels, img_file_count)

    equation_images = np.asarray(equation_images)
    equation_labels = np.asarray(equation_labels)
    equation_labels = np.reshape(equation_labels, (len(equation_labels), 24))
    print(equation_images.shape, equation_labels.shape)

    os.chdir(os.path.join(os.path.dirname(__file__), os.pardir))
    f = h5py.File("Dataset.hdf5", "w")
    f.create_dataset('img', data=equation_images)
    f.create_dataset('label', data=equation_labels)


def makeAllTestData(pic_size, equation_images, equation_labels, img_file_count):
    count = 0
    with open('all_equations.csv', newline='') as all_equations:
        equations_reader = csv.reader(all_equations)
        for row in equations_reader:
            count += 1
            num1, operator, num2 = row[1], row[3], row[5]
            num1_filename, operator_filename, num2_filename = row[0], row[2], row[4]

            if num1_filename in img_file_count:
                img_file_count[num1_filename] += 2
            else:
                img_file_count[num1_filename] = 2

            if num2_filename in img_file_count:
                img_file_count[num2_filename] += 2
            else:
                img_file_count[num2_filename] = 2

            if operator_filename in img_file_count:
                img_file_count[operator_filename] += 2
            else:
                img_file_count[operator_filename] = 2

            print('num1: ' + num1 + ' operator: ' + operator + ' num2: ' + num2)
            print('num1_filename: ' + num1_filename + '\noperator_filename: ' + operator_filename
                  + '\nnum2_filename: ' + num2_filename)

            num1_image = Image.open(os.path.join(parent_dir, 'MnistPics', num1_filename))
            num2_image = Image.open(os.path.join(parent_dir, 'MnistPics', num2_filename))
            operator_image = Image.open(os.path.join(parent_dir, 'Operators', operator_filename))
            makeEquationImage(num1_image, num2_image, operator_image,
                              num1, num2, operator, equation_images, equation_labels, pic_size)


            # if count % 4 == 1:
            rotations = range(-10, 10)
            makeEquationImage(num1_image.rotate(random.choice(rotations)),
                              num2_image.rotate(random.choice(rotations)),
                              operator_image.rotate(random.choice(rotations)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(num1_image.rotate(random.choice(rotations)).resize((35, 35)).crop((1, 1, 29, 29)),
                              num2_image.rotate(random.choice(rotations)).resize((35, 35)).crop((1, 1, 29, 29)),
                              operator_image.rotate(random.choice(rotations)).resize((35, 35)).crop((1, 1, 29, 29)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(translate(num1_image.rotate(random.choice(rotations))).resize((28, 28)),
                              translate(num2_image.rotate(random.choice(rotations))).resize((28, 28)),
                              translate(operator_image.rotate(random.choice(rotations))).resize((28, 28)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(translate(num1_image.rotate(random.choice(rotations)).resize((35, 35))
                                        .crop((1, 1, 29, 29))).resize((28, 28)),
                              translate(num2_image.rotate(random.choice(rotations)).resize((35, 35))
                                        .crop((1, 1, 29, 29))).resize((28, 28)),
                              translate(operator_image.rotate(random.choice(rotations)).resize((35, 35))
                                        .crop((1, 1, 29, 29))).resize((28, 28)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(num1_image.resize((35, 35)).crop((1, 1, 29, 29)),
                              num2_image.resize((35, 35)).crop((1, 1, 29, 29)),
                              operator_image.resize((35, 35)).crop((1, 1, 29, 29)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(num1_image.resize((35, 35)).crop((1, 1, 29, 29)).rotate(random.choice(rotations)),
                              num2_image.resize((35, 35)).crop((1, 1, 29, 29)).rotate(random.choice(rotations)),
                              operator_image.resize((35, 35)).crop((1, 1, 29, 29)).rotate(random.choice(rotations)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(translate(num1_image.resize((35, 35)).crop((1, 1, 29, 29))).resize((28, 28)),
                              translate(num2_image.resize((35, 35)).crop((1, 1, 29, 29))).resize((28, 28)),
                              translate(operator_image.resize((35, 35)).crop((1, 1, 29, 29))).resize((28, 28)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(translate(num1_image.resize((35, 35)).crop((1, 1, 29, 29))).resize((28, 28))
                              .rotate(random.choice(rotations)),
                              translate(num2_image.resize((35, 35)).crop((1, 1, 29, 29))).resize((28, 28))
                              .rotate(random.choice(rotations)),
                              translate(operator_image.resize((35, 35)).crop((1, 1, 29, 29))).resize((28, 28))
                              .rotate(random.choice(rotations)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(translate(num1_image).resize((28, 28)).rotate(random.choice(rotations)),
                              translate(num2_image).resize((28, 28)).rotate(random.choice(rotations)),
                              translate(operator_image).resize((28, 28)).rotate(random.choice(rotations)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(translate(num1_image).resize((28, 28)).rotate(random.choice(rotations)),
                              translate(num2_image).resize((28, 28)).rotate(random.choice(rotations)),
                              translate(operator_image).resize((28, 28)).rotate(random.choice(rotations)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(translate(num1_image).resize((28, 28)).resize((35, 35)).crop((1, 1, 29, 29)),
                              translate(num2_image).resize((28, 28)).resize((35, 35)).crop((1, 1, 29, 29)),
                              translate(operator_image).resize((28, 28)).resize((35, 35)).crop((1, 1, 29, 29)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(translate(num1_image).resize((28, 28)),
                              translate(num2_image).resize((28, 28)),
                              translate(operator_image).resize((28, 28)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(num1_image.rotate(random.choice(rotations)).resize((35, 35)).crop((1, 1, 29, 29)),
                              num2_image.rotate(random.choice(rotations)).resize((35, 35)).crop((1, 1, 29, 29)),
                              operator_image.rotate(random.choice(rotations)).resize((35, 35)).crop((1, 1, 29, 29)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(num1_image.resize((35, 35)).crop((1, 1, 29, 29)),
                              num2_image.resize((35, 35)).crop((1, 1, 29, 29)),
                              operator_image.resize((35, 35)).crop((1, 1, 29, 29)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            makeEquationImage(translate(num1_image).resize((28, 28)),
                              translate(num2_image).resize((28, 28)),
                              translate(operator_image).resize((28, 28)),
                              num1, num2, operator, equation_images, equation_labels, pic_size)

            final_image = makeEquationImage(num1_image, num2_image, operator_image,
                                            num1, num2, operator, equation_images, equation_labels, pic_size)

            if count % 1000 == 0:
                # print('num1: ' + num1 + ' operator: ' + operator + ' num2: ' + num2)
                # print('num1_filename: ' + num1_filename + '\noperator_filename: ' + operator_filename
                #       + '\nnum2_filename: ' + num2_filename)
                # print(label)
                final_image.show()
                print(count)
                # final_image_2.show()

    all_equations.close()


def makeEquationImage(num1_image, num2_image, operator_image, num1, num2, operator,
                      equation_images, equation_labels,pic_size):
    final_image = Image.new('L', (3 * pic_size, pic_size))
    final_image.paste(num1_image, box=(0, 0))
    final_image.paste(operator_image, box=(pic_size, 0))
    final_image.paste(num2_image, box=(2 * pic_size, 0))
    pic, label = makeHDF5(final_image, resultVector(int(num1), int(num2), operator))
    equation_images.append(pic)
    equation_labels.append(label)
    return final_image


# Stitches two digit and one operand picture together, creates dataset and labels for those images
def makeTestData(sample_size, equation_images, equation_labels, mnist_pics, operator_pics, img_file_count):
    pic_size = 28

    for i in range(sample_size):
        num1_filename = random.choice(mnist_pics)
        num2_filename = random.choice(mnist_pics)
        operator_filename = random.choice(operator_pics)

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

        num1_target = int(num1_filename.split("-")[1][0])
        num2_target = int(num2_filename.split("-")[1][0])
        operator_target = operator_filename.split(" ")[0]

        num1_image = Image.open(os.path.join(parent_dir, 'MnistPics', num1_filename))
        num2_image = Image.open(os.path.join(parent_dir, 'MnistPics', num2_filename))
        operator_image = Image.open(os.path.join(parent_dir, 'Operators', operator_filename))

        # L --> (8-bit pixels, black and white)
        final_image = Image.new('L', (3*pic_size, pic_size))
        final_image.paste(num1_image, box=(0,0))
        final_image.paste(operator_image,box=(pic_size,0))
        final_image.paste(num2_image, box=(2*pic_size,0))

        pic, label = makeHDF5(final_image, resultVector(num1_target, num2_target, operator_target))
        equation_images.append(pic)
        equation_labels.append(label)
        # if i % 1000 == 0:
            # print (label)
            # final_image.show()


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
    if operator == "-":
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
    makeDataset(250000)

import os
import math
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

import utils

def gaussian_pyramid(input_image, level):
    """
    Args:
        input_image (numpy array): input array
        level (int): level of pyramid

    Return:
        Gaussian pyramid (list of numpy array)
    """

    # Your code
    # Note that elements in the list must be arranged in descending order in image resolution (from big image to small image).
    gp = [input_image] # Create a Gaussian pyramid for the input image
    
    for i in range(level):
        input_image = utils.down_sampling(input_image) # Down-sample the images
        gp.append(input_image) # Append them to the list

    # First image has the highest resolution while the last image hast the lowest resolution as it is the most down-sampled image
    return gp


def laplacian_pyramid(gaussian_pyramid):
    """
    Args:
        gaussian_pyramid (list of numpy array): result from the gaussian_pyramid function

    Return:
        laplacian pyramid (list of numpy array)
    """

    # Your code
    # Note that elements in the list must be arranged in descending order in image resolution (from big image to small image).
    lp = []

    # Build the Laplacian pyramid from the Gaussian pyramid
    for i in range(len(gaussian_pyramid) - 1):
        upsampled_image = utils.up_sampling(gaussian_pyramid[i + 1]) # Up-sampled the next level of the Gaussian pyramid
        lp.append(utils.safe_subtract(gaussian_pyramid[i], upsampled_image)) # Subtract the up-sampled next level from the current level

    # Append the smallest Gaussian image at the end of the Laplacian pyramid
    lp.append(gaussian_pyramid[-1])

    # Messi gets clearer, but it does not mean that image resolution is increasing
    # The first image in the Laplacian pyramid (highest resolution) will have the most high-frequency details (edges, texture, etc.) of Messi
    # The last image in the Laplacian pyramid will be more blurry and represent the larger structures or base tones of the image
    # The actual resolution of the images is still decreasing as you move down the pyramid

    return lp

def blend_images(image1, image2, mask, level):
    """
    Args:
        image1 (numpy array): background image
        image2 (numpy array): object image
        mask (numpy array): mask
        level (int): level of pyramid
    Return:
        blended image (numpy array)
    """
    # Your code
    gp1 = gaussian_pyramid(image1, level) # Gaussian pyramid for image 1
    gp2 = gaussian_pyramid(image2, level) # Gaussian pyramid for image 2
    gpm = gaussian_pyramid(mask, level) # Gaussian pyramid for the mask

    lp1 = laplacian_pyramid(gp1) # Laplacian pyramid for image 1
    lp2 = laplacian_pyramid(gp2) # # Laplacian pyramid for image 2

    bp = []

    for l1, l2, m in zip(lp1, lp2, gpm):
        # Mask is close to 1 => Blended image takes more from image2
        # Mask is close to 0 => Blended image takes more from image1
        bp_image = utils.safe_add(l2 * (m / 255.0), l1 * (1 - m / 255.0))
        bp.append(bp_image)

    blended_image = bp[-1] # Initialize blended image with the smallest image from the blended pyramid

    for i in range(level - 1, -1, -1): # Iterating through the levels in reverse order
        blended_image = utils.safe_add(utils.up_sampling(blended_image), bp[i]) # Constructing the blended image by adding up-sampled and blended images

    return blended_image


if __name__ == '__main__':
    messi = np.asarray(Image.open(os.path.join('images', 'messi.jpg')).convert('RGB'))
    ronaldo = np.asarray(Image.open(os.path.join('images', 'ronaldo.jpg')).convert('RGB'))
    mask = np.asarray(Image.open(os.path.join('images', 'mask.jpg')).convert('RGB'))

    logdir = os.path.join('results', 'HW1_1')
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    level = 3

    ret = gaussian_pyramid(messi, level)
    if ret is not None:
        plt.figure()
        for i in range(len(ret)):
            plt.subplot(1, len(ret), i + 1)
            plt.imshow(ret[i].astype(np.uint8))
            plt.axis('off')
        plt.savefig(os.path.join(logdir, 'gaussian_pyramid.jpg'))
        plt.show()

        ret = laplacian_pyramid(ret)
        if ret is not None:
            plt.figure()
            for i in range(len(ret)):
                plt.subplot(1, len(ret), i + 1)
                plt.imshow(ret[i].astype(np.uint8))
                plt.axis('off')
            plt.savefig(os.path.join(logdir, 'laplacian_pyramid.jpg'))
            plt.show()

    ret = blend_images(messi, ronaldo, mask, level)
    if ret is not None:
        plt.figure()
        plt.imshow(ret.astype(np.uint8))
        plt.axis('off')
        plt.savefig(os.path.join(logdir, 'blended.jpg'))
        plt.show()
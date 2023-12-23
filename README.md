# VisionBlendPyramids

## Project Overview
VisionBlendPyramids is an advanced Python project leveraging Gaussian and Laplacian pyramid techniques for image blending. This project seamlessly merges two images at multiple resolution levels, ensuring texture and detail preservation, with precise control offered by a blending mask.

## Features
- **Gaussian Pyramid Generation**: Constructs a series of progressively lower resolution versions of an image.
- **Laplacian Pyramid Construction**: Creates a pyramid that highlights the image's details at various scales.
- **Image Blending**: Merges two images based on a given mask, maintaining high-frequency details.

## Input Images
The blending process uses the following input images:

- **Background Image:** Lionel Messi in action on the football field.
- **Object Image:** Cristiano Ronaldo in his football attire.
- **Mask Image:** A gradient mask used to control the blending of the two images.

## Results
The project successfully blends two iconic football players, Messi and Ronaldo, into a single image. The Gaussian pyramid represents the images at decreasing resolutions, while the Laplacian pyramid captures the details necessary for blending. The final result is a composite image that naturally combines elements from both source images.

![Gaussian Pyramid](/results/vision_blend_pyramids/gaussian_pyramid.jpg)
*Figure 1: Gaussian Pyramid of Messi*

![Laplacian Pyramid](/results/vision_blend_pyramids/laplacian_pyramid.jpg)
*Figure 2: Laplacian Pyramid of Messi*

![Blended Image](/results/vision_blend_pyramids/blended.jpg)
*Figure 3: Blended Image of Messi and Ronaldo*

## Utilities (`utils.py`)
The utils.py module provides essential utility functions that are used throughout the image blending process:

- `safe_subtract``: Safely subtracts one image from another.
- `safe_add``: Safely adds two images together.
- `down_sampling``: Reduces the resolution of an image.
- `up_sampling``: Increases the resolution of an image.  

These functions ensure that image transformations are performed without data overflow or underflow, maintaining the integrity of pixel values.

## Getting Started
To use VisionBlendPyramids, ensure you have Python installed along with the following dependencies:
- NumPy
- PIL (Python Imaging Library)
- Matplotlib

Clone this repository to your local machine to get started:
```bash
git clone https://github.com/megamiii/VisionBlendPyramids.git
```

## Usage
1. **Prepare Images**: Place your background image, object image, and mask image in the 'images' directory.
2. **Set Parameters**: Define the number of levels for the pyramids.
3. **Run the Script**: Execute the main script to see the results of Gaussian and Laplacian pyramids, and the final blended image.

Example:
```python
from VisionBlendPyramids import blend_images
import numpy as np
from PIL import Image

# Load images
background = np.asarray(Image.open('path/to/background.jpg').convert('RGB'))
object = np.asarray(Image.open('path/to/object.jpg').convert('RGB'))
mask = np.asarray(Image.open('path/to/mask.jpg').convert('RGB'))

# Blending
blended_image = blend_images(background, object, mask, level=3)
```


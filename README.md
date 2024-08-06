# Image Transformer

## Overview

The Image Transformer is a Python script that performs random image sampling using the PIL library. It allows users to load an image, specify a sample size and the number of samples, and generate random non-overlapping samples from the image.

## Features

- Load an image from a specified path.
- Specify the width and height of the sample size.
- Define the number of random samples to generate.
- Ensure samples do not overlap.
- Display or save the generated samples.

## Requirements

- Python 3.x
- PIL (Pillow)
- numpy
- pandas

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/eugeniavuong/image-transformer.git
    cd image-transformer
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the Image Transformer, follow these steps:

1. Add the path to your image in the `main()` function.
2. Specify the sample size (width and height) and the number of samples.
3. Run the script:

    ```bash
    python image_transformer.py
    ```

### Example

```python
def main():
    transformer = ImageTransformer("images/cat.jpeg")
    sample_size = (100, 50)  # width, height
    num_samples = 3
    
    try:
        samples = transformer.get_randomised_sample(sample_size, num_samples)
        for i, sample in enumerate(samples):
            sample.show()  # or save file using sample.save(f"sample_{i}.jpg")
    except ValueError as e:
        print(e)
    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    main()

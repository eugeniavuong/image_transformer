from PIL import Image
import numpy as np 
import pandas as pd

class ImageTransformer: 
    '''
    A class to perform random image sampling 
    '''

    '''
    Load the image taken from the image_path parameter and record the size of the image 
    Parameters:
    image_path (str): The path to the image file to be loaded.
    '''
    def __init__(self, image_path: str):
        # Open the image using PIL and store its dimentions 
        try:
            self.image = Image.open(image_path)
            self.width, self.height = self.image.size
        except Exception as e:
            raise ValueError(f"Invalid image path: {e}")
    

    '''
    Param checker and error handling
    ''' 
    def param_check(self, sample_size: tuple, num_samples:int):
        # Check whether width and height of sample is correctly defined
        if not(isinstance(sample_size, tuple) and len(sample_size)==2): 
            raise ValueError("Sample size must be of width and height.")
        sample_width, sample_height = sample_size 
        # Check is sample width and height are positive integers
        if sample_width < 0 or sample_height < 0:
            raise ValueError("Sample size must be positive integers.")
        # Check if sample size is less than the width and height of the image
        if sample_width > self.width or sample_height > self.height:
            raise ValueError("Sample size exceeds image dimensions.")
        # Check the sample number is a positive integer
        if num_samples <= 0: 
            raise ValueError("Number of samples must be a positive integer.")
   

    '''
    Get random sample
    '''
    # randomised points for sampling 
    def get_randomised_sample(self, sample_size:int, num_samples:int) -> list:
        self.param_check(sample_size, num_samples)

        # Generate a list of all possible top left corners positions (x,y) where the sample can fit within the image dimensions. 
        # Using a pandas df to store these positions for efficient manipulation 
        x_coords = range(0,self.width - sample_size[0] + 1)
        y_coords = range(0, self.height - sample_size[1] + 1)
        possible_positions = pd.DataFrame(data=[(x,y) for x in x_coords for y in y_coords], columns= ['x', 'y'])
        # Shuffle df of all possible positions 
        possible_positions = possible_positions.sample(frac=1).reset_index(drop=True)

        samples = []
        used_positions = []

        # Encapsultation function to check for non-overlapping samples
        def boxed_overlap(box1:tuple, box2:tuple) -> bool:
            x1, y1, x2, y2 = box1 #top left and bottom right coords 
            x3, y3, x4, y4 = box2 # top left and bottom right coords
            return not (x2 <= x3 or x4 <= x1 or y2 <= y3 or y4 <= y1)
        
        # Select for non-overlapping samples 
        for index, row in possible_positions.iterrows(): # Iterate over the possible positions 
            if len(samples) >= num_samples:
                break #stop iterating if the number of samples is >= 3
            x,y = row['x'], row['y']
            sample_box = (x, y, x + sample_size[0], y + sample_size[1]) # creates a tuple representing top left corner and bottom rifght corner

            if not any(boxed_overlap(sample_box, s) for s in used_positions):
                sample = self.image.crop(sample_box)
                samples.append(sample)
                used_positions.append(sample_box) # make sure we don't have the same sample in samples list 
        if len(samples) < num_samples:
            raise RuntimeError("Unable to find enough non-overlapping samples.")
        return samples

        
def main():
        #add path to image 
        transformer = ImageTransformer("images/cat.jpeg")
        sample_size = (100,50) # width, height 
        num_samples = 3
        
        try:
            samples = transformer.get_randomised_sample(sample_size, num_samples) 
            for i, sample in enumerate(samples):
                sample.show() # or save file using sample.save(f"sample_{i}.jpg")
        except ValueError as e:
            print(e)
        except RuntimeError as e:
            print(e)



if __name__ == "__main__":
        main()
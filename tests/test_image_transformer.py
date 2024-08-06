import unittest 
from PIL import Image 
import os
from image_transformer import ImageTransformer

class TestImageTransformer(unittest.TestCase):

    # setUpClass created a red image and saves it to disk
    @classmethod 
    def setUpClass(cls):
        # Create a test image 
        cls.test_image_path = "images/test_image.jpeg"
        cls.image = Image.new('RGB', (500,500), color = 'red') # Creates a image that is red 
        cls.image.save(cls.test_image_path)
        cls.transformer = ImageTransformer(cls.test_image_path)

    @classmethod
    def tearDownClass(cls):
        # remove the test image after all tests
        os.remove(cls.test_image_path)

    def test_param_check_valid(self):
        # Valid paramters 
        self.transformer.param_check((100,300), 3)
    
    def test_param_check_invalid_sample_size(self):
        with self.assertRaises(ValueError):
            self.transformer.param_check((600,600),3)
    
    def test_get_randomised_samples(self):
        # Test getting samples 
        samples = self.transformer.get_randomised_sample((50,50), 3)
        self.assertEqual(len(samples), 3)

    def test_get_randomised_sample_invalid(self):
        # Test getting more samples than possible 
        with self.assertRaises(RuntimeError):
            self.transformer.get_randomised_sample((100,100), 30)
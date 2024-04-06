from openai import OpenAI


class Image:
    """
    A class to handle image operations including creating images from text prompts.
    """

    def __init__(self):
        """
        Initializes the Image class with an OpenAI client.
        """
        self.client = OpenAI()

    def create_image(self, prompt: str) -> str:
        """
        Creates an image based on a text prompt and returns the image URL.

        :param prompt: The text prompt to generate an image from.
        :return: The URL of the generated image.
        """
        image = self.client.images.generate(model="dall-e-3", prompt=prompt)
        return image.data[0].url

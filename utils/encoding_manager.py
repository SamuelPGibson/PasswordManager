import numpy as np


class EncodingManager:
    ''' Placeholder class to do optional encoding/decoding
    '''
    def __init__(self):
        '''class to encode/decode account info'''
        
    def initiate_chars(self, chars_code:int):
        '''
        Purpose:
            converts encoded (scrambled chars) into actual characters to use for encoding/decoding
            multiplication of chars_code with self.__factors determines reorganizing index
            there is only one chars_code that will work
            if chars_code is incorrect, the program will continue but password decoding will be wrong
        Pre-conditions:
            :param chars_code : int - value to multiply with self.__factors
        Post-conditions:
            password encoding/decoding key is changed which affects password display
        Returns:
            (none)
        '''

    def encode(self, text:str):
        '''
        Purpose:
            encodes text
        Pre-conditions:
            :param text : str - text to be encoded
        Post-conditions:
            (none)
        Returns:
            :return : str - encoded text
        '''
        return text

    def decode(self, text:str):
        '''
        Purpose:
            decodes text
        Pre-conditions:
            :param text : str - text to be decoded
        Post-conditions:
            (none)
        Returns:
            :return : str - decoded text
        '''
        return text
    
    def raw_encode(self, text:str):
        '''
        Purpose:
            encodes text raw
            this will return the same result regardless of encryption key
        Pre-conditions:
            :param text : str - text to be encoded
        Post-conditions:
            (none)
        Returns:
            :return : str - encoded text
        '''
        return text

    def raw_decode(self, text:str):
        '''
        Purpose:
            decodes text raw
            this will return the same result regardless of encryption key
        Pre-conditions:
            :param text : str - text to be decoded
        Post-conditions:
            (none)
        Returns:
            :return : str - decoded text
        '''
        return text

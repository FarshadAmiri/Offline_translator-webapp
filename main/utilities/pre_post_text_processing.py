import re

def modify_translation(text):
    pattern = r'(?<!^)(?<=\n)(\d+\.)\s*\d+\.?'
    modified_text = re.sub(pattern, r'\1', text)
    return modified_text


def preprocess_text(text):
    preprocessed_text = re.sub(r'(\d+)-', r'\1.', text)
    return preprocessed_text
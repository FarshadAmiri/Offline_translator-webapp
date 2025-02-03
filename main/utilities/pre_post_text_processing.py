import re

def modify_translation(text):
    pattern = r'(?<!^)(?<=\n)(\d+\.)\s*\d+\.?'
    modified_text = re.sub(pattern, r'\1', text)
    return modified_text


def preprocess_text(text):
    preprocessed_text = re.sub(r'(\d+)-', r'\1.', text)
    return preprocessed_text


def single_word_input(text):
    return len(text.split()) == 1


def analyse_text(text):
    analysis_result = dict()
    single_word = single_word_input(text)

    analysis_result["single_word"] = single_word
    return analysis_result


def postprocess_text(translation, source_text_analysis):
    for i in range(5):
        translation = modify_translation(translation)

    if source_text_analysis["single_word"]:
        translated_words_list = translation.split()
        if (len(translated_words_list) > 1) and (set([translated_words_list[0]]) == set(translated_words_list)):
            translation = translated_words_list[0]
    return translation

    
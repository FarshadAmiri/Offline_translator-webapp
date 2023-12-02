import argostranslate.translate

def translate_en_fa(article_en):
    result = argostranslate.translate.translate(article_en, 'en', 'fa',)
    return result
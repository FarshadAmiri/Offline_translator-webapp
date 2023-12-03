import argostranslate.translate

def translate_en_fa(article_en):
    result = argostranslate.translate.translate(article_en, 'en', 'fa',)
    return result

def translate_fa_en(article_fa):
    result = argostranslate.translate.translate(article_fa, 'fa', 'en',)
    return result
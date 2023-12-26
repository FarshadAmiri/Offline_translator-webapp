import argostranslate.translate

def translate_en_fa(article_en):
    result = argostranslate.translate.translate(article_en, 'en', 'fa',)
    return result


def translate_fa_en(article_fa):
    result = argostranslate.translate.translate(article_fa, 'fa', 'en',)
    return result


def translate_ar_en(article_ar):
    result = argostranslate.translate.translate(article_ar, 'ar', 'en',)
    return result


def translate_en_ar(article_en):
    result = argostranslate.translate.translate(article_en, 'en', 'ar',)
    return result


def translate_fa_ar(article_fa):
    article_en = argostranslate.translate.translate(article_fa, 'fa', 'en',)
    result = argostranslate.translate.translate(article_en, 'en', 'ar',)
    return result


def translate_ar_fa(article_ar):
    article_en = argostranslate.translate.translate(article_ar, 'ar', 'en',)
    result = argostranslate.translate.translate(article_en, 'en', 'fa',)
    return result
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
    article_en = article_en.replace('(', '')
    article_en = article_en.replace(')', '')
    result = argostranslate.translate.translate(article_en, 'en', 'ar',)
    result =result.replace('&quot;', '"')
    return result


def translate_fa_ar(article_fa):
    article_en = translate_fa_en(article_fa)
    result = translate_en_ar(article_en)
    return result


def translate_ar_fa(article_ar):
    article_en = translate_ar_en(article_ar)
    result = translate_en_fa(article_en)
    return result


def translate(article, source_lang, target_lang):
    if source_lang == 'en' and target_lang == 'fa':
        return translate_en_fa(article)
    elif source_lang == 'fa' and target_lang == 'en':
        return translate_fa_en(article)
    elif source_lang == 'ar' and target_lang == 'en':
        return translate_ar_en(article)
    elif source_lang == 'en' and target_lang == 'ar':
        return translate_en_ar(article)
    elif source_lang == 'fa' and target_lang == 'ar':
        return translate_fa_ar(article)
    elif source_lang == 'ar' and target_lang == 'fa':
        return translate_ar_fa(article)
    else:
        return "Invalid input"
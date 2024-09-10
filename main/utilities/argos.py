import argostranslate.translate

# Persian 
def translate_en_fa(article_en):
    result = argostranslate.translate.translate(article_en, 'en', 'fa',)
    return result


def translate_fa_en(article_fa):
    result = argostranslate.translate.translate(article_fa, 'fa', 'en',)
    result = result.replace('&quot; ', '')
    result = result.replace(' &apos; ', "'")
    return result


# Arabic
def translate_ar_en(article_ar):
    result = argostranslate.translate.translate(article_ar, 'ar', 'en',)
    result = result.replace('&quot; ', '')
    result = result.replace(' &apos; ', "'")

    return result


def translate_en_ar(article_en):
    article_en = article_en.replace('(', '')
    article_en = article_en.replace(')', '')
    result = argostranslate.translate.translate(article_en, 'en', 'ar',)
    result = result.replace('&quot; ', '')

    return result


def translate_fa_ar(article_fa):
    article_en = translate_fa_en(article_fa)
    result = translate_en_ar(article_en)
    return result


def translate_ar_fa(article_ar):
    article_en = translate_ar_en(article_ar)
    result = translate_en_fa(article_en)
    return result


# Deutsch
def translate_en_de(article_en):
    result = argostranslate.translate.translate(article_en, 'en', 'de',)
    return result

def translate_de_en(article_de):
    result = argostranslate.translate.translate(article_de, 'de', 'en',)
    return result


# Hebrew
def translate_en_he(article_en):
    result = argostranslate.translate.translate(article_en, 'en', 'he',)
    return result

def translate_he_en(article_en):
    result = argostranslate.translate.translate(article_en, 'he', 'en',)
    return result

def translate_he_fa(article_he):
    article_en = translate_he_en(article_he)
    result = translate_en_fa(article_en)
    return result

def translate_fa_he(article_fa):
    article_en = translate_fa_en(article_fa)
    result = translate_en_he(article_en)
    return result

def translate_he_ar(article_he):
    article_en = translate_he_en(article_he)
    result = translate_en_ar(article_en)
    return result

def translate_ar_he(article_ar):
    article_en = translate_ar_en(article_ar)
    result = translate_en_he(article_en)
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
    elif source_lang == 'en' and target_lang == 'de':
        return translate_en_de(article)
    elif source_lang == 'de' and target_lang == 'en':
        return translate_de_en(article)
    elif source_lang == 'he' and target_lang == 'en':
        return translate_he_en(article)
    elif source_lang == 'en' and target_lang == 'he':
        return translate_en_he(article)
    elif source_lang == 'he' and target_lang == 'fa':
        return translate_he_fa(article)
    elif source_lang == 'fa' and target_lang == 'he':
        return translate_fa_he(article)
    elif source_lang == 'he' and target_lang == 'ar':
        return translate_he_ar(article)
    elif source_lang == 'ar' and target_lang == 'he':
        return translate_ar_he(article)
    else:
        return "Invalid input"

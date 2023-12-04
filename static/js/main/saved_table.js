function fa_digits($text){
    $persian_digits = array('۰','۱','۲','۳','۴','۵','۶','۷','۸','۹');
    $english_digits = array('0','1','2','3','4','5','6','7','8','9');
    $text = str_replace($english_digits, $persian_digits, $text);
    return $text;
}
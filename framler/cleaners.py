import string
import re


def remove_emails(text):
    return re.sub('\S*@\S*\s?', '', text)


def remove_newline_characters(text):
    return re.sub('\s+', ' ', text)


def remove_links_content(text):
    text = re.sub(r"http\S+", "", text)
    return text


def remove_multiple_space(text):
    return re.sub("\s\s+", " ", text)


def remove_punctuation(text):
    """https://stackoverflow.com/a/37221663"""
    import string  # noqa
    table = str.maketrans({key: None for key in string.punctuation})
    return text.translate(table)


def split_punctuation(text):
    '''
    Split string at punctuation characters
    :rtype list:
    '''
    rtext = []
    temp_text = []
    for char in text:
        if char not in string.punctuation:
            temp_text.append(char)
        else:
            new_text = ''.join(temp_text).lower().strip()
            rtext.append(new_text)
            temp_text = []
    return rtext


def remove_numeric(text):
    import string  # noqa
    table = str.maketrans({key: None for key in string.digits})
    return text.translate(table)


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def remove_stopwords(text, stopwords):
    return " ".join([word for word in text.split() if word not in stopwords])

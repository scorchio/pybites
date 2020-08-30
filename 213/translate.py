from bs4 import BeautifulSoup as Soup

def fix_translation(org_text, trans_text):
    """Receives original English text as well as text returned by translator.
       Parse trans_text restoring the original (English) code (wrapped inside
       code and pre tags) into it. Return the fixed translation str
    """
    org = Soup(org_text, 'html.parser')
    trans = Soup(trans_text, 'html.parser')
    orig_code = [elem for elem in org.find_all('code')]
    orig_pre = [elem for elem in org.find_all('pre')]
    for i, elem in enumerate(trans.find_all('code')):
      elem.replace_with(orig_code[i])
    for i, elem in enumerate(trans.find_all('pre')):
      elem.replace_with(orig_pre[i])
    return str(trans)

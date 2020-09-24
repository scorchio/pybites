import re

def strip_comments(code):
    result = re.sub(r'^[\s]*#[^#]+?\n', '', code, flags=re.MULTILINE)
    result = re.sub(r'^(.*?)  #[^#]+?\n', '\\1', result, flags=re.MULTILINE)
    result = re.sub(r'^[\s]*"""[^#]+?"""\n', '', result, flags=re.MULTILINE)
    return result

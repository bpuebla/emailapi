import re

def read_txt(path):
    with open(path,'r') as f:
        return f.read()
    
def clean_string(s):
    # Replace multiple \r, \n, or spaces with a single space
    return re.sub(r'[\r\n]+', '\n', s).strip()
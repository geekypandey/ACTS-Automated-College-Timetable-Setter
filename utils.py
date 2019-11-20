import camelot

def extract_json(filename):
    tables = camelot.read_pdf(filename,pages='4')
    tables[0].to_json('foo.json')
    print('Table successfully extracted')

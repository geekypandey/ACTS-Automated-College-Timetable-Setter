import camelot

def extract_df(filename):
    tables = camelot.read_pdf(filename,pages='4')
    df = tables[0].df
    print('Table successfully extracted')
    return df

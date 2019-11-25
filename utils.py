import camelot

def extract_df(filename,page_number):
    tables = camelot.read_pdf(filename,pages=page_number)
    df = tables[0].df
    print('Table successfully extracted')
    return df

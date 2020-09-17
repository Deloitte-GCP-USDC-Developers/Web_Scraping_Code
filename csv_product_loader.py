import pandas

class CsvProductLoader(object):
    PRODUCTNAME_CSVFILE = ''
    @classmethod
    def loadProductNames(cls):
        pl_df = pandas.read_csv(cls.PRODUCTNAME_CSVFILE)
        return pl_df['name'].tolist()

    @classmethod
    def loadProductDefaultUrls(cls):
        pl_df = pandas.read_csv(cls.PRODUCTNAME_CSVFILE)
        return pl_df['cnet_url_check'].tolist()
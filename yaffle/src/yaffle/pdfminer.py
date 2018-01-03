# -*- encoding: utf-8

# Based on https://stackoverflow.com/a/26495057/1558022

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path, outfile):
    """Given a path to a PDF file, save the text contents of the file.

    :param path: PDF document to analyse.
    :param outfile: File to save the text contents of the document to.

    """
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()

    with open(path, 'rb') as fp, open(outfile, 'wb') as outfp:
        try:
            device = TextConverter(rsrcmgr, outfp=outfp, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr=rsrcmgr, device=device)

            for page in PDFPage.get_pages(fp, check_extractable=True):
                interpreter.process_page(page)
        finally:
            device.close()

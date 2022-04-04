# -*- coding:utf-8*-
# 利用PyPDF2模块合并同一文件夹下的所有PDF文件

import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from utilles import get_file_list


def merge_pdf(filepath, outfile):
    """合并同一目录下的所有PDF文件.
    Args:
        filepath (str): 文件夹路径
        outfile (str): 输出文件路径
    """
    output = PdfFileWriter()
    outputPages = 0
    pdf_list = get_file_list(filepath, ".pdf")

    if pdf_list:
        for pdf_file in pdf_list:
            # print("路径: %s" % pdf_file)

            # 读取源PDF文件
            input = PdfFileReader(open(pdf_file, "rb"))

            # 获得源PDF文件中页面总数
            pageCount = input.getNumPages()
            outputPages += pageCount
            # print("页数: %d" % pageCount)

            # 分别将page添加到输出output中
            for iPage in range(pageCount):
                output.addPage(input.getPage(iPage))

        # print("合并后的总页数: %d." % outputPages)
        # 写入到目标PDF文件
        outputStream = open(os.path.join(filepath, outfile), "wb")
        output.write(outputStream)
        outputStream.close()
        return "PDF文件合并完成"
    else:
        return "没有可以合并的PDF文件"

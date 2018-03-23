# -*- coding: utf-8 -*-
"""
将excel文件转成json
"""

import xlrd
import json
import codecs
import os
import copy
from collections import OrderedDict
from pprint import pprint

def excel_json(file_path):
    if get_data(file_path) is not None:
        book=get_data(file_path)
        worksheets=book.sheet_names()
        all_data = [] #总数据

        #遍历每一个工作表
        for i in worksheets:
            #遍历所有的行和列将数据转为json
            if i =='CateTag':
                catetag_data = OrderedDict()
                sheet = book.sheet_by_index(worksheets.index(i))
                row_o = sheet.row(0)
                nrows = sheet.nrows
                ncols = sheet.ncols
                for i in range(1, nrows):  # 行
                    # 储存单元格的内容
                    fields = OrderedDict()
                    for j in range(ncols):#列
                    #获取标题对应的内容,因为第一行的内容也是用字典存储的，
                    # 但是没有对应的key,所以编译器自动将值的属性当做了key
                        if j > 1:

                            title_de = str(row_o[j].value)
                            fields[title_de] = sheet.row_values(i)[j]

                        else:
                            title_de = row_o[j].value
                            pk_int= lambda sheet1 : sheet1 if isinstance(sheet1,str) else int(sheet1)
                            catetag_data[title_de]=pk_int(sheet.row_values(i)[j])
                    catetag_data['fields'] = fields
                    zj_data=copy.deepcopy(catetag_data)
                    all_data.append(zj_data)



            else:
                post_data = OrderedDict()
                sheet = book.sheet_by_index(worksheets.index(i))
                row_o = sheet.row(0)
                nrows = sheet.nrows
                ncols = sheet.ncols
                for i in range(1,nrows):
                    fields = OrderedDict()
                    for j in range(ncols):
                        if j >1:
                            title_de = str(row_o[j].value)
                            pk_int = lambda sheet1: sheet1 if isinstance(sheet1, str) else int(sheet1)
                            fields[title_de] = pk_int(sheet.row_values(i)[j])
                        else:
                            title_de=str(row_o[j].value)
                            pk_int = lambda sheet1: sheet1 if isinstance(sheet1, str) else int(sheet1)
                            post_data[title_de]=pk_int(sheet.row_values(i)[j])
                            # print(type(sheet.row_values(i)[j]))
                            # print(type( post_data[title_de]))
                    post_data['fields'] = fields
                    # pprint(post_data['fields'])
                    # print(post_data)
                    zj_data = copy.deepcopy(post_data)
                    all_data.append(zj_data)

        # print(type(all_data[4]['fields']))
        print(type(all_data[4]['pk']))
        all_data=(json.dumps(all_data,indent= 4,sort_keys=True))
        # pprint(all_data)
        savefile(all_data)



def get_data(file_path):
    with xlrd.open_workbook(file_path) as f:
        return f

def savefile(data):
    global output
    try:
        output=codecs.open('post_json.json','w','utf-8')
        output.write(data)
    except Exception:
        print('excel 打开失败')
    finally:
        output.close()
#文件都是写死的，必要时可以自己换
file_path='post_xiangqing.xlsx'
get_data(file_path)
excel_json(file_path)
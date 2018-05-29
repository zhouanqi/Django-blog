# -*- coding: utf-8 -*-
"""
将excel文件转成json
"""

import xlrd
import json
import codecs
import os

def excel_json(file_path):
    if get_data(file_path) is not None:
        book=get_data(file_path)
        worksheets=book.sheet_names()
        #打印sheet列表和列表序号
        # for sheet in worksheets:
        #     print('%s,%s'%(worksheets.index(sheet),sheet))
        # inp=input('请输入表单对应编号，对应表单自动转为json:\n')
        sheet=book.sheet_by_index(0)
        row_o=sheet.row(0)
        nrows=sheet.nrows
        ncols=sheet.ncols
        result={}

        #遍历所有的行和列将数据转为json
        for i in range(1,nrows):#行
            result[i] = {}
            tmp={}#储存单元格的内容
            for j in range(ncols):#列
                title_de=str(row_o[j].value)
                #获取标题对应的内容,因为第一行的内容也是用字典存储的，但是没有对应的key,所以编译器自动将值的属性当做了key
                tmp[title_de]=sheet.row_values(i)[j]
            result[i]=tmp
        # 将python对象编程json字符串,json.dumps(result,indent= 4,sort_keys=True)为了输出中文
        json_data=(json.dumps(result,indent= 4,sort_keys=True))
        savefile(json_data)

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
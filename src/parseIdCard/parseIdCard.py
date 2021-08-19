#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FilePath: /Python/parseIdCard/src/parseIdCard/parseIdCard.py
Author: 潘高
LastEditors: 潘高
Date: 2021-08-18 15:32:37
LastEditTime: 2021-08-19 20:25:48
Description: 解析身份证
usage: 运行前，请确保本机已经搭建Python3开发环境。详细教程请移步至 https://blog.pangao.vip/Python环境搭建及模块安装/
        Example:
            from parseIdCard import parseIdCard
            parseIdCard.parseJYM('12345678901234567')
'''


import os
import re
import sqlite3
from datetime import datetime


def parseArea(areaId):
    '''解析地区编码(6位数字)。输入6位地区编码，返回：{code, id, area}'''
    if isinstance(areaId, int):
        # 整数
        areaId = str(areaId)
        return __checkArea(areaId)
    elif isinstance(areaId, str):
        # 字符串
        areaId = areaId.replace(' ', '')    # 去除空格
        areaId = areaId.replace('\n', '')    # 去除回车
        areaIdList = re.split(',|;|，|；|、', areaId)    # 以常见的分隔符分割
        if len(areaIdList) == 1:
            return __checkArea(areaId)
        else:
            resultList = list()
            for areaId in areaIdList:
                resultList.append(__checkArea(areaId))
            return resultList
    elif isinstance(areaId, list):
        # 列表
        resultList = list()
        for aid in areaId:
            aid = str(aid)
            aid = aid.replace(' ', '')    # 去除空格
            aid = aid.replace('\n', '')    # 去除回车
            resultList.append(__checkArea(aid))
        return resultList
    else:
        return {'code': 'Error', 'id': areaId, 'area': '非法输入，请输入6位地区编码'}

def parseBirthdate(ymd):
    '''解析出生日期(8位数字)。输入8位出生日期，返回：{code, id, age}'''
    if isinstance(ymd, int):
        # 整数
        ymd = str(ymd)
        return __checkBirthdate(ymd)
    elif isinstance(ymd, str):
        # 字符串
        ymd = ymd.replace(' ', '')    # 去除空格
        ymd = ymd.replace('\n', '')    # 去除回车
        ymdList = re.split(',|;|，|；|、', ymd)    # 以常见的分隔符分割
        if len(ymdList) == 1:
            return __checkBirthdate(ymd)
        else:
            resultList = list()
            for ymd in ymdList:
                resultList.append(__checkBirthdate(ymd))
            return resultList
    elif isinstance(ymd, list):
        # 列表
        resultList = list()
        for y in ymd:
            y = str(y)
            y = y.replace(' ', '')    # 去除空格
            y = y.replace('\n', '')    # 去除回车
            resultList.append(__checkBirthdate(y))
        return resultList
    else:
        return {'code': 'Error', 'id': ymd, 'age': '非法输入，请输入8位出生日期'}

def parseGender(gender):
    '''解析性别。输入1位性别编码，返回：{code, id, gender}'''
    if isinstance(gender, int):
        # 整数
        gender = str(gender)
        return __checkGender(gender)
    elif isinstance(gender, str):
        # 字符串
        gender = gender.replace(' ', '')    # 去除空格
        gender = gender.replace('\n', '')    # 去除回车
        genderList = re.split(',|;|，|；|、', gender)    # 以常见的分隔符分割
        if len(genderList) == 1:
            return __checkGender(gender)
        else:
            resultList = list()
            for gender in genderList:
                resultList.append(__checkGender(gender))
            return resultList
    elif isinstance(gender, list):
        # 列表
        resultList = list()
        for g in gender:
            g = str(g)
            g = g.replace(' ', '')    # 去除空格
            g = g.replace('\n', '')    # 去除回车
            resultList.append(__checkGender(g))
        return resultList
    else:
        return {'code': 'Error', 'id': gender, 'gender': '非法输入，请输入1位性别编码'}

def parseJYM(inStr):
    '''校验校验码。输入17位字符串，返回：{code, id, area, age, gender, jym}'''
    if isinstance(inStr, int):
        # 整数
        inStr = str(inStr)
        return __checkJYM(inStr)
    elif isinstance(inStr, str):
        # 字符串
        inStr = inStr.replace(' ', '')    # 去除空格
        inStr = inStr.replace('\n', '')    # 去除回车
        inList = re.split(',|;|，|；|、', inStr)    # 以常见的分隔符分割
        if len(inList) == 1:
            return __checkJYM(inStr)
        else:
            resultList = list()
            for il in inList:
                resultList.append(__checkJYM(il))
            return resultList
    elif isinstance(inStr, list):
        # 列表
        resultList = list()
        for s in inStr:
            s = str(s)
            s = s.replace(' ', '')    # 去除空格
            s = s.replace('\n', '')    # 去除回车
            resultList.append(__checkJYM(s))
        return resultList
    else:
        return {'code': 'Error', 'id': inStr, 'jym': '非法输入，请输入身份证前17位'}

def parseIdCard(idCard):
    '''解析身份证号码'''
    if isinstance(idCard, int):
        # 整数
        idCard = str(idCard)
        return __checkIdCard(idCard)
    elif isinstance(idCard, str):
        # 字符串
        idCard = idCard.replace(' ', '')    # 去除空格
        idCard = idCard.replace('\n', '')    # 去除回车
        idCardList = re.split(',|;|，|；|、', idCard)    # 以常见的分隔符分割
        if len(idCardList) == 1:
            return __checkIdCard(idCard)
        else:
            resultList = list()
            for idCard in idCardList:
                resultList.append(__checkIdCard(idCard))
            return resultList
    elif isinstance(idCard, list):
        # 列表
        resultList = list()
        for cid in idCard:
            cid = str(cid)
            cid = cid.replace(' ', '')    # 去除空格
            cid = cid.replace('\n', '')    # 去除回车
            resultList.append(__checkIdCard(cid))
        return resultList
    else:
        return {'code': 'Error', 'id': idCard, 'info': '非法输入，请输入18位身份证编码'}

def __checkArea(areaId):
    '''校验地区。输入6位地区编码字符串，返回：{code, id, area}'''
    if len(areaId) != 6:
        return {'code': 'Error', 'id': areaId, 'area': '地区编码应该为6位'}
    else:
        if areaId.isdigit():
            dbAreaPath = os.path.join(os.path.dirname(__file__), 'area')
            conn = sqlite3.connect(dbAreaPath)
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT area FROM area WHERE id = '" + areaId + "'")
            returnArea = ''
            for c in cur:
                returnArea = c[0]
            conn.close()
            if returnArea == '':
                return {'code': 'Error', 'id': areaId, 'area': '未知地区编码'}
            else:
                return {'code': 'OK', 'id': areaId, 'area': returnArea}
        return {'code': 'Error', 'id': areaId, 'area': '非法地区编码'}
    
def __checkBirthdate(ymd):
    '''校验出生日期。输入8位出生日期字符串，返回：{code, id, age}'''
    if len(ymd) != 8:
        return {'code': 'Error', 'id': ymd, 'age': '出生日期应该为8位'}
    else:
        if ymd.isdigit():
            yearInt = int(ymd[:4])
            currentYearInt = datetime.now().year
            age = currentYearInt - yearInt
            if age >= 0:
                # 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
                # 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
                if (yearInt % 4 == 0 or yearInt % 100 == 0 and yearInt % 4 == 0):
                    ereg = re.compile('([1-9][0-9]{3})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))')
                else:
                    ereg = re.compile('([1-9][0-9]{3})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))')
                if (re.match(ereg, ymd)):
                    # 校验通过
                    return {'code': 'OK', 'id': ymd, 'age': age}
        return {'code': 'Error', 'id': ymd, 'age': '非法出生日期'}

def __checkGender(gender):
    '''校验性别。输入1位性别编码字符串，返回：{code, id, gender}'''
    if len(gender) != 1:
        return {'code': 'Error', 'id': gender, 'gender': '性别编码应该为1位'}
    else:
        if gender.isdigit():
            genderInt = int(gender)
            if genderInt % 2 == 0:
                # 偶数 => 女
                return {'code': 'OK', 'id': gender, 'gender': '女'}
            else:
                # 奇数 => 男
                return {'code': 'OK', 'id': gender, 'gender': '男'}
        else:
            return {'code': 'Error', 'id': gender, 'gender': '非法性别编码'}
    
def __checkJYM(inStr):
    '''校验校验码。输入17位字符串，返回：{code, id, area, age, gender, jym}'''
    if len(inStr) != 17:
        return {'code': 'Error', 'id': inStr, 'jym': '请输入身份证前17位'}
    else:
        if inStr.isdigit():
            # 校验地区
            resultArea = __checkArea(inStr[:6])
            area = resultArea['area']
            if resultArea['code'] == 'Error':
                return {'code': 'Error', 'id': inStr, 'jym': area}
            # 校验出生日期
            resultBirthdate = __checkBirthdate(inStr[6:14])
            age = resultBirthdate['age']
            if resultBirthdate['code'] == 'Error':
                return {'code': 'Error', 'id': inStr, 'jym': age}
            # 校验性别
            resultGender = __checkGender(inStr[16:17])
            gender = resultGender['gender']
            if resultGender['code'] == 'Error':
                return {'code': 'Error', 'id': inStr, 'jym': gender}
            S = (int(inStr[0]) + int(inStr[10])) * 7 + (int(inStr[1]) + int(inStr[11])) * 9 + (int(inStr[2]) + int(inStr[12])) * 10 + (int(inStr[3]) + int(inStr[13])) * 5 + (int(inStr[4]) + int(inStr[14])) * 8 + (int(inStr[5]) + int(inStr[15])) * 4 + (int(inStr[6]) + int(inStr[16])) * 2 + int(inStr[7]) * 1 + int(inStr[8]) * 6 + int(inStr[9]) * 3
            Y = S % 11
            jym = ''    # 校验码
            jymList = '10X98765432'
            if Y <= 10:
                jym = jymList[Y]  # 校验码
                return {'code': 'OK', 'id': inStr, 'area': area, 'age': age, 'gender': gender, 'jym': jym}
        return {'code': 'Error', 'id': inStr, 'jym': '非法输入参数'}

def __checkIdCard(idCard):
    '''校验身份证。输入18位身份证字符串，返回：{code, id, gender}'''
    if len(idCard) != 18:
        return {'code': 'Error', 'id': idCard, 'gender': '身份证编码应该为18位'}
    else:
        idCard17 = idCard[:17]    # 前17位
        idCardLast = idCard[-1:]    # 最后一位
        if idCard17.isdigit() and re.match('([0-9]|X|x)', idCardLast):
            resultJYM = __checkJYM(idCard17)
            if resultJYM['code'] == 'Error':
                infoList = list()
                if 'area' in resultJYM:
                    infoList.append(resultJYM['area'])
                    del resultJYM['area']
                if 'age' in resultJYM:
                    infoList.append(resultJYM['age'])
                    del resultJYM['age']
                if 'gender' in resultJYM:
                    infoList.append(resultJYM['gender'])
                    del resultJYM['gender']
                if 'jym' in resultJYM:
                    infoList.append(resultJYM['jym'])
                    del resultJYM['jym']
                resultJYM['info'] = '；'.join(infoList)
                return resultJYM
            if idCardLast == resultJYM['jym']:
                del resultJYM['jym']
                resultJYM['info'] = '身份证校验通过'
                return resultJYM
            else:
                return {'code': 'Error', 'id': idCard, 'info': '身份证校验码错误'}
        else:
            return {'code': 'Error', 'id': idCard, 'info': '非法身份证编码'}

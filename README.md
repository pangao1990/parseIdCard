
更多内容，请访问我的 [个人博客](https://blog.pangao.vip/可能是Python中最好用的身份证解析工具—parseIdCard/)。

---

### 前言
> 2021.08.03，武汉新冠疫情似有复苏的迹象，于是武汉政府立即采取果断措施，启动全城核酸检测。很荣幸，我们公司也积极参与核酸检测工作。我在其中参与了核酸实验和数据校对的工作。在数据校对过程中，主要矛盾体现在身份证不匹配的问题上。于是，我写了这个可能是Python中最好用的身份证解析工具--parseIdCard。

### 身份证格式说明
根据〖中华人民共和国国家标准GB11643-1999〗中有关公民身份号码的规定，公民身份号码是特征组合码，由十七位数字本体码和一位数字校验码组成。排列顺序从左至右依次为：六位数字地址码，八位数字出生日期码，三位数字顺序码和一位数字校验码。如下所示：

42 01 16 20200103 12 3 X

- 42 => 湖北（省）
- 01 => 武汉（市）
- 16 => 黄陂（区）
- 20200103 => 2020年01月03日（出生日期）
- 12 => 派出所代码
- 3 => 性别码
- X => 校验码

### 具体代码实现

#### 地区码校验

地区码比较简单，就是地区与编码的一一对应关系，整理如下数据库就行。

```
420101	湖北武汉市市辖区
420102	湖北武汉市江岸区
420103	湖北武汉市江汉区
420104	湖北武汉市乔口区
420105	湖北武汉市汉阳区
420106	湖北武汉市武昌区
420107	湖北武汉市青山区
420111	湖北武汉市洪山区
420112	湖北武汉市东西湖区
420113	湖北武汉市汉南区
420114	湖北武汉市蔡甸区
420115	湖北武汉市江夏区
420116	湖北武汉市黄陂区
420117	湖北武汉市新洲区
......
```

再将地区码与数据库比对，用 Python 代码实现如下：

```
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
```

#### 出生日期校验
众所周知，日期是有一定的规律的。比如：年份是四位数字，月份和日是两位数字，月份最多只有12月，日最多只有31，不过有的月份是28、29、30。把这些常见的规则，用 Python 代码实现如下：

```
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
```

#### 性别校验
性别校验的规则比较简单，奇数为男，偶数为女。用 Python 代码实现如下：

```
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
```

#### 校验码
其他组码都好理解，这最后一位的校验码，就比较复杂了。校验码是根据前面十七位数字码，按照ISO7064:1983.MOD11-2校验码计算出来的。详细步骤如下所示：

```
1、将身份证号码前17位数分别乘以不同的系数。从第一位到第十七位的系数分别为：7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2
2、将这17位数字和系数相乘的结果相加
3、用加出来和除以11，看余数是多少
4、余数只可能有0 1 2 3 4 5 6 7 8 9 10这11个数字。其分别对应的校验码为1 0 X 9 8 7 6 5 4 3 2 
```

按照以上逻辑，用 Python 代码实现如下：

```
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
```

#### 身份证编码校验
综上，即可对整体身份证编码进行校验，用 Python 代码实现如下：

```
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
```

### parseIdCard工具的使用

安装 parseIdCard 工具，如下所示：

```
pip install parseIdCard
```
使用方法，如下所示：

```
from parseIdCard import parseIdCard

## 校验地区码。可以输入整型，列表，字符串(可用逗号等分割多条信息码)
parseIdCard.parseArea(420116)
# 输出 {'code': 'OK', 'id': '420116', 'area': '湖北武汉市黄陂区'}

parseIdCard.parseArea(['429116', '42010'])
# 输出 [{'code': 'Error', 'id': '429116', 'area': '未知地区编码'}, {'code': 'Error', 'id': '42010', 'area': '地区编码应该为6位'}]

parseIdCard.parseArea('420116,420101')
# 输出 [{'code': 'OK', 'id': '420116', 'area': '湖北武汉市黄陂区'}, {'code': 'OK', 'id': '420101', 'area': '湖北武汉市市辖区'}]


## 校验出生日期。可以输入整型，列表，字符串(可用逗号等分割多条信息码)
parseIdCard.parseBirthdate(20200103)
# 输出 {'code': 'OK', 'id': '20200103', 'age': 1}

parseIdCard.parseBirthdate(['00000000', '22221203'])
# 输出 [{'code': 'Error', 'id': '00000000', 'age': '非法出生日期'}, {'code': 'Error', 'id': '22221203', 'age': '非法出生日期'}]

parseIdCard.parseBirthdate('20200103, 20121222')
# 输出 [{'code': 'OK', 'id': '20200103', 'age': 1}, {'code': 'OK', 'id': '20121222', 'age': 9}]


## 校验性别。可以输入整型，列表，字符串(可用逗号等分割多条信息码)
parseIdCard.parseGender(1)
# 输出 {'code': 'OK', 'id': '1', 'gender': '男'}

parseIdCard.parseGender(['2', 'X'])
# 输出 [{'code': 'OK', 'id': '2', 'gender': '女'}, {'code': 'Error', 'id': 'X', 'gender': '非法性别编码'}]

parseIdCard.parseGender('12;9')
# 输出 [{'code': 'Error', 'id': '12', 'gender': '性别编码应该为1位'}, {'code': 'OK', 'id': '9', 'gender': '男'}]


## 计算校验码。可以输入整型，列表，字符串(可用逗号等分割多条信息码)
parseIdCard.parseJYM(42011620200103123)
# 输出 {'code': 'OK', 'id': '42011620200103123', 'area': '湖北武汉市黄陂区', 'age': 1, 'gender': '男', 'jym': 'X'}

parseIdCard.parseJYM(['02011620200103123', '4201162020010'])
# 输出 [{'code': 'Error', 'id': '02011620200103123', 'jym': '未知地区编码'}, {'code': 'Error', 'id': '4201162020010', 'jym': '请输入身份证前17位'}]

parseIdCard.parseJYM('02011620200103123，4201162020010')
# 输出 [{'code': 'Error', 'id': '02011620200103123', 'jym': '未知地区编码'}, {'code': 'Error', 'id': '4201162020010', 'jym': '请输入身份证前17位'}]


## 校验身份证编码。可以输入整型，列表，字符串(可用逗号等分割多条信息码)
parseIdCard.parseIdCard(420116202001031248)
# 输出 {'code': 'OK', 'id': '42011620200103124', 'area': '湖北武汉市黄陂区', 'age': 1, 'gender': '女', 'info': '身份证校验通过'}

parseIdCard.parseIdCard([420116202001031248, '42011620200103123X'])
# 输出 [{'code': 'OK', 'id': '42011620200103124', 'area': '湖北武汉市黄陂区', 'age': 1, 'gender': '女', 'info': '身份证校验通过'}, {'code': 'OK', 'id': '42011620200103123', 'area': '湖北武汉市黄陂区', 'age': 1, 'gender': '男', 'info': '身份证校验通过'}]

parseIdCard.parseIdCard('42011620200103124X；42011620200103123')
# 输出 [{'code': 'Error', 'id': '42011620200103124X', 'info': '身份证校验码错误'}, {'code': 'Error', 'id': '42011620200103123', 'gender': '身份证编码应该为18位'}]
```

### 计划升级
后续版本计划新增智能修复身份证编码的功能。

### 后记
附上一个我穿防护服的镇楼照。希望疫情尽快过去，以后一切顺利。

![image](https://cdn.jsdelivr.net/gh/pangao1990/pangao1990.github.io@master/pic/可能是Python中最好用的身份证解析工具—parseIdCard.jpg)

---

更多编程教学请关注公众号：**潘高陪你学编程**

![image](https://cdn.jsdelivr.net/gh/pangao1990/pangao1990.github.io@master/pic/潘高陪你学编程.jpg)

---
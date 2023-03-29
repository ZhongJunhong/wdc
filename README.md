# wdc
数据范围：1951-2020

数据清洗流程：

- TXT数据格式转换为sqlite database格式
- 检查转换结果
- 筛选质量控制码为0的数据。
- TXT数据转换为csv数据
  - 读取TXT为dataframe格式
  - 将质量控制码为0以外的值改为空
  - 去除质量控制码字段
  - 经纬度、高程转为正确的小数格式
  - 气象数据按照要求转（有待研究）
  - 按照气象站点进行归类，至新的dataframe
  - 根据该TXT数据所属年份，创建年份目录
  - 向年份目录写入新的csv文件，文件名同TXT文件名
- csv数据转为gdb：一种气象要素的一个月的数据对应一张csv数据表及一份gdb数据。

注：2015年以后的数据，缺漏较多，是师兄同门整理的，不是官方出品。

txt2gdb.py: 将datasets转为文件地理数据库GeoDatabase格式

由于转换结果太大所以上传百度网盘：

> 链接: https://pan.baidu.com/s/1TK0ttApPY38M59IOk_ugcw?pwd=ztdr 提取码: ztdr 

txt2db.py: 将datasets转为文件地理数据库sqlite格式

datasets.zip: 重新使用txt2db.py和txt2gdb.py时需要讲datasets.zip解压，放在工作根目录下。

因为datasets.zip文件太大所以上传百度网盘：

> 链接: https://pan.baidu.com/s/1FTBKoNmPssC9Pb4nvVX8ZA?pwd=mfmd 提取码: mfmd 

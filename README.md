# wdc
weather data clean and trans to geodatabase

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

- csv数据转为shp数据：一种气象要素的一个月的数据对应一张csv数据表及一份shp数据，再按年份归类到文件夹
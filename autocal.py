from bjontegaard_metric import *
import argparse
import csv
from itertools import groupby

def extract_columns(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        data = [[row[0], row[1], float(row[2]), float(row[3])] for row in reader]
        # 使用 groupby 函数将相同的数据分为同一组
        data.sort(key=lambda x: x[0])  # 先按第一列排序
        groups = []
        for key, group in groupby(data, lambda x: x[0]):
            group_data = {'seqs': key, 'bitrate': [], 'psnr': []}
            for item in group:
                group_data['bitrate'].append(item[2])
                group_data['psnr'].append(item[3])
            groups.append(group_data)
        return groups

def calculate_bdrate(ref, test):
    avg = 0
    seqs_nums = len(ref)
    for seq in range(seqs_nums):
        bdrate = BD_RATE(ref[seq]['bitrate'], ref[seq]['psnr'],
                      test[seq]['bitrate'], test[seq]['psnr']) / 100
        print('Video ', ref[seq]['seqs'],
              'bd-rate is ', f'{bdrate: .8f}')
        avg += bdrate
    avg = (avg / seqs_nums)
    print('average bd-rate is ', f'{avg: .8f}')

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description='Extract first three columns from CSV files')

# 添加命令行参数
parser.add_argument('file1', help='first CSV file')
parser.add_argument('file2', help='second CSV file')

# 解析命令行参数
args = parser.parse_args()

# 提取第一个 CSV 文件的数据并分组
ref_data = extract_columns(args.file1)

# 提取第二个 CSV 文件的数据并分组
test_data = extract_columns(args.file2)

calculate_bdrate(ref_data, test_data)
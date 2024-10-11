import os
import re
from datetime import datetime

def parse_log_file(file_path, next_file_time=None):
    """
    解析日志文件，提取 Makespan 结果和完成时间
    :param file_path: 日志文件的路径
    :param next_file_time: 下一个文件的完成时间，用来计算执行时间
    :return: 文件名, 执行时间 (毫秒), Makespan 结果
    """
    makespan = None
    process_time = None

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 Overall maximum shortest path delay
    makespan_match = re.search(r'Overall maximum shortest path delay: ([\d.]+)', content)
    if makespan_match:
        makespan = float(makespan_match.group(1))

    # 提取 Process completed at 时间
    time_match = re.search(r'Process completed at: ([\d-]+\s[\d:.]+)', content)
    if time_match:
        process_time = datetime.strptime(time_match.group(1), '%Y-%m-%d %H:%M:%S.%f')

    # 如果有下一个文件的时间，则计算执行时间 (毫秒)
    if next_file_time:
        exec_time = (next_file_time - process_time).total_seconds() * 1000  # 转换为毫秒
    else:
        exec_time = 0  # 第一个文件无前置文件，执行时间设为0

    return os.path.basename(file_path), exec_time, makespan

def analyze_logs(directory):
    """
    分析指定目录下的所有日志文件，输出 文件名, 执行时间 (毫秒), Makespan 结果
    :param directory: 日志文件所在目录
    :return: 解析结果列表
    """
    log_files = sorted([f for f in os.listdir(directory) if f.endswith(".log")],
                       key=lambda f: os.path.getmtime(os.path.join(directory, f)))

    results = []
    previous_time = None

    for i in range(len(log_files)):
        log_file = log_files[i]
        file_path = os.path.join(directory, log_file)

        # 如果有下一个文件，则获取下一个文件的完成时间
        next_file_time = None
        if i + 1 < len(log_files):
            next_file = os.path.join(directory, log_files[i + 1])
            with open(next_file, 'r', encoding='utf-8') as f:
                next_content = f.read()
            next_time_match = re.search(r'Process completed at: ([\d-]+\s[\d:.]+)', next_content)
            if next_time_match:
                next_file_time = datetime.strptime(next_time_match.group(1), '%Y-%m-%d %H:%M:%S.%f')

        # 解析日志文件
        filename, exec_time, makespan = parse_log_file(file_path, next_file_time)
        results.append((filename, exec_time, makespan))

    return results

def save_results(results, output_file):
    """
    保存分析结果到日志格式的文件
    :param results: 分析结果列表
    :param output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("文件名, 执行时间（毫秒）, Makespan 结果\n")
        for filename, exec_time, makespan in results:
            f.write(f"{filename}, {exec_time:.3f}, {makespan}\n")
    print(f"分析结果已保存到: {output_file}")

if __name__ == "__main__":
    # 指定日志文件路径和输出文件路径
    log_directory = "/Users/duling/Desktop/code/Geo_All2All/output/us"  # 日志文件的路径
    output_file = "/Users/duling/Desktop/code/Geo_All2All/output/shortest_path/_analyze2.log"  # 输出的结果路径

    # 分析日志文件
    results = analyze_logs(log_directory)

    # 保存结果
    save_results(results, output_file)
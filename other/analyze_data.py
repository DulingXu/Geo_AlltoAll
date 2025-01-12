import os
import numpy as np
import glob

# 定义文件路径
log_dir = '/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/key_result'
output_dir = '/Users/duling/Desktop/code/Geo_All2All/output/display'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 获取所有包含"_0.1", "_0.2", "_0.3", "_0.4", "_0.5"的文件
files_patterns = ['*_0.1*.log', '*_0.2*.log', '*_0.3*.log', '*_0.4*.log', '*_0.5*.log']

# 定义函数从日志文件中提取 Makespan 结果
def extract_makespan(file_path):
    makespan_values = []
    with open(file_path, 'r') as f:
        next(f)  # 跳过第一行标题行
        for line in f:
            try:
                # 拆分行，获取最后一个数值 (Makespan)
                makespan = float(line.strip().split(',')[-1])
                makespan_values.append(makespan)
            except ValueError:
                # 跳过无法转换的行
                print(f"Warning: 无法处理文件 {os.path.basename(file_path)} 中的行: {line.strip()}")
    return makespan_values

# 准备将输出保存到文件
output_file_path = os.path.join(output_dir, 'makespan_percentiles_results.txt')
with open(output_file_path, 'w') as output_file:

    # 分别处理每个模式下的文件
    percentiles = [99, 95, 90]
    for pattern in files_patterns:
        files = glob.glob(os.path.join(log_dir, pattern))

        if not files:
            output_file.write(f"\n未找到模式 {pattern} 的数据文件\n")
            print(f"\n未找到模式 {pattern} 的数据文件")
            continue  # 如果没有找到该模式的文件，跳过展示

        all_makespan_dict = {}
        dp_makespan = []
        all_other_makespan = []  # 用于存储所有非 dp 方案的数据

        # 从文件中提取所有的 Makespan 结果
        for file in files:
            makespan_values = extract_makespan(file)

            # 文件名作为字典键，只保留文件名不包括路径
            all_makespan_dict[os.path.basename(file)] = makespan_values

            # 判断文件名中是否包含 'dp'
            if 'dp' in file:
                dp_makespan.extend(makespan_values)
            else:
                all_other_makespan.extend(makespan_values)  # 累加所有非 dp 的 makespan

        output_file.write(f"\n模式 {pattern} 的结果：\n")
        print(f"\n模式 {pattern} 的结果：")

        # 展示 DP 方案的分位数和平均值
        if dp_makespan:
            dp_percentiles = np.percentile(dp_makespan, percentiles)
            dp_mean = np.mean(dp_makespan)
            output_file.write("\nDP 方案的分位数和平均值：\n")
            print("\nDP 方案的分位数和平均值：")
            for p, val in zip(percentiles, dp_percentiles):
                output_file.write(f"{p} 分位数: {val:.2f}\n")
                print(f"{p} 分位数: {val:.2f}")
            output_file.write(f"平均值: {dp_mean:.2f}\n")
            print(f"平均值: {dp_mean:.2f}")
        else:
            output_file.write("\n没有找到包含 'dp' 的方案 Makespan 数据\n")
            print("\n没有找到包含 'dp' 的方案 Makespan 数据")
            continue

        # 计算 DP 方案相对于其他方案的提升百分比
        output_file.write("\nDP 方案相对于其他方案的提升百分比（分位数和平均值）：\n")
        print("\nDP 方案相对于其他方案的提升百分比（分位数和平均值）：")
        
        for file, makespan_values in all_makespan_dict.items():
            if makespan_values and 'dp' not in file:
                # 计算当前方案的分位数和平均值
                scheme_percentiles = np.percentile(makespan_values, percentiles)
                scheme_mean = np.mean(makespan_values)

                output_file.write(f"\n方案 {file} 的分位数和平均值：\n")
                print(f"\n方案 {file} 的分位数和平均值：")
                for p, val in zip(percentiles, scheme_percentiles):
                    output_file.write(f"{p} 分位数: {val:.2f}\n")
                    print(f"{p} 分位数: {val:.2f}")
                output_file.write(f"平均值: {scheme_mean:.2f}\n")
                print(f"平均值: {scheme_mean:.2f}")

                # 计算 DP 方案相对于当前方案的时延降低百分比
                for p, scheme_val in zip(percentiles, scheme_percentiles):
                    dp_val = dp_percentiles[percentiles.index(p)]
                    improvement = (scheme_val - dp_val) / scheme_val * 100
                    output_file.write(f"{p} 分位数的时延降低为 {improvement:.2f}%\n")
                    print(f"{p} 分位数的时延降低为 {improvement:.2f}%")
                
                # 计算平均值的时延降低
                mean_improvement = (scheme_mean - dp_mean) / scheme_mean * 100
                output_file.write(f"平均值的时延降低为 {mean_improvement:.2f}%\n")
                print(f"平均值的时延降低为 {mean_improvement:.2f}%")

        # 计算 DP 方案相对于所有方案的整体提升
        if all_other_makespan:
            all_other_percentiles = np.percentile(all_other_makespan, percentiles)
            all_other_mean = np.mean(all_other_makespan)

            output_file.write(f"\n所有方案的整体分位数和平均值：\n")
            print(f"\n所有方案的整体分位数和平均值：")
            for p, val in zip(percentiles, all_other_percentiles):
                output_file.write(f"{p} 分位数: {val:.2f}\n")
                print(f"{p} 分位数: {val:.2f}")
            output_file.write(f"平均值: {all_other_mean:.2f}\n")
            print(f"平均值: {all_other_mean:.2f}")

            # 计算 DP 方案相对于所有方案的提升
            for p, all_val in zip(percentiles, all_other_percentiles):
                dp_val = dp_percentiles[percentiles.index(p)]
                overall_improvement = (all_val - dp_val) / all_val * 100
                output_file.write(f"{p} 分位数的整体时延降低为 {overall_improvement:.2f}%\n")
                print(f"{p} 分位数的整体时延降低为 {overall_improvement:.2f}%")

            overall_mean_improvement = (all_other_mean - dp_mean) / all_other_mean * 100
            output_file.write(f"平均值的整体时延降低为 {overall_mean_improvement:.2f}%\n")
            print(f"平均值的整体时延降低为 {overall_mean_improvement:.2f}%")

print(f"结果已保存到 {output_file_path}")
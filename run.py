import subprocess
import os

# 定义命令及其参数
executable = './src/floyd'
input_file = '/Users/duling/Desktop/code/Geo_All2All/dataset/delay_matrix.txt'
output_file = '/Users/duling/Desktop/code/Geo_All2All/dataset/new_delay_matrix.txt'

# 检查可执行文件是否存在
if not os.path.exists(executable):
    print(f"Error: The executable {executable} does not exist.")
    exit(1)

# 构造完整命令
command = [executable, input_file, output_file]

try:
    # 使用 subprocess.run 来运行命令
    result = subprocess.run(command, capture_output=True, text=True)

    # 打印标准输出
    if result.stdout:
        print(result.stdout)

    # 打印标准错误
    if result.stderr:
        print(f"Error: {result.stderr}")

    print(f"Shortest path matrix has been saved to {output_file}")

except Exception as e:
    print(f"An error occurred while running the command: {e}")

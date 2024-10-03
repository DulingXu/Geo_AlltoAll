# 指定编译器
CC=/usr/bin/g++

# 编译标志
CFLAGS=-std=c++11 -Wall

# 目标
TARGET=compute_group_total_delay

# 源文件
SRCS=$(wildcard src/*.cpp)  # 自动获取 src 目录下的所有 .cpp 文件

# 包含目录
INCLUDES=-Iinclude

# 构建目标
$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(INCLUDES) $(SRCS) -o $(TARGET)

# 清理目标
clean:
	rm -rf $(TARGET)  # 只清理可执行文件

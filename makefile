# 只编译compute

# 指定编译器
CC=/usr/bin/g++

# 编译标志
CFLAGS=-std=c++11 -Wall

# 目标
TARGET=compute_group_total_delay

# 源文件
SRCS=src/compute_group_total_delay.cpp

# 包含目录
INCLUDES=-Iinclude

# 构建目标
$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(INCLUDES) $(SRCS) -o $(TARGET)

# 清理目标
clean:
	rm -rf *.o $(TARGET)





# # 指定编译器
# CC=/usr/bin/g++

# # 编译标志
# CFLAGS=-std=c++11 -Wall

# # 目标
# TARGETS=compute_group_total_delay single_all_to_all

# # 源文件
# SRCS1=src/compute_group_total_delay.cpp
# SRCS2=src/single_all_to_all.cpp

# # 包含目录
# INCLUDES=-Iinclude

# # 构建目标
# all: $(TARGETS)

# compute_group_total_delay: $(SRCS1)
# 	$(CC) $(CFLAGS) $(INCLUDES) $(SRCS1) -o compute_group_total_delay

# single_all_to_all: $(SRCS2)
# 	$(CC) $(CFLAGS) $(INCLUDES) $(SRCS2) -o single_all_to_all

# # 清理目标
# clean:
# 	rm -rf *.o $(TARGETS)




# # 指定编译器
# CC=/usr/bin/g++

# # 编译标志
# CFLAGS=-std=c++11 -Wall

# # 目标
# TARGET=compute_group_total_delay

# # 源文件
# SRCS=src/compute_group_total_delay.cpp src/single_all_to_all.cpp

# # 包含目录
# INCLUDES=-Iinclude

# # 构建目标
# $(TARGET): $(SRCS)
# 	$(CC) $(CFLAGS) $(INCLUDES) $(SRCS) -o $(TARGET)

# # 清理目标
# clean:
# 	rm -rf *.o $(TARGET)







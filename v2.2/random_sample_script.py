#!/usr/bin/env python3
"""
脚本用于从两个JSON文件中随机选择指定数量的数据项，并生成新的文件
从 addata-safe-v2.json 和 addata-harmful-v2.json 中分别等量随机选择 5、10、25、50 个项目
生成的文件：
- sampled_data_5.json (10项: 5个safe + 5个harmful)
- sampled_data_10.json (20项: 10个safe + 10个harmful)
- sampled_data_25.json (50项: 25个safe + 25个harmful)
- sampled_data_50.json (100项: 50个safe + 50个harmful)
"""

import json
import random
import os
from pathlib import Path

def load_json_file(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载文件 {file_path} 时出错: {e}")
        return None

def save_json_file(data, file_path):
    """保存JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"成功保存文件: {file_path} (包含 {len(data)} 个项目)")
    except Exception as e:
        print(f"保存文件 {file_path} 时出错: {e}")

def random_sample(data, n):
    """从数据中随机选择n个项目"""
    if len(data) < n:
        print(f"警告: 数据总数 ({len(data)}) 少于请求的样本数 ({n})")
        return data
    return random.sample(data, n)

def main():
    # 设置文件路径
    base_dir = Path(__file__).parent
    safe_file = base_dir / "addata-safe-v2.json"
    harmful_file = base_dir / "addata-harmful-v2.json"
    
    # 检查文件是否存在
    if not safe_file.exists():
        print(f"错误: 文件不存在 {safe_file}")
        return
    if not harmful_file.exists():
        print(f"错误: 文件不存在 {harmful_file}")
        return
    
    # 加载数据
    print("正在加载数据文件...")
    safe_data = load_json_file(safe_file)
    harmful_data = load_json_file(harmful_file)
    
    if safe_data is None or harmful_data is None:
        print("加载数据失败，退出程序")
        return
    
    print(f"安全数据项目数: {len(safe_data)}")
    print(f"有害数据项目数: {len(harmful_data)}")
    
    # 设置随机种子以确保结果可重现
    random.seed(42)
    
    # 定义要采样的数量
    sample_sizes = [5, 10, 25, 50]
    
    for size in sample_sizes:
        print(f"\n正在处理 {size} 个样本...")
        
        # 随机选择指定数量的safe和harmful数据
        selected_safe = random_sample(safe_data, size)
        selected_harmful = random_sample(harmful_data, size)
        
        # 合并数据
        combined_data = selected_safe + selected_harmful
        
        # 打乱合并后的数据顺序
        random.shuffle(combined_data)
        
        # 保存到文件
        output_file = base_dir / f"sampled_data_{size}.json"
        save_json_file(combined_data, output_file)
        
        # 打印统计信息
        safe_count = sum(1 for item in combined_data if 'intent: safe' in item.get('output', ''))
        harmful_count = sum(1 for item in combined_data if 'intent: harmful' in item.get('output', ''))
        print(f"  - 安全项目: {safe_count}")
        print(f"  - 有害项目: {harmful_count}")
        print(f"  - 总计: {len(combined_data)}")
    
    print("\n所有文件已生成完成！")
    
    # 显示生成的文件列表
    print("\n生成的文件:")
    for size in sample_sizes:
        output_file = base_dir / f"sampled_data_{size}.json"
        if output_file.exists():
            print(f"  - {output_file.name}")

if __name__ == "__main__":
    main()

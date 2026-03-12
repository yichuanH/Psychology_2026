#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
處理加分名單
"""

import pandas as pd
import json

def process_bonus_list():
    # 讀取 0303 加分名單（從新路徑）
    bonus_0303 = []
    with open('0303/0303_add.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    bonus_0303.append({
                        '姓名': parts[0],
                        '學號': parts[2]
                    })

    # 讀取 0310 加分名單（從新路徑）
    df_0310_add = pd.read_excel('0310/0310_add.xlsx')
    bonus_0310 = []
    for _, row in df_0310_add.iterrows():
        if pd.notna(row['姓名']) and pd.notna(row['學號']):
            bonus_0310.append({
                '姓名': row['姓名'],
                '學號': str(int(row['學號'])) if isinstance(row['學號'], float) else str(row['學號'])
            })

    # 整合加分資料
    bonus_data = {
        '0303': bonus_0303,
        '0310': bonus_0310
    }

    # 儲存為 JSON
    with open('bonus_data.json', 'w', encoding='utf-8') as f:
        json.dump(bonus_data, f, ensure_ascii=False, indent=2)

    print("✅ 加分名單處理完成！")
    print(f"📊 0303 加分人數: {len(bonus_0303)}")
    print(f"📊 0310 加分人數: {len(bonus_0310)}")

    # 顯示名單
    print("\n=== 0303 加分名單 ===")
    for i, student in enumerate(bonus_0303, 1):
        print(f"{i}. {student['姓名']} ({student['學號']})")

    print("\n=== 0310 加分名單 ===")
    for i, student in enumerate(bonus_0310, 1):
        print(f"{i}. {student['姓名']} ({student['學號']})")

    return bonus_data

if __name__ == '__main__':
    process_bonus_list()

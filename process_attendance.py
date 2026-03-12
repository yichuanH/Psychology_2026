#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
藝術心理學課程出缺席記錄處理腳本
"""

import pandas as pd
import json

def process_attendance():
    # 讀取成員名單
    df_member = pd.read_excel('member.xlsx')

    # 讀取出席記錄（從新路徑）
    df_0303 = pd.read_excel('0303/0303.xlsx')
    df_0310 = pd.read_excel('0310/0310.xlsx')

    # 讀取請假名單
    leave_0303 = []
    try:
        with open('0303/0303_leave.txt', 'r', encoding='utf-8') as f:
            for line in f:
                name = line.strip()
                if name:
                    leave_0303.append(name)
    except FileNotFoundError:
        print("⚠️  0303_leave.txt 不存在，跳過請假名單")

    print(f"📋 0303 請假名單: {leave_0303}")

    # 建立出缺席統計表
    attendance_data = []

    # 排除教授與助教
    exclude_names = ['陳一平', '黃怡川']

    for _, member in df_member.iterrows():
        name = member['姓名']
        student_id = str(member['帳號'])
        group = member['分組'] if pd.notna(member['分組']) else '未分組'

        # 跳過教授與助教
        if name in exclude_names:
            continue

        # 檢查 0303 出席（僅 A 組/第一組）
        if group == '第一組':
            attended_0303 = name in df_0303['姓名'].values or student_id in df_0303['學號'].astype(str).values

            # 檢查是否請假
            if name in leave_0303:
                status_0303 = '🏥 請假'
            elif attended_0303:
                status_0303 = '✓ 出席'
            else:
                status_0303 = '✗ 缺席'
        else:
            status_0303 = '— 無需出席'

        # 檢查 0310 出席（全員）
        attended_0310 = name in df_0310['姓名'].values or student_id in df_0310['學號'].astype(str).values
        status_0310 = '✓ 出席' if attended_0310 else '✗ 缺席'

        attendance_data.append({
            '姓名': name,
            '學號': student_id,
            '分組': group,
            '2026-03-03': status_0303,
            '2026-03-10': status_0310
        })

    # 建立 DataFrame
    df_attendance = pd.DataFrame(attendance_data)

    # 儲存為 Excel
    df_attendance.to_excel('attendance_record.xlsx', index=False)

    # 轉換為 JSON 供網頁使用
    attendance_json = df_attendance.to_dict(orient='records')
    with open('attendance_data.json', 'w', encoding='utf-8') as f:
        json.dump(attendance_json, f, ensure_ascii=False, indent=2)

    print("✅ 出缺席記錄處理完成！")
    print(f"📊 總共處理 {len(df_attendance)} 位成員")
    print("\n生成檔案：")
    print("  - attendance_record.xlsx (Excel 格式)")
    print("  - attendance_data.json (JSON 格式供網頁使用)")

    # 統計資訊
    count_0303_present = df_attendance[df_attendance['2026-03-03'] == '✓ 出席'].shape[0]
    count_0303_absent = df_attendance[df_attendance['2026-03-03'] == '✗ 缺席'].shape[0]
    count_0303_leave = df_attendance[df_attendance['2026-03-03'] == '🏥 請假'].shape[0]
    count_0310_present = df_attendance[df_attendance['2026-03-10'] == '✓ 出席'].shape[0]
    count_0310_absent = df_attendance[df_attendance['2026-03-10'] == '✗ 缺席'].shape[0]

    print(f"\n📊 0303 統計：出席 {count_0303_present} | 缺席 {count_0303_absent} | 請假 {count_0303_leave}")
    print(f"📊 0310 統計：出席 {count_0310_present} | 缺席 {count_0310_absent}")

    return df_attendance

if __name__ == '__main__':
    process_attendance()

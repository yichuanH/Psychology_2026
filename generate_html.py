#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成包含嵌入資料的 HTML
"""

import json

# 讀取出席資料
with open('attendance_data.json', 'r', encoding='utf-8') as f:
    attendance_data = json.load(f)

# 讀取加分資料
with open('bonus_data.json', 'r', encoding='utf-8') as f:
    bonus_data = json.load(f)

# 修正 NaN 值
for record in attendance_data:
    if record['分組'] is None or (isinstance(record['分組'], float) and str(record['分組']) == 'nan'):
        record['分組'] = '未分組'

# 將資料轉換為 JavaScript 格式
json_data_str = json.dumps(attendance_data, ensure_ascii=False, indent=8)
bonus_data_str = json.dumps(bonus_data, ensure_ascii=False, indent=8)

# HTML 模板
html_template = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>藝術心理學課程</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Microsoft JhengHei', 'PingFang TC', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            color: white;
            padding: 40px 0;
            animation: fadeIn 1s ease;
        }}

        header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        header p {{
            font-size: 1.3em;
            opacity: 0.95;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* 導航卡片 */
        .nav-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 30px;
            margin-bottom: 40px;
        }}

        .nav-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            animation: slideUp 0.6s ease forwards;
            opacity: 0;
        }}

        .nav-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .nav-card:nth-child(2) {{ animation-delay: 0.2s; }}
        .nav-card:nth-child(3) {{ animation-delay: 0.3s; }}
        .nav-card:nth-child(4) {{ animation-delay: 0.4s; }}

        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .nav-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }}

        .nav-card-icon {{
            font-size: 4em;
            margin-bottom: 15px;
        }}

        .nav-card h2 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 1.8em;
        }}

        .nav-card p {{
            color: #666;
            font-size: 1.1em;
        }}

        .nav-card a {{
            text-decoration: none;
            color: inherit;
            display: block;
        }}

        /* 出缺席記錄區 */
        .attendance-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-top: 30px;
            display: none;
        }}

        .attendance-section.active {{
            display: block;
            animation: fadeIn 0.5s ease;
        }}

        .attendance-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #667eea;
        }}

        .attendance-header h2 {{
            color: #333;
            font-size: 2em;
        }}

        .close-btn {{
            background: #e74c3c;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: background 0.3s ease;
        }}

        .close-btn:hover {{
            background: #c0392b;
        }}

        /* 搜尋框 */
        .search-box {{
            width: 100%;
            padding: 12px 20px;
            font-size: 1.1em;
            border: 2px solid #667eea;
            border-radius: 10px;
            margin-bottom: 20px;
            font-family: 'Microsoft JhengHei', 'PingFang TC', sans-serif;
        }}

        .search-box:focus {{
            outline: none;
            border-color: #764ba2;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        }}

        /* 出席表格 */
        .attendance-table-container {{
            max-height: 600px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}

        .attendance-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .attendance-table thead {{
            position: sticky;
            top: 0;
            background: #667eea;
            z-index: 10;
        }}

        .attendance-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-size: 1.1em;
        }}

        .attendance-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}

        .attendance-table tbody tr:hover {{
            background: #f8f9fa;
        }}

        .status-present {{
            color: #27ae60;
            font-weight: bold;
        }}

        .status-absent {{
            color: #e74c3c;
            font-weight: bold;
        }}

        .status-na {{
            color: #95a5a6;
        }}

        .status-leave {{
            color: #3498db;
            font-weight: bold;
        }}

        .bonus-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #f39c12, #e67e22);
            color: white;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.8em;
            margin-left: 5px;
            font-weight: bold;
        }}

        .bonus-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-top: 30px;
            display: none;
        }}

        .bonus-section.active {{
            display: block;
            animation: fadeIn 0.5s ease;
        }}

        .bonus-lists {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .bonus-list {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #f39c12;
        }}

        .bonus-list h3 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}

        .bonus-list ul {{
            list-style: none;
        }}

        .bonus-list li {{
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
        }}

        .bonus-list li:last-child {{
            border-bottom: none;
        }}

        .stats-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}

        .stat-card h3 {{
            font-size: 2.5em;
            margin-bottom: 5px;
        }}

        .stat-card p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        footer {{
            text-align: center;
            color: white;
            padding: 40px 0 20px;
            margin-top: 40px;
        }}

        /* 響應式設計 */
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 2em;
            }}

            .nav-card h2 {{
                font-size: 1.5em;
            }}

            .attendance-table {{
                font-size: 0.9em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎨 藝術心理學</h1>
            <p>Art Psychology Course - 2026 Spring</p>
        </header>

        <!-- 主要導航 -->
        <div class="nav-section">
            <div class="nav-card" onclick="showAttendance()">
                <div class="nav-card-icon">📋</div>
                <h2>出缺席記錄</h2>
                <p>查看課程出席狀況</p>
            </div>

            <div class="nav-card" onclick="showBonus()">
                <div class="nav-card-icon">⭐</div>
                <h2>加分名單</h2>
                <p>課堂參與加分紀錄</p>
            </div>

            <div class="nav-card">
                <a href="https://drive.google.com/drive/u/0/folders/10UBmw3oAEy0lXtVCms4unrCSMdO0O8dM" target="_blank">
                    <div class="nav-card-icon">📝</div>
                    <h2>課程小結繳交</h2>
                    <p>上傳您的課程心得</p>
                </a>
            </div>

            <div class="nav-card">
                <a href="https://www.youtube.com/@yichuanh1314" target="_blank">
                    <div class="nav-card-icon">🎥</div>
                    <h2>課程影片頻道</h2>
                    <p>觀看課程錄影</p>
                </a>
            </div>
        </div>

        <!-- 出缺席記錄區域 -->
        <div class="attendance-section" id="attendanceSection">
            <div class="attendance-header">
                <h2>📊 出缺席記錄</h2>
                <button class="close-btn" onclick="hideAttendance()">關閉</button>
            </div>

            <!-- 統計資訊 -->
            <div class="stats-section">
                <div class="stat-card">
                    <h3 id="totalStudents">0</h3>
                    <p>總修課人數</p>
                </div>
                <div class="stat-card">
                    <h3 id="attendance0303">0</h3>
                    <p>3/3 出席人數</p>
                </div>
                <div class="stat-card">
                    <h3 id="attendance0310">0</h3>
                    <p>3/10 出席人數</p>
                </div>
            </div>

            <!-- 搜尋框 -->
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 搜尋姓名或學號...">

            <!-- 出席表格 -->
            <div class="attendance-table-container">
                <table class="attendance-table">
                    <thead>
                        <tr>
                            <th>姓名</th>
                            <th>學號</th>
                            <th>分組</th>
                            <th>2026-03-03 (第一組)</th>
                            <th>2026-03-10 (全員)</th>
                        </tr>
                    </thead>
                    <tbody id="attendanceTableBody">
                        <!-- 資料將透過 JavaScript 動態載入 -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 加分名單區域 -->
        <div class="bonus-section" id="bonusSection">
            <div class="attendance-header">
                <h2>⭐ 課堂參與加分名單</h2>
                <button class="close-btn" onclick="hideBonus()">關閉</button>
            </div>

            <div class="bonus-lists">
                <div class="bonus-list">
                    <h3>📅 2026-03-03 加分名單</h3>
                    <ul id="bonus0303List">
                        <!-- 將透過 JavaScript 動態載入 -->
                    </ul>
                </div>

                <div class="bonus-list">
                    <h3>📅 2026-03-10 加分名單</h3>
                    <ul id="bonus0310List">
                        <!-- 將透過 JavaScript 動態載入 -->
                    </ul>
                </div>
            </div>
        </div>

        <footer>
            <p>© 2026 藝術心理學課程 | 陽明交通大學</p>
        </footer>
    </div>

    <script>
        // 出席資料（直接嵌入）
        const attendanceData = {json_data_str};

        // 加分資料（直接嵌入）
        const bonusData = {bonus_data_str};

        // 檢查學生是否有加分
        function hasBonus(studentId, date) {{
            const dateKey = date === '2026-03-03' ? '0303' : '0310';
            return bonusData[dateKey] && bonusData[dateKey].some(s => s['學號'] === studentId);
        }}

        // 渲染出席表格
        function renderAttendanceTable(data) {{
            const tbody = document.getElementById('attendanceTableBody');
            tbody.innerHTML = '';

            data.forEach(record => {{
                const row = document.createElement('tr');

                // 判斷 0303 狀態樣式
                let status0303Class = 'status-na';
                if (record['2026-03-03'].includes('✓')) {{
                    status0303Class = 'status-present';
                }} else if (record['2026-03-03'].includes('✗')) {{
                    status0303Class = 'status-absent';
                }} else if (record['2026-03-03'].includes('🏥')) {{
                    status0303Class = 'status-leave';
                }}

                const status0310Class = record['2026-03-10'].includes('✓') ? 'status-present' : 'status-absent';

                // 檢查是否有加分
                const bonus0303 = hasBonus(record['學號'], '2026-03-03') ? '<span class="bonus-badge">⭐ 加分</span>' : '';
                const bonus0310 = hasBonus(record['學號'], '2026-03-10') ? '<span class="bonus-badge">⭐ 加分</span>' : '';

                row.innerHTML = `
                    <td>${{record['姓名']}}</td>
                    <td>${{record['學號']}}</td>
                    <td>${{record['分組']}}</td>
                    <td class="${{status0303Class}}">${{record['2026-03-03']}}${{bonus0303}}</td>
                    <td class="${{status0310Class}}">${{record['2026-03-10']}}${{bonus0310}}</td>
                `;

                tbody.appendChild(row);
            }});
        }}

        // 更新統計資訊
        function updateStats(data) {{
            document.getElementById('totalStudents').textContent = data.length;

            const attendance0303 = data.filter(r => r['2026-03-03'].includes('✓')).length;
            const attendance0310 = data.filter(r => r['2026-03-10'].includes('✓')).length;

            document.getElementById('attendance0303').textContent = attendance0303;
            document.getElementById('attendance0310').textContent = attendance0310;
        }}

        // 搜尋功能
        document.addEventListener('DOMContentLoaded', function() {{
            const searchBox = document.getElementById('searchBox');
            if (searchBox) {{
                searchBox.addEventListener('input', function() {{
                    const searchTerm = this.value.toLowerCase();
                    const filteredData = attendanceData.filter(record =>
                        record['姓名'].toLowerCase().includes(searchTerm) ||
                        record['學號'].toLowerCase().includes(searchTerm) ||
                        record['分組'].toLowerCase().includes(searchTerm)
                    );
                    renderAttendanceTable(filteredData);
                }});
            }}
        }});

        // 隱藏所有頁面
        function hideAllSections() {{
            document.getElementById('attendanceSection').classList.remove('active');
            document.getElementById('bonusSection').classList.remove('active');
        }}

        // 顯示出席記錄
        function showAttendance() {{
            hideAllSections();
            document.getElementById('attendanceSection').classList.add('active');
            renderAttendanceTable(attendanceData);
            updateStats(attendanceData);
        }}

        // 隱藏出席記錄
        function hideAttendance() {{
            hideAllSections();
        }}

        // 渲染加分名單
        function renderBonusLists() {{
            const list0303 = document.getElementById('bonus0303List');
            const list0310 = document.getElementById('bonus0310List');

            list0303.innerHTML = '';
            list0310.innerHTML = '';

            bonusData['0303'].forEach((student, index) => {{
                const li = document.createElement('li');
                li.textContent = `${{index + 1}}. ${{student['姓名']}} (${{student['學號']}})`;
                list0303.appendChild(li);
            }});

            bonusData['0310'].forEach((student, index) => {{
                const li = document.createElement('li');
                li.textContent = `${{index + 1}}. ${{student['姓名']}} (${{student['學號']}})`;
                list0310.appendChild(li);
            }});
        }}

        // 顯示加分名單
        function showBonus() {{
            hideAllSections();
            document.getElementById('bonusSection').classList.add('active');
            renderBonusLists();
        }}

        // 隱藏加分名單
        function hideBonus() {{
            hideAllSections();
        }}
    </script>
</body>
</html>'''

# 儲存 HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✅ HTML 已生成完成！")
print(f"📊 包含 {len(attendance_data)} 筆出席記錄")

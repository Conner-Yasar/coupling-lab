# 南京气温数据可视化
# ─── 必须在 import matplotlib.pyplot 之前设置后端 ────────────────────
import matplotlib
matplotlib.use('Agg')   # 非交互后端，终端运行不阻塞

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import re
from matplotlib import rcParams
from matplotlib.patches import Patch

# ─── 字体配置（支持中文显示）───────────────────────────────────────────
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'PingFang SC', 'sans-serif']
rcParams['axes.unicode_minus'] = False

# ════════════════════════════════════════════════════════════════════════
# 1. 读取数据
# ════════════════════════════════════════════════════════════════════════
df_raw = pd.read_csv(
    r'd:\document\files\python大作业\南京2023年5月到2026年2月天气情况.csv',
    encoding='gb18030'
)
print(f"读取成功，共 {len(df_raw)} 条记录")

if df_raw.empty:
    print("错误：CSV 文件为空，无法继续。")
    exit()

# ════════════════════════════════════════════════════════════════════════
# 2. 解析日期
#    实际格式示例: '2023年05月01日'
# ════════════════════════════════════════════════════════════════════════
df_raw['日期'] = pd.to_datetime(df_raw['日期'].astype(str).str.strip(), format='%Y年%m月%d日', errors='coerce')
df = df_raw.dropna(subset=['日期']).sort_values('日期').reset_index(drop=True)

n_invalid = len(df_raw) - len(df)
if n_invalid > 0:
    print(f"⚠ {n_invalid} 行日期解析失败或格式不正确，已丢弃")

if df.empty:
    print("错误：日期解析后未提取到有效数据，请检查日期格式。")
    exit()

# ════════════════════════════════════════════════════════════════════════
# 3. 解析气温字段
#    实际格式示例：'多云28℃'  '晴35℃'  '小雨-3℃'
#    策略：提取所有整数，若仅有1个则视为日气温，若有2个则视为高低温
# ════════════════════════════════════════════════════════════════════════
def parse_temp(s):
    if pd.isna(s):
        return np.nan, np.nan
    nums = re.findall(r'-?\d+', str(s))
    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    elif len(nums) == 1:
        v = float(nums[0])
        return v, v
    return np.nan, np.nan

# 先计算解析结果再赋值，避免空数据时的 ValueError
temp_parsed = df['气温'].apply(parse_temp).apply(pd.Series)
df[['最高气温', '最低气温']] = temp_parsed

df = df.dropna(subset=['最高气温']).reset_index(drop=True)
df['平均气温'] = (df['最高气温'] + df['最低气温']) / 2

print(f"有效数据：{len(df)} 条，时间范围：{df['日期'].min().date()} ~ {df['日期'].max().date()}")

# 衍生列
df['年月'] = df['日期'].dt.to_period('M')
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

# ════════════════════════════════════════════════════════════════════════
# 全局样式与工具
# ════════════════════════════════════════════════════════════════════════
BG_COLOR    = '#0f1117'
PANEL_COLOR = '#1a1d2e'
HIGH_COLOR  = '#ff6b6b'
LOW_COLOR   = '#4ecdc4'
AVG_COLOR   = '#ffd93d'
GRID_COLOR  = '#2a2d3e'
TEXT_COLOR  = '#e0e0e0'

def style_ax(ax):
    ax.set_facecolor(PANEL_COLOR)
    ax.tick_params(colors=TEXT_COLOR)
    ax.spines[:].set_color(GRID_COLOR)
    ax.grid(color=GRID_COLOR, linewidth=0.5, alpha=0.7)

# ════════════════════════════════════════════════════════════════════════
# 图表 1：逐日气温折线图
# ════════════════════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(18, 7), facecolor=BG_COLOR)
style_ax(ax1)

dates = df['日期']
has_range = (df['最高气温'] != df['最低气温']).any()

if has_range:
    ax1.fill_between(dates, df['最低气温'], df['最高气温'], alpha=0.2, color=HIGH_COLOR, label='高低温区间')
    ax1.plot(dates, df['最高气温'], color=HIGH_COLOR, linewidth=1.0, alpha=0.85, label='最高气温')
    ax1.plot(dates, df['最低气温'], color=LOW_COLOR, linewidth=1.0, alpha=0.85, label='最低气温')
else:
    ax1.plot(dates, df['最高气温'], color=AVG_COLOR, linewidth=1.5, label='气温')

ax1.plot(dates, df['平均气温'], color=AVG_COLOR, linewidth=1.5, linestyle='--', alpha=0.9, label='日均温')
ax1.axhline(0, color='#888888', linewidth=0.8, linestyle=':')

ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right', color=TEXT_COLOR, fontsize=9)

ax1.set_title('南京逐日气温变化趋势', color=TEXT_COLOR, fontsize=16, fontweight='bold', pad=14)
ax1.set_xlabel('日期', color=TEXT_COLOR, fontsize=11)
ax1.set_ylabel('气温 (℃)', color=TEXT_COLOR, fontsize=11)
ax1.legend(loc='upper right', framealpha=0.3, facecolor=PANEL_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

plt.tight_layout()
plt.savefig(r'd:\document\files\python大作业\气温折线图.png', dpi=150, facecolor=BG_COLOR)
print("✔ 已保存：气温折线图.png")
plt.close(fig1)

# ════════════════════════════════════════════════════════════════════════
# 图表 2：月度气温箱线图
# ════════════════════════════════════════════════════════════════════════
months_sorted = sorted(df['年月'].unique())
fig2, ax2 = plt.subplots(figsize=(18, 7), facecolor=BG_COLOR)
style_ax(ax2)
x = np.arange(len(months_sorted))

if has_range:
    high_data = [df[df['年月'] == m]['最高气温'].values for m in months_sorted]
    low_data  = [df[df['年月'] == m]['最低气温'].values for m in months_sorted]
    ax2.boxplot(high_data, positions=x - 0.2, widths=0.3, patch_artist=True,
                boxprops=dict(facecolor=HIGH_COLOR, alpha=0.5), medianprops=dict(color='white'))
    ax2.boxplot(low_data, positions=x + 0.2, widths=0.3, patch_artist=True,
                boxprops=dict(facecolor=LOW_COLOR, alpha=0.5), medianprops=dict(color='white'))
    legend_handles = [Patch(facecolor=HIGH_COLOR, alpha=0.7, label='最高气温分布'),
                      Patch(facecolor=LOW_COLOR, alpha=0.7, label='最低气温分布')]
else:
    temp_data = [df[df['年月'] == m]['平均气温'].values for m in months_sorted]
    ax2.boxplot(temp_data, positions=x, widths=0.5, patch_artist=True,
                boxprops=dict(facecolor=AVG_COLOR, alpha=0.5), medianprops=dict(color='white'))
    legend_handles = [Patch(facecolor=AVG_COLOR, alpha=0.7, label='气温分布')]

ax2.set_xticks(x)
ax2.set_xticklabels([str(m) for m in months_sorted], rotation=45, ha='right', color=TEXT_COLOR)
ax2.set_title('南京月度气温区间分布', color=TEXT_COLOR, fontsize=15, fontweight='bold')
ax2.legend(handles=legend_handles, labelcolor=TEXT_COLOR, facecolor=PANEL_COLOR)

plt.tight_layout()
plt.savefig(r'd:\document\files\python大作业\月度气温箱线图.png', dpi=150, facecolor=BG_COLOR)
print("✔ 已保存：月度气温箱线图.png")
plt.close(fig2)

# ════════════════════════════════════════════════════════════════════════
# 图表 3：热力图
# ════════════════════════════════════════════════════════════════════════
pivot = df.pivot_table(values='平均气温', index='年份', columns='月份', aggfunc='mean')
pivot = pivot.reindex(columns=range(1, 13))

fig3, ax3 = plt.subplots(figsize=(14, 5), facecolor=BG_COLOR)
ax3.set_facecolor(BG_COLOR)
im = ax3.imshow(pivot.values, cmap='RdYlBu_r', aspect='auto')

for i in range(len(pivot.index)):
    for j in range(12):
        val = pivot.values[i, j]
        if not np.isnan(val):
            ax3.text(j, i, f'{val:.1f}', ha='center', va='center', color='black', fontweight='bold')

ax3.set_xticks(range(12))
ax3.set_xticklabels([f'{m}月' for m in range(1, 13)], color=TEXT_COLOR)
ax3.set_yticks(range(len(pivot.index)))
ax3.set_yticklabels(pivot.index, color=TEXT_COLOR)
plt.colorbar(im, ax=ax3, label='平均气温 (℃)')
ax3.set_title('南京月均气温热力图', color=TEXT_COLOR, fontsize=15, fontweight='bold')

plt.tight_layout()
plt.savefig(r'd:\document\files\python大作业\月均气温热力图.png', dpi=150, facecolor=BG_COLOR)
print("✔ 已保存：月均气温热力图.png")
plt.close(fig3)

# ════════════════════════════════════════════════════════════════════════
# 统计摘要
# ════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 40)
print("  南京气温统计摘要")
print("═" * 40)
print(f"  最高气温：{df['最高气温'].max():.1f}℃ ({df.loc[df['最高气温'].idxmax(), '日期'].date()})")
print(f"  最低气温：{df['最低气温'].min():.1f}℃ ({df.loc[df['最低气温'].idxmin(), '日期'].date()})")
print(f"  总平均气温：{df['平均气温'].mean():.1f}℃")
print("═" * 40)
print("\n所有图表已生成完毕！")

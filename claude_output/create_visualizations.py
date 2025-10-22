"""
Fulfillio Q1 Operations - Time Series Visualizations
Senior Operations Analyst - Data Visualization Script
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime
import numpy as np

# Set style for professional appearance
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Read datasets
df_q1 = pd.read_csv('/Users/jonasvyshniauskas/Documents/getyourguide/thtsoa_dataset - Fulfillio Q1 Warehouse Operations.csv')
df_large = pd.read_csv('/Users/jonasvyshniauskas/Documents/getyourguide/thtsoa_dataset - Orders with _5 Items (Picking System Subset).csv')

# Clean column names
df_q1.columns = df_q1.columns.str.strip()
df_large.columns = df_large.columns.str.strip()

# Convert numeric columns (remove commas from numbers)
for col in df_q1.columns:
    if col != 'Month':
        df_q1[col] = df_q1[col].astype(str).str.replace(',', '').astype(float)

for col in df_large.columns:
    if col != 'Month':
        df_large[col] = df_large[col].astype(str).str.replace(',', '').astype(float)

# Create month mapping for x-axis
months = ['January', 'February', 'March']
month_nums = [1, 2, 3]

print("=" * 80)
print("GENERATING Q1 WAREHOUSE OPERATIONS VISUALIZATIONS")
print("=" * 80)

# ============================================================================
# GRAPH SET 1: Q1 WAREHOUSE OPERATIONS - COMPREHENSIVE TIME SERIES
# ============================================================================

fig1 = plt.figure(figsize=(16, 12))
fig1.suptitle('Case Study 1: Q1 Warehouse Operations - Time Series Analysis',
              fontsize=18, fontweight='bold', y=0.995)

# Graph 1.1: Volume & Processing Time
ax1 = plt.subplot(3, 2, 1)
ax1_twin = ax1.twinx()

line1 = ax1.plot(month_nums, df_q1['Orders Processed'],
                 marker='o', linewidth=2.5, markersize=8,
                 color='#2E86AB', label='Orders Processed')
line2 = ax1_twin.plot(month_nums, df_q1['Avg. Order Processing Time (min)'],
                      marker='s', linewidth=2.5, markersize=8,
                      color='#A23B72', label='Avg Processing Time')

ax1.set_xlabel('Month', fontsize=11, fontweight='bold')
ax1.set_ylabel('Orders Processed', fontsize=11, fontweight='bold', color='#2E86AB')
ax1_twin.set_ylabel('Processing Time (min)', fontsize=11, fontweight='bold', color='#A23B72')
ax1.set_title('Volume Growth vs. Processing Time', fontsize=13, fontweight='bold', pad=10)
ax1.set_xticks(month_nums)
ax1.set_xticklabels(months, rotation=0)
ax1.tick_params(axis='y', labelcolor='#2E86AB')
ax1_twin.tick_params(axis='y', labelcolor='#A23B72')
ax1.grid(True, alpha=0.3)

# Add combined legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', fontsize=9)

# Add growth annotations
ax1.annotate('+30%', xy=(3, df_q1['Orders Processed'].iloc[2]),
            xytext=(3.2, df_q1['Orders Processed'].iloc[2]-500),
            fontsize=10, fontweight='bold', color='#2E86AB',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#2E86AB'))

# Graph 1.2: Quality Metrics (Errors & Late Deliveries)
ax2 = plt.subplot(3, 2, 2)
width = 0.35
x = np.array(month_nums)

bars1 = ax2.bar(x - width/2, df_q1['Picking Errors'], width,
                label='Picking Errors', color='#E63946', alpha=0.8)
bars2 = ax2.bar(x + width/2, df_q1['Late Deliveries'], width,
                label='Late Deliveries', color='#F77F00', alpha=0.8)

ax2.set_xlabel('Month', fontsize=11, fontweight='bold')
ax2.set_ylabel('Number of Incidents', fontsize=11, fontweight='bold')
ax2.set_title('Quality Crisis: Errors & Late Deliveries', fontsize=13, fontweight='bold', pad=10)
ax2.set_xticks(month_nums)
ax2.set_xticklabels(months, rotation=0)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# Add crisis indicator
ax2.text(0.5, 0.95, '🚨 CRITICAL', transform=ax2.transAxes,
        fontsize=11, fontweight='bold', color='#E63946',
        ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#E63946', linewidth=2))

# Graph 1.3: Resource Strain Metrics
ax3 = plt.subplot(3, 2, 3)
ax3.plot(month_nums, df_q1['Overtime Hours'],
         marker='o', linewidth=2.5, markersize=8,
         color='#FB8500', label='Overtime Hours')
ax3.plot(month_nums, df_q1['Staff Absences'],
         marker='s', linewidth=2.5, markersize=8,
         color='#8338EC', label='Staff Absences')

ax3.set_xlabel('Month', fontsize=11, fontweight='bold')
ax3.set_ylabel('Hours / Days', fontsize=11, fontweight='bold')
ax3.set_title('Workforce Burnout Indicators', fontsize=13, fontweight='bold', pad=10)
ax3.set_xticks(month_nums)
ax3.set_xticklabels(months, rotation=0)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)

# Add trend annotations
ax3.annotate('+83%', xy=(3, df_q1['Overtime Hours'].iloc[2]),
            xytext=(2.5, df_q1['Overtime Hours'].iloc[2]+20),
            fontsize=10, fontweight='bold', color='#FB8500',
            arrowprops=dict(arrowstyle='->', color='#FB8500', lw=1.5))
ax3.annotate('+157%', xy=(3, df_q1['Staff Absences'].iloc[2]),
            xytext=(2.5, df_q1['Staff Absences'].iloc[2]-5),
            fontsize=10, fontweight='bold', color='#8338EC',
            arrowprops=dict(arrowstyle='->', color='#8338EC', lw=1.5))

# Graph 1.4: Normalized Efficiency Metrics (per 1000 orders)
ax4 = plt.subplot(3, 2, 4)

# Calculate efficiency metrics
errors_per_1k = (df_q1['Picking Errors'] / df_q1['Orders Processed']) * 1000
late_per_1k = (df_q1['Late Deliveries'] / df_q1['Orders Processed']) * 1000
overtime_per_order = (df_q1['Overtime Hours'] / df_q1['Orders Processed']) * 60  # in minutes

ax4.plot(month_nums, errors_per_1k,
         marker='o', linewidth=2.5, markersize=8,
         color='#E63946', label='Errors per 1K Orders')
ax4.plot(month_nums, late_per_1k,
         marker='s', linewidth=2.5, markersize=8,
         color='#F77F00', label='Late Deliveries per 1K')

ax4.set_xlabel('Month', fontsize=11, fontweight='bold')
ax4.set_ylabel('Incidents per 1,000 Orders', fontsize=11, fontweight='bold')
ax4.set_title('Efficiency Deterioration (Volume-Normalized)', fontsize=13, fontweight='bold', pad=10)
ax4.set_xticks(month_nums)
ax4.set_xticklabels(months, rotation=0)
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

# Graph 1.5: Growth Rate Comparison
ax5 = plt.subplot(3, 2, 5)

metrics = ['Orders\n(+30%)', 'Processing\nTime\n(+22%)', 'Picking\nErrors\n(+106%)',
           'Late\nDeliveries\n(+56%)', 'Overtime\n(+83%)', 'Absences\n(+157%)']
growth_rates = [30, 22, 106, 56, 83, 157]
colors = ['#2E86AB', '#A23B72', '#E63946', '#F77F00', '#FB8500', '#8338EC']

bars = ax5.bar(range(len(metrics)), growth_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax5.set_ylabel('Growth Rate (%)', fontsize=11, fontweight='bold')
ax5.set_title('Q1 Growth Rate Comparison: Volume vs. Quality/Resource Metrics',
              fontsize=13, fontweight='bold', pad=10)
ax5.set_xticks(range(len(metrics)))
ax5.set_xticklabels(metrics, fontsize=9)
ax5.axhline(y=30, color='#2E86AB', linestyle='--', linewidth=2, label='Volume Growth Baseline')
ax5.grid(True, alpha=0.3, axis='y')
ax5.legend(fontsize=9)

# Add value labels
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}%',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Add danger zone shading
ax5.axhspan(50, 160, alpha=0.1, color='red', label='Crisis Zone (>50%)')
ax5.text(0.98, 0.95, 'CRISIS ZONE', transform=ax5.transAxes,
        fontsize=11, fontweight='bold', color='#E63946',
        ha='right', va='top', rotation=0)

# Graph 1.6: Key Insight Summary
ax6 = plt.subplot(3, 2, 6)
ax6.axis('off')

insight_text = """
KEY INSIGHTS - Q1 WAREHOUSE OPERATIONS

🚨 QUALITY CRISIS
• Picking errors growing 3.5x faster than volume
• Late deliveries up 56% (not keeping pace with growth)
• Efficiency metrics deteriorating across all dimensions

⚠️ RESOURCE STRAIN
• Overtime costs growing 2.8x faster than revenue
• Staff absences up 157% - clear burnout signals
• Processing time per order increasing (+22%)

📊 SYSTEMIC ISSUES
• Not scaling efficiently - losing productivity gains
• Workforce capacity exhausted
• Quality collapse indicates structural problems

💡 SENIOR ANALYST RECOMMENDATION
Phase 1 (Immediate): Stabilize quality systems
Phase 2 (Month 2-3): Strategic hiring to replace overtime
Phase 3 (Q2): Technology investment for scale
"""

ax6.text(0.05, 0.95, insight_text, transform=ax6.transAxes,
        fontsize=10, verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=1', facecolor='#F8F9FA',
                 edgecolor='#2E86AB', linewidth=2))

plt.tight_layout()
plt.savefig('/Users/jonasvyshniauskas/Documents/getyourguide/claude_output/Q1_Warehouse_Operations_Analysis.png',
            dpi=300, bbox_inches='tight')
print("✓ Saved: Q1_Warehouse_Operations_Analysis.png")

# ============================================================================
# GRAPH SET 2: LARGE ORDERS (5+ ITEMS) ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("GENERATING LARGE ORDERS (5+ ITEMS) VISUALIZATIONS")
print("=" * 80)

fig2 = plt.figure(figsize=(16, 10))
fig2.suptitle('Case Study 1 Deep Dive: Large Orders (5+ Items) Crisis Analysis',
              fontsize=18, fontweight='bold', y=0.995)

# Graph 2.1: Large Order Volume Trend
ax7 = plt.subplot(2, 3, 1)
ax7.plot(month_nums, df_large['Orders >5 Items'],
         marker='o', linewidth=3, markersize=10,
         color='#06AED5', label='Large Orders')
ax7.fill_between(month_nums, 0, df_large['Orders >5 Items'], alpha=0.3, color='#06AED5')

ax7.set_xlabel('Month', fontsize=11, fontweight='bold')
ax7.set_ylabel('Number of Orders', fontsize=11, fontweight='bold')
ax7.set_title('Large Order Volume Growth', fontsize=13, fontweight='bold', pad=10)
ax7.set_xticks(month_nums)
ax7.set_xticklabels(months, rotation=0)
ax7.grid(True, alpha=0.3)

# Add growth annotation
growth_pct = ((df_large['Orders >5 Items'].iloc[2] - df_large['Orders >5 Items'].iloc[0]) /
              df_large['Orders >5 Items'].iloc[0] * 100)
ax7.text(0.5, 0.95, f'+{growth_pct:.1f}% Growth', transform=ax7.transAxes,
        fontsize=11, fontweight='bold', color='#06AED5',
        ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#06AED5', linewidth=2))

# Graph 2.2: Picking Errors on Large Orders
ax8 = plt.subplot(2, 3, 2)
bars = ax8.bar(month_nums, df_large['Picking Errors (Large Orders)'],
               color='#DC2F02', alpha=0.8, edgecolor='black', linewidth=2)

ax8.set_xlabel('Month', fontsize=11, fontweight='bold')
ax8.set_ylabel('Number of Errors', fontsize=11, fontweight='bold')
ax8.set_title('Picking Errors - Large Orders (CRITICAL)', fontsize=13, fontweight='bold', pad=10)
ax8.set_xticks(month_nums)
ax8.set_xticklabels(months, rotation=0)
ax8.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax8.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add crisis indicator
error_growth = ((df_large['Picking Errors (Large Orders)'].iloc[2] -
                df_large['Picking Errors (Large Orders)'].iloc[0]) /
                df_large['Picking Errors (Large Orders)'].iloc[0] * 100)
ax8.text(0.5, 0.95, f'🚨 +{error_growth:.1f}%', transform=ax8.transAxes,
        fontsize=12, fontweight='bold', color='white',
        ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#DC2F02', linewidth=0))

# Graph 2.3: Error Rate Escalation
ax9 = plt.subplot(2, 3, 3)
line = ax9.plot(month_nums, df_large['Error Rate (%)'],
                marker='o', linewidth=3, markersize=10,
                color='#DC2F02', label='Error Rate')
ax9.fill_between(month_nums, 0, df_large['Error Rate (%)'], alpha=0.3, color='#DC2F02')

ax9.set_xlabel('Month', fontsize=11, fontweight='bold')
ax9.set_ylabel('Error Rate (%)', fontsize=11, fontweight='bold')
ax9.set_title('Error Rate Deterioration - Large Orders', fontsize=13, fontweight='bold', pad=10)
ax9.set_xticks(month_nums)
ax9.set_xticklabels(months, rotation=0)
ax9.grid(True, alpha=0.3)

# Add threshold line
ax9.axhline(y=2.0, color='orange', linestyle='--', linewidth=2, label='Warning Threshold (2%)')
ax9.axhline(y=3.0, color='red', linestyle='--', linewidth=2, label='Critical Threshold (3%)')
ax9.legend(fontsize=9, loc='upper left')

# Add annotations for each point
for i, (x, y) in enumerate(zip(month_nums, df_large['Error Rate (%)'])):
    ax9.annotate(f'{y:.2f}%', xy=(x, y),
                xytext=(0, 10), textcoords='offset points',
                fontsize=10, fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#DC2F02'))

# Graph 2.4: Large Orders as % of Total Volume
ax10 = plt.subplot(2, 3, 4)

# Calculate percentage of total
pct_large = (df_large['Orders >5 Items'] / df_q1['Orders Processed']) * 100

bars = ax10.bar(month_nums, pct_large, color='#06AED5', alpha=0.8, edgecolor='black', linewidth=2)
ax10.set_xlabel('Month', fontsize=11, fontweight='bold')
ax10.set_ylabel('% of Total Orders', fontsize=11, fontweight='bold')
ax10.set_title('Large Orders as % of Total Volume', fontsize=13, fontweight='bold', pad=10)
ax10.set_xticks(month_nums)
ax10.set_xticklabels(months, rotation=0)
ax10.set_ylim(0, 12)
ax10.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, pct in zip(bars, pct_large):
    ax10.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{pct:.1f}%',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# Graph 2.5: Error Concentration Analysis
ax11 = plt.subplot(2, 3, 5)

# Calculate what % of total errors come from large orders
pct_errors_from_large = (df_large['Picking Errors (Large Orders)'] / df_q1['Picking Errors']) * 100

bars = ax11.bar(month_nums, pct_errors_from_large,
                color='#DC2F02', alpha=0.8, edgecolor='black', linewidth=2)
ax11.set_xlabel('Month', fontsize=11, fontweight='bold')
ax11.set_ylabel('% of Total Errors', fontsize=11, fontweight='bold')
ax11.set_title('Error Concentration: Large Orders', fontsize=13, fontweight='bold', pad=10)
ax11.set_xticks(month_nums)
ax11.set_xticklabels(months, rotation=0)
ax11.set_ylim(0, 50)
ax11.grid(True, alpha=0.3, axis='y')

# Add value labels and insight
for bar, pct in zip(bars, pct_errors_from_large):
    ax11.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{pct:.1f}%',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax11.text(0.5, 0.5, f'Large orders = {pct_large.iloc[2]:.1f}% of volume\nBut cause {pct_errors_from_large.iloc[2]:.1f}% of errors',
         transform=ax11.transAxes,
         fontsize=10, fontweight='bold', ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#FFE5E5', edgecolor='#DC2F02', linewidth=2))

# Graph 2.6: Key Insights for Large Orders
ax12 = plt.subplot(2, 3, 6)
ax12.axis('off')

# Calculate key metrics
volume_ratio = pct_large.iloc[2]
error_ratio = pct_errors_from_large.iloc[2]
disproportionate_factor = error_ratio / volume_ratio

# Calculate error rate change
error_rate_start = df_large['Error Rate (%)'].iloc[0]
error_rate_end = df_large['Error Rate (%)'].iloc[2]
error_rate_change = ((error_rate_end / error_rate_start) - 1) * 100

insight_text_large = f"""
CRITICAL FINDINGS - LARGE ORDERS ANALYSIS

🎯 DISPROPORTIONATE ERROR CONCENTRATION
• Large orders: {volume_ratio:.1f}% of volume
• But cause: {error_ratio:.1f}% of all errors
• {disproportionate_factor:.1f}x higher error rate than average

📈 ACCELERATING CRISIS
• Error rate: {error_rate_start:.2f}% → {error_rate_end:.2f}% (+{error_rate_change:.1f}%)
• Now at {error_rate_end:.2f}% error rate (10% in March)
• Picking errors up {error_growth:.1f}% in 90 days

🚨 ROOT CAUSE HYPOTHESIS
• Picking system optimized for small orders
• Complex orders (5+ items) break the workflow
• Staff lack training for large order handling
• Possible layout/routing inefficiencies

💡 IMMEDIATE ACTIONS REQUIRED
1. Dedicated large-order picking workflow
2. Specialized training for complex orders
3. Technology investment (pick-to-light, etc.)
4. Process redesign for multi-item efficiency
"""

ax12.text(0.05, 0.95, insight_text_large, transform=ax12.transAxes,
        fontsize=9.5, verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=1', facecolor='#FFF5F5',
                 edgecolor='#DC2F02', linewidth=2))

plt.tight_layout()
plt.savefig('/Users/jonasvyshniauskas/Documents/getyourguide/claude_output/Large_Orders_Crisis_Analysis.png',
            dpi=300, bbox_inches='tight')
print("✓ Saved: Large_Orders_Crisis_Analysis.png")

print("\n" + "=" * 80)
print("VISUALIZATION GENERATION COMPLETE")
print("=" * 80)
print("\nGenerated Files:")
print("1. Q1_Warehouse_Operations_Analysis.png")
print("2. Large_Orders_Crisis_Analysis.png")
print("\nNext: Review visualizations and create analysis document")


from config import settings
from datetime import datetime

class Reporter:
    def __init__(self):
        pass

    def generate_reminder_message(self, total_value, total_profit):
        """
        Generates a simple reminder message.
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        profit_percent = (total_profit / (total_value - total_profit)) * 100 if (total_value - total_profit) > 0 else 0
        
        message = (
            f"🔔 *ISAMB Routine Reminder* ({now})\n\n"
            f"Please update your Google Sheet with the latest holdings.\n\n"
            f"💰 *Current Estimate:*\n"
            f"- Total Value: {total_value:,.0f} KRW\n"
            f"- Total Profit: {total_profit:,.0f} KRW ({profit_percent:.2f}%)\n\n"
            f"[Google Sheet Link](YOUR_SHEET_URL)"
        )
        return message

    def generate_rebalancing_report(self, holdings, suggestions, simulation_result):
        """
        Generates a detailed rebalancing report.
        """
        now = datetime.now().strftime("%Y-%m-%d")
        
        report = f"📊 *ISAMB Quarterly Report* ({now})\n\n"
        
        # 1. Rebalancing Suggestions
        if suggestions:
            report += "⚠️ *Rebalancing Required:*\n"
            for s in suggestions:
                direction = "🔴 SELL" if s['action'] == "SELL" else "🟢 BUY"
                report += (
                    f"{direction} {s['ticker']}\n"
                    f"  Diff: {s['diff_percent']*100:.1f}% ({s['amount']:,.0f} KRW)\n"
                    f"  New Weight: {s['target_weight']*100:.1f}%\n"
                )
        else:
            report += "✅ *Portfolio is Balanced.*\n"
            
        report += "\n"
        
        # 2. ISA Simulation
        report += "🔮 *ISA Maturity Simulation (3Y)*\n"
        report += f"  Tax Exempt: {simulation_result['tax_exempt']:,.0f} KRW\n"
        report += f"  Est. Tax (9.9%): {simulation_result['tax']:,.0f} KRW\n"
        report += f"  Net Profit: {simulation_result['net_profit']:,.0f} KRW\n"
        
        return report

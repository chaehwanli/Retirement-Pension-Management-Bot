
from config import settings

class Calculator:
    def __init__(self):
        pass

    def calculate_total_value(self, holdings):
        """
        Calculates the total value of the portfolio based on current holdings.
        holdings: List of dictionaries (from Google Sheet)
        """
        total_value = 0
        total_invested = 0
        
        total_cash = 0
        
        for item in holdings:
            qty = float(item.get('보유수량', 0))
            price = float(item.get('현재가', 0))
            avg_price = float(item.get('매수단가', 0))
            
            # Identify Cash
            if str(item.get('티커', '')).upper() in ['CASH', 'KRW']:
                total_cash += qty * price # usually price is 1
            
            total_value += qty * price
            total_invested += qty * avg_price
            
        return total_value, total_invested, total_cash

    def check_rebalancing_needed(self, holdings, target_weights=None):
        """
        Checks if rebalancing is needed based on thresholds.
        holdings: List of dicts.
        target_weights: Dict {ticker: target_percent}. If None, looks for 'Target_Weight' in holdings.
        """
        rebalancing_suggestions = []
        total_value, _, _ = self.calculate_total_value(holdings)
        
        if total_value == 0:
            return []

        for item in holdings:
            ticker = item.get('티커')
            current_val = float(item.get('보유수량', 0)) * float(item.get('현재가', 0))
            current_weight = current_val / total_value
            
            # Get target weight
            target = 0
            if target_weights and ticker in target_weights:
                target = target_weights[ticker]
            elif 'Target_Weight' in item:
                target = float(item['Target_Weight'])
            else:
                continue # No target specified, skip
                
            # Skip Rebalancing for Cash
            if ticker.upper() in ['CASH', 'KRW']:
                continue

            # Check threshold
            diff = current_weight - target
            if abs(diff) > settings.REBALANCING_THRESHOLD_PERCENT:
                action = "SELL" if diff > 0 else "BUY"
                amount_diff = diff * total_value
                rebalancing_suggestions.append({
                    'ticker': ticker,
                    'action': action,
                    'diff_percent': diff,
                    'amount': abs(amount_diff),
                    'current_weight': current_weight,
                    'target_weight': target
                })
                
        return rebalancing_suggestions

    def simulate_isa(self, total_profit):
        """
        Simulates ISA tax benefits and final payout.
        """
        tax_exempt = settings.ISA_TAX_EXEMPT_LIMIT
        tax_rate = settings.ISA_TAX_RATE_EXCESS
        
        if total_profit <= tax_exempt:
            tax = 0
        else:
            taxable_amount = total_profit - tax_exempt
            tax = taxable_amount * tax_rate
            
        return {
            'total_profit': total_profit,
            'tax_exempt': tax_exempt,
            'tax': tax,
            'net_profit': total_profit - tax
        }

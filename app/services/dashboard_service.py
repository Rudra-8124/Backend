class DashboardService:
    def get_summary(self):
        records = [] # Empty list as mock
        
        income = sum(r['amount'] for r in records if r['type'] == 'income')
        expense = sum(r['amount'] for r in records if r['type'] == 'expense')
        
        return {
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense
        }

    def get_category_summary(self):
        records = []
        
        summary = {}
        for r in records:
            cat = r['category']
            if cat not in summary:
                summary[cat] = {'income': 0, 'expense': 0}
            summary[cat][r['type']] += r['amount']
            
        return summary

    def get_recent_transactions(self):
        records = []
        return records

    def get_trends(self):
        records = []
        
        trends = {}
        for r in records:
            d = r['date']
            if d not in trends:
                trends[d] = {'income': 0, 'expense': 0}
            trends[d][r['type']] += r['amount']
            
        return trends

dashboard_service = DashboardService()

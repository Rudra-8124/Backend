from app.db.supabase_client import supabase


class DashboardService:
    TABLE = "financial_records"

    def _get_all_records(self):
        response = supabase.table(self.TABLE).select("*").eq("is_deleted", False).execute()
        return response.data or []

    def get_summary(self):
        records = self._get_all_records()

        income = sum(r['amount'] for r in records if r.get('type') == 'income')
        expense = sum(r['amount'] for r in records if r.get('type') == 'expense')

        return {
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense,
            "record_count": len(records),
        }

    def get_category_summary(self):
        records = self._get_all_records()

        summary = {}
        for r in records:
            cat = r.get('category', 'uncategorized')
            if cat not in summary:
                summary[cat] = {'income': 0.0, 'expense': 0.0}
            rtype = r.get('type')
            if rtype in ('income', 'expense'):
                summary[cat][rtype] += r.get('amount', 0)

        return summary

    def get_recent_transactions(self, limit: int = 10):
        response = (
            supabase.table(self.TABLE)
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []

    def get_trends(self):
        records = self._get_all_records()

        trends = {}
        for r in records:
            d = r.get('date', 'unknown')
            if d not in trends:
                trends[d] = {'income': 0.0, 'expense': 0.0}
            rtype = r.get('type')
            if rtype in ('income', 'expense'):
                trends[d][rtype] += r.get('amount', 0)

        # Return sorted by date ascending
        return dict(sorted(trends.items()))


dashboard_service = DashboardService()

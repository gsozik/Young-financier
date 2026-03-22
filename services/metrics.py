class MetricsCalculator:
    def calculate(self, report: dict) -> dict:
        data = report.get("financial_inputs", {})

        self.total_assets = data.get("total_assets", None)
        self.equity = data.get("equity", None)
        self.long_term_liabilities = data.get("long_term_liabilities", None)
        self.short_term_liabilities = data.get("short_term_liabilities", None)
        self.current_assets = data.get("current_assets", None)
        self.revenue = data.get("revenue", None)
        self.net_income = data.get("net_income", None)
        self.previous_year_revenue = data.get("previous_year_revenue", None)

        return {
            "equity_ratio": self._equity_ratio(),
            "debt_to_equity": self._debt_to_equity(),
            "debt_ratio": self._debt_ratio(),
            "current_ratio": self._current_ratio(),
            "working_capital": self._working_capital(),
            "net_margin": self._net_margin(),
            "return_on_assets": self._return_on_assets(),
            "return_on_equity": self._return_on_equity(),
            "asset_turnover": self._asset_turnover(),
            "revenue_growth": self._revenue_growth(),
        }

    def _is_number(self, value):
        return isinstance(value, (int, float))

    def _safe_div(self, a, b):
        if not self._is_number(a) or not self._is_number(b) or b == 0:
            return None
        return a / b

    def _safe_sub(self, a, b):
        if not self._is_number(a) or not self._is_number(b):
            return None
        return a - b

    def _total_liabilities(self):
        if not self._is_number(self.long_term_liabilities) or not self._is_number(self.short_term_liabilities):
            return None
        return self.long_term_liabilities + self.short_term_liabilities

    def _equity_ratio(self):
        return self._safe_div(self.equity, self.total_assets)

    def _debt_to_equity(self):
        return self._safe_div(self._total_liabilities(), self.equity)

    def _debt_ratio(self):
        return self._safe_div(self._total_liabilities(), self.total_assets)

    def _current_ratio(self):
        return self._safe_div(self.current_assets, self.short_term_liabilities)

    def _working_capital(self):
        return self._safe_sub(self.current_assets, self.short_term_liabilities)

    def _net_margin(self):
        return self._safe_div(self.net_income, self.revenue)

    def _return_on_assets(self):
        return self._safe_div(self.net_income, self.total_assets)

    def _return_on_equity(self):
        return self._safe_div(self.net_income, self.equity)

    def _asset_turnover(self):
        return self._safe_div(self.revenue, self.total_assets)

    def _revenue_growth(self):
        if not self._is_number(self.revenue) or not self._is_number(self.previous_year_revenue) or self.previous_year_revenue == 0:
            return None
        return (self.revenue / self.previous_year_revenue) - 1
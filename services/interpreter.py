class MetricsInterpreter:
    def interpret(self, metrics: dict) -> str:
        self.equity_ratio = metrics.get("equity_ratio", None)
        self.debt_to_equity = metrics.get("debt_to_equity", None)
        self.debt_ratio = metrics.get("debt_ratio", None)
        self.current_ratio = metrics.get("current_ratio", None)
        self.working_capital = metrics.get("working_capital", None)
        self.net_margin = metrics.get("net_margin", None)
        self.return_on_assets = metrics.get("return_on_assets", None)
        self.return_on_equity = metrics.get("return_on_equity", None)
        self.asset_turnover = metrics.get("asset_turnover", None)
        self.revenue_growth = metrics.get("revenue_growth", None)

        lines = [
            self._format_percent(
                "Equity Ratio (доля собственного капитала в активах)",
                self.equity_ratio
            ),
            self._format_percent(
                "D/E (отношение долга к собственному капиталу)",
                self.debt_to_equity
            ),
            self._format_percent(
                "Debt Ratio (доля обязательств в активах)",
                self.debt_ratio
            ),
            self._format_number(
                "Current Ratio (коэффициент текущей ликвидности)",
                self.current_ratio
            ),
            self._format_integer(
                "Working Capital (чистый оборотный капитал)",
                self.working_capital
            ),
            self._format_percent(
                "Net Margin (чистая рентабельность продаж)",
                self.net_margin
            ),
            self._format_percent(
                "ROA (рентабельность активов)",
                self.return_on_assets
            ),
            self._format_percent(
                "ROE (рентабельность собственного капитала)",
                self.return_on_equity
            ),
            self._format_number(
                "Asset Turnover (оборачиваемость активов)",
                self.asset_turnover
            ),
            self._format_percent(
                "Revenue Growth (темп роста выручки)",
                self.revenue_growth
            ),
        ]

        return "\n".join(lines)

    def _format_percent(self, title: str, value):
        if value is None:
            return f"{title} = нет данных"
        return f"{title} = {value * 100:.2f}%"

    def _format_number(self, title: str, value):
        if value is None:
            return f"{title} = нет данных"
        return f"{title} = {value:.2f}"

    def _format_integer(self, title: str, value):
        if value is None:
            return f"{title} = нет данных"
        return f"{title} = {int(value)}"
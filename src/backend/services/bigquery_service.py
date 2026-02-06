import os
from google.cloud import bigquery
from datetime import datetime, timedelta

class BigQueryService:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "celestial-biome-480601")
        self.client = bigquery.Client(project=self.project_id)
        self.dataset = "celestial_biome_data_staging"
        # 各テーブル名の定義
        self.table_space = "space_weather_metrics"
        self.table_earthquake = "earthquakes_raw"
        self.table_economy = "economy_raw"

    def get_latest_metrics(self, hours: int = 24):
        """宇宙・地震・経済の3つのデータを統合して取得する"""
        
        # 1. 宇宙天気データの取得
        space_data = self._fetch_space_weather(hours)
        
        # 2. 地震データの取得
        earthquake_data = self._fetch_earthquakes(hours)
        
        # 3. 経済データの取得
        economy_data = self._fetch_economy()

        # 全データを結合して1つのコンテキストにする
        combined_context = f"""
### [Celestial Data Context]

#### 1. Space Weather (Last {hours}h)
{space_data}

#### 2. Earthquakes (Last {hours}h)
{earthquake_data}

#### 3. Global Economy Indicators (Latest)
{economy_data}
"""
        return combined_context

    def _fetch_space_weather(self, hours: int):
        query = f"""
            SELECT timestamp, metric, value
            FROM `{self.project_id}.{self.dataset}.{self.table_space}`
            WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {hours} HOUR)
            ORDER BY timestamp DESC LIMIT 20
        """
        results = self.client.query(query).result()
        lines = [f"- {r.timestamp}: {r.metric} = {r.value}" for r in results]
        return "\n".join(lines) if lines else "No space weather data."

    def _fetch_earthquakes(self, hours: int):
        # マグニチュードが大きい順、または最新順に取得
        query = f"""
            SELECT timestamp, magnitude, place, depth
            FROM `{self.project_id}.{self.dataset}.{self.table_earthquake}`
            WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {hours} HOUR)
            ORDER BY magnitude DESC LIMIT 5
        """
        results = self.client.query(query).result()
        lines = [f"- {r.timestamp}: M{r.magnitude} at {r.place} (Depth: {r.depth}km)" for r in results]
        return "\n".join(lines) if lines else "No significant earthquakes."

    def _fetch_economy(self):
        # 経済指標の最新値を取得
        query = f"""
            SELECT country_iso3, indicator_type, value, date
            FROM `{self.project_id}.{self.dataset}.{self.table_economy}`
            WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
            QUALIFY ROW_NUMBER() OVER(PARTITION BY country_iso3, indicator_type ORDER BY date DESC) = 1
            LIMIT 10
        """
        results = self.client.query(query).result()
        lines = [f"- {r.country_iso3} {r.indicator_type}: {r.value} (Date: {r.date})" for r in results]
        return "\n".join(lines) if lines else "No recent economic indicators."
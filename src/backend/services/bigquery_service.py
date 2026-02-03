import os
from google.cloud import bigquery
from datetime import datetime, timedelta

class BigQueryService:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "celestial-biome-480601")
        self.client = bigquery.Client(project=self.project_id)
        self.dataset = "celestial_biome_data_staging"
        self.table = "space_weather_metrics"

    def get_latest_metrics(self, hours: int = 24):
        """直近数時間の最新宇宙天気指標を取得する"""
        query = f"""
            SELECT
                timestamp,
                metric,
                value
            FROM
                `{self.project_id}.{self.dataset}.{self.table}`
            WHERE
                timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {hours} HOUR)
            ORDER BY
                timestamp DESC
        """
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Gemini に渡しやすくするためテキスト形式に整形
            metrics_summary = []
            for row in results:
                metrics_summary.append(
                    f"Time: {row.timestamp}, Metric: {row.metric}, Value: {row.value}"
                )
            
            return "\n".join(metrics_summary) if metrics_summary else "No recent space weather data available."
        except Exception as e:
            print(f"BigQuery Error: {e}")
            return "Space weather data currently unavailable."
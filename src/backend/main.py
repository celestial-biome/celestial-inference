import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
from services.bigquery_service import BigQueryService

app = FastAPI(title="Celestial Inference API")
bigquery_service = BigQueryService()

# GCP プロジェクト設定 (Terraform で注入した環境変数を使用)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"

# Vertex AI の初期化
vertexai.init(project=PROJECT_ID, location=REGION)

class InferenceRequest(BaseModel):
    prompt: str

@app.post("/v1/predict")
async def predict(request: InferenceRequest):
    # 1. コンテキスト取得
    context = bigquery_service.get_latest_metrics(hours=12)
    
    # 2. システム命令とデータの統合
    system_instruction = """
    あなたは Celestial Biome プロジェクトの専門 AI 助手です。
    提供される宇宙天気データ（X線フラックス、太陽風速度、磁場、Kp指数など）を考慮し、
    それらが地球上の生物、社会、経済あるいは人の感性にどのような微細な影響を与えるか、
    科学的かつ詩的な洞察を交えて回答してください。
    """

    full_prompt = f"{system_instruction}\n\n### 最新の宇宙天気データ:\n{context}\n\n### ユーザーの質問:\n{request.prompt}"
    
    # 3. 推論
    model = GenerativeModel("gemini-2.0-flash-001")
    response = await model.generate_content_async(full_prompt)

    return {"content": response.text, "context_used": context}

    try:
        # Gemini 2.0 Flash 
        model = GenerativeModel("gemini-2.0-flash-001")
        
        # 推論の実行
        response = await model.generate_content_async(
            request.prompt,
            generation_config={
                "max_output_tokens": request.max_output_tokens,
                "temperature": request.temperature,
            }
        )
        
        return InferenceResponse(content=response.text)
    
    except Exception as e:
        # 詳細は後ほど Sentry で捕捉するようにします
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
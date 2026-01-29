import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

app = FastAPI(title="Celestial Inference API")

# GCP プロジェクト設定 (Terraform で注入した環境変数を使用)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "asia-northeast1"

# Vertex AI の初期化
vertexai.init(project=PROJECT_ID, location=REGION)

class InferenceRequest(BaseModel):
    prompt: str
    max_output_tokens: int = 1024
    temperature: float = 0.7

class InferenceResponse(BaseModel):
    content: str

@app.post("/v1/predict", response_model=InferenceResponse)
async def predict(request: InferenceRequest):
    try:
        # モデルの初期化 (Gemini 1.5 Flash を推奨)
        model = GenerativeModel("gemini-1.5-flash-002")
        
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
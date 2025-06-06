from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
import io

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_bayes_probabilities(df):
    # Calcular probabilidades básicas
    total_conversions = df['conversions'].sum()
    total_clicks = df['clicks'].sum()
    total_impressions = df['impressions'].sum()

    # Probabilidade geral de conversão (P(Conversão))
    p_conversion = total_conversions / total_clicks

    results = []

    for _, row in df.iterrows():
        channel = row['channel']
        clicks = row['clicks']
        conversions = row['conversions']

        # P(Canal | Conversão) = conversões neste canal / total de conversões
        p_channel_given_conversion = conversions / total_conversions

        # P(Canal) = cliques neste canal / total de cliques
        p_channel = clicks / total_clicks

        # Teorema de Bayes: P(Conversão | Canal)
        p_conversion_given_channel = (p_channel_given_conversion * p_conversion) / p_channel

        # ROI (Return on Investment)
        roi = (conversions * 100) / row['cost']  # Assumindo que cada conversão vale $100

        results.append({
            'channel': channel,
            'probability': round(p_conversion_given_channel, 4),
            'roi': round(roi, 2),
            'recommendation_score': round(p_conversion_given_channel * roi, 4)
        })

    # Ordenar por recommendation_score
    results_sorted = sorted(results, key=lambda x: x['recommendation_score'], reverse=True)

    return results_sorted

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

    # Calcular métricas adicionais
    df['CTR'] = df['clicks'] / df['impressions'] * 100
    df['CPA'] = df['cost'] / df['conversions']

    # Processar dados com Bayes
    results = calculate_bayes_probabilities(df)

    # Incluir métricas adicionais no resultado
    for result in results:
        row = df[df['channel'] == result['channel']].iloc[0]
        result['CTR'] = round(row['CTR'], 2)
        result['CPA'] = round(row['CPA'], 2)

    # Gerar recomendação
    recommendation = f"Aloque mais recursos em {results[0]['channel']} (Probabilidade: {results[0]['probability']*100:.2f}%, ROI: ${results[0]['roi']} por dólar investido)"

    return {
        "probabilities": results,
        "recommendation": recommendation
    }

@app.get("/sample")
async def get_sample_data():
    # Carregar dados de exemplo
    df = pd.read_csv('data/sample_data.csv')

    df['CTR'] = df['clicks'] / df['impressions'] * 100
    df['CPA'] = df['cost'] / df['conversions']

    results = calculate_bayes_probabilities(df)

    for result in results:
        row = df[df['channel'] == result['channel']].iloc[0]
        result['CTR'] = round(row['CTR'], 2)
        result['CPA'] = round(row['CPA'], 2)

    recommendation = f"Aloque mais recursos em {results[0]['channel']} (Probabilidade: {results[0]['probability']*100:.2f}%, ROI: ${results[0]['roi']} por dólar investido)"

    return {
        "probabilities": results,
        "recommendation": recommendation
    }

@app.get("/instructions", response_class=HTMLResponse)
async def get_instructions():
    return """
    <html>
        <head>
            <title>Instruções para Upload de Dados</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #2c3e50; }
                .instruction-box { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #3498db; color: white; }
                pre { background-color: #2c3e50; color: white; padding: 10px; border-radius: 4px; overflow-x: auto; }
            </style>
        </head>
        <body>
            <h1>Instruções para Preparação de Dados</h1>

            <div class="instruction-box">
                <h2>Formato do Arquivo CSV</h2>
                <p>Seu arquivo CSV deve conter as seguintes colunas:</p>
                <ul>
                    <li><strong>channel</strong>: Nome do canal de marketing</li>
                    <li><strong>impressions</strong>: Número de impressões/exibições</li>
                    <li><strong>clicks</strong>: Número de cliques</li>
                    <li><strong>conversions</strong>: Número de conversões</li>
                    <li><strong>cost</strong>: Custo total da campanha (em dólares)</li>
                </ul>
            </div>

            <div class="instruction-box">
                <h2>Exemplo de Arquivo CSV</h2>
                <pre>
channel,impressions,clicks,conversions,cost
google_ads,10000,500,50,2000
instagram,8000,400,60,1200
email,15000,750,30,900
facebook,12000,300,20,1500</pre>
            </div>

            <div class="instruction-box">
                <h2>Métricas Calculadas</h2>
                <p>Além dos dados fornecidos, calcularemos automaticamente:</p>
                <table>
                    <tr>
                        <th>Métrica</th>
                        <th>Descrição</th>
                        <th>Fórmula</th>
                    </tr>
                    <tr>
                        <td>CTR</td>
                        <td>Taxa de Clique</td>
                        <td>Cliques / Impressões</td>
                    </tr>
                    <tr>
                        <td>CPA</td>
                        <td>Custo por Aquisição</td>
                        <td>Custo / Conversões</td>
                    </tr>
                    <tr>
                        <td>Prob. Conversão</td>
                        <td>Probabilidade de conversão por canal</td>
                        <td>Teorema de Bayes</td>
                    </tr>
                </table>
            </div>
        </body>
    </html>
    """

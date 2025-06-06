async function processFile() {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Por favor, selecione um arquivo CSV');
        return;
    }

    try {
        const rawData = await readFile(file);
        const parsedData = parseCSV(rawData);
        displayUploadedData(parsedData);

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData
        });

        const analysisResults = await response.json();
        displayResults(analysisResults);

    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao processar o arquivo: ' + error.message);
    }
}

function readFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = event => resolve(event.target.result);
        reader.onerror = error => reject(error);
        reader.readAsText(file);
    });
}

function parseCSV(csvText) {
    const lines = csvText.split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim() === '') continue;

        const values = lines[i].split(',');
        const entry = {};

        for (let j = 0; j < headers.length; j++) {
            entry[headers[j]] = values[j] ? values[j].trim() : '';
        }

        data.push(entry);
    }

    return data;
}

function displayUploadedData(data) {
    const uploadedDataSection = document.getElementById('uploadedDataSection');
    const uploadedDataBody = document.getElementById('uploadedDataBody');

    uploadedDataSection.style.display = 'block';
    uploadedDataBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        const impressions = parseInt(item.impressions) || 0;
        const clicks = parseInt(item.clicks) || 0;
        const conversions = parseInt(item.conversions) || 0;
        const cost = parseFloat(item.cost) || 0;

        const ctr = impressions > 0 ? (clicks / impressions * 100).toFixed(2) + '%' : 'N/A';
        const cpa = conversions > 0 ? (cost / conversions).toFixed(2) : 'N/A';

        row.innerHTML = `
            <td>${item.channel || ''}</td>
            <td>${impressions.toLocaleString()}</td>
            <td>${clicks.toLocaleString()}</td>
            <td>${conversions.toLocaleString()}</td>
            <td>$${cost.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
            <td class="metric-highlight">${ctr}</td>
            <td class="metric-highlight">$${cpa}</td>
        `;

        uploadedDataBody.appendChild(row);
    });

    uploadedDataSection.scrollIntoView({ behavior: 'smooth' });
}

async function loadSampleData() {
    try {
        const sampleData = [
            { channel: 'google_ads', impressions: '10000', clicks: '500', conversions: '50', cost: '2000' },
            { channel: 'instagram', impressions: '8000', clicks: '400', conversions: '60', cost: '1200' },
            { channel: 'email', impressions: '15000', clicks: '750', conversions: '30', cost: '900' },
            { channel: 'facebook', impressions: '12000', clicks: '300', conversions: '20', cost: '1500' }
        ];

        displayUploadedData(sampleData);

        const response = await fetch('http://localhost:8000/sample');
        if (!response.ok) {
            throw new Error('Erro ao carregar dados de exemplo');
        }
        const analysisResults = await response.json();
        displayResults(analysisResults);

    } catch (error) {
        console.error('Erro:', error);
        alert('Dados de exemplo carregados, mas a análise não pôde ser concluída: ' + error.message);
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const recommendationDiv = document.getElementById('recommendation');
    const resultsBody = document.getElementById('resultsBody');

    resultsSection.style.display = 'block';
    recommendationDiv.innerHTML = `<strong>Recomendação:</strong> ${data.recommendation}`;
    resultsBody.innerHTML = '';

    // Ordenar por score decrescente
    const sorted = data.probabilities.sort((a, b) => b.recommendation_score - a.recommendation_score);

    sorted.forEach((item, index) => {
        const row = document.createElement('tr');

        if (item.recommendation_score > 0.5) {
            row.classList.add('high-score');
        } else if (item.recommendation_score > 0.2) {
            row.classList.add('medium-score');
        }

        const icon = index === 0 ? '⭐ ' : '';

        row.innerHTML = `
            <td>${icon}${item.channel}</td>
            <td>${(item.probability * 100).toFixed(2)}%</td>
            <td><span style="color: #27ae60; font-weight: bold;">$${item.roi}</span></td>
            <td><span style="color: #e67e22; font-weight: bold;">${item.recommendation_score.toFixed(4)}</span></td>
            <td>${item.CTR ? item.CTR.toFixed(2) + '%' : 'N/A'}</td>
            <td>${item.CPA ? '$' + item.CPA.toFixed(2) : 'N/A'}</td>
        `;

        resultsBody.appendChild(row);
    });

    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

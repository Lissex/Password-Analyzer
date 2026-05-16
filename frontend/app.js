// DOM Elements
const passwordInput = document.getElementById('passwordInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const togglePasswordBtn = document.getElementById('togglePasswordBtn');
const entropyValue = document.getElementById('entropyValue');
const strengthBar = document.getElementById('strengthBar');
const strengthBadge = document.getElementById('strengthBadge');
const percentileValue = document.getElementById('percentileValue');
const funFact = document.getElementById('funFact');
const gpuTime = document.getElementById('gpuTime');
const badgeLowercase = document.getElementById('badgeLowercase');
const badgeUppercase = document.getElementById('badgeUppercase');
const badgeDigits = document.getElementById('badgeDigits');
const badgeSymbols = document.getElementById('badgeSymbols');
const crackElements = {
    online_throttled: document.getElementById('crackOnlineThrottled'),
    online_unthrottled: document.getElementById('crackOnlineUnthrottled'),
    offline_slow: document.getElementById('crackOfflineSlow'),
    offline_fast: document.getElementById('crackOfflineFast')
};
const lengthSlider = document.getElementById('lengthSlider');
const lengthValue = document.getElementById('lengthValue');
const toggleUppercase = document.getElementById('toggleUppercase');
const toggleDigits = document.getElementById('toggleDigits');
const toggleSymbols = document.getElementById('toggleSymbols');
const generateBtn = document.getElementById('generateBtn');
const generatedPassword = document.getElementById('generatedPassword');
const copyBtn = document.getElementById('copyBtn');
const historyTableBody = document.getElementById('historyTableBody');

const API_BASE = '/api/v1';

async function fetchAPI(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: { 'Content-Type': 'application/json' },
        ...options
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Request failed');
    }
    return response.json();
}

// Преобразование секунд в читаемый формат
function formatTime(seconds) {
    if (seconds < 1) return 'мгновенно';
    if (seconds < 60) return `${Math.floor(seconds)} сек`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)} мин`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} ч`;
    if (seconds < 31536000) return `${Math.floor(seconds / 86400)} дней`;
    if (seconds < 31536000000) return `${Math.floor(seconds / 31536000)} лет`;
    return `${Math.floor(seconds / 31536000000)} тыс. лет`;
}

// Расчёт процента паролей, которые слабее
function calculatePercentile(entropy) {
    // Модель распределения паролей (приблизительная)
    if (entropy < 20) return 5;
    if (entropy < 28) return 15;
    if (entropy < 36) return 35;
    if (entropy < 60) return 70;
    if (entropy < 80) return 90;
    if (entropy < 100) return 97;
    if (entropy < 128) return 99.5;
    return 99.99;
}

// Интересные факты
function getFunFact(entropy, poolSize, length) {
    const facts = [];
    
    if (entropy < 28) {
        facts.push('⚠️ Этот пароль взламывается быстрее, чем заваривается чай');
    } else if (entropy < 36) {
        facts.push('😐 Такой пароль взломают пока вы пьете кофе');
    } else if (entropy < 60) {
        facts.push('👍 Уже неплохо, но хакеру потребуется всего несколько дней');
    } else if (entropy < 80) {
        facts.push('🔒 Хороший пароль! Хакер потратит годы');
    } else if (entropy < 128) {
        facts.push('🛡️ Отличный пароль! Даже ферма GPU не справится');
    } else {
        facts.push('💎 Броня! Твой пароль переживет человечество');
    }
    
    if (poolSize === 26) {
        facts.push('📝 Используй цифры и символы для усиления');
    } else if (poolSize < 52) {
        facts.push('🔤 Добавь символы для повышения стойкости');
    }
    
    if (length < 12) {
        facts.push('📏 Увеличь длину пароля до 12+ символов');
    }
    
    return facts[Math.floor(Math.random() * facts.length)];
}

// Время взлома на RTX 4090 (12 000 000 000 паролей/сек для MD5)
function formatGPUTime(entropy) {
    const combinations = Math.pow(2, entropy);
    const gpuSpeed = 12_000_000_000; // 12 млрд паролей/сек на RTX 4090
    const seconds = combinations / gpuSpeed;
    return formatTime(seconds);
}

function getCrackTimeColor(seconds) {
    if (seconds > 3153600000) return 'text-success';
    if (seconds > 31536000) return 'text-warning';
    if (seconds > 86400) return 'text-danger-emphasis';
    return 'text-danger';
}

function animateEntropy(target) {
    entropyValue.textContent = target.toFixed(1);
}

function updateUI(analysis) {
    animateEntropy(analysis.entropy_bits);
    
    let percent = Math.min(100, (analysis.entropy_bits / 128) * 100);
    strengthBar.style.width = `${percent}%`;
    
    let barColor = 'bg-danger';
    if (analysis.entropy_bits >= 128) barColor = 'bg-purple';
    else if (analysis.entropy_bits >= 60) barColor = 'bg-success';
    else if (analysis.entropy_bits >= 36) barColor = 'bg-info';
    else if (analysis.entropy_bits >= 28) barColor = 'bg-warning';
    strengthBar.className = `progress-bar ${barColor}`;
    
    strengthBadge.textContent = analysis.strength_label;
    
    // Процентная метрика
    const percentile = calculatePercentile(analysis.entropy_bits);
    percentileValue.textContent = `${percentile}%`;
    
    // Интересный факт
    funFact.textContent = getFunFact(analysis.entropy_bits, analysis.pool_size, 
        Math.log2(analysis.pool_size) > 0 ? Math.round(analysis.entropy_bits / Math.log2(analysis.pool_size)) : 0);
    
    // Время взлома на GPU
    gpuTime.textContent = formatGPUTime(analysis.entropy_bits);
    
    badgeLowercase.className = `badge rounded-pill ${analysis.pool_details.has_lowercase ? 'bg-purple' : 'bg-secondary'}`;
    badgeUppercase.className = `badge rounded-pill ${analysis.pool_details.has_uppercase ? 'bg-purple' : 'bg-secondary'}`;
    badgeDigits.className = `badge rounded-pill ${analysis.pool_details.has_digits ? 'bg-purple' : 'bg-secondary'}`;
    badgeSymbols.className = `badge rounded-pill ${analysis.pool_details.has_symbols ? 'bg-purple' : 'bg-secondary'}`;
    
    for (const estimate of analysis.crack_estimates) {
        const element = crackElements[estimate.scenario];
        if (element) {
            element.textContent = formatTime(estimate.seconds);
            element.className = getCrackTimeColor(estimate.seconds);
        }
    }
}

async function analyzePassword() {
    const password = passwordInput.value;
    if (!password) {
        alert('Введите пароль');
        return;
    }
    
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Анализируем...';
    
    try {
        const result = await fetchAPI('/analyze', {
            method: 'POST',
            body: JSON.stringify({ password })
        });
        updateUI(result);
        await loadHistory();
    } catch (error) {
        console.error('Analysis failed:', error);
        alert('Ошибка анализа');
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '🔐 Анализировать пароль';
    }
}

analyzeBtn.addEventListener('click', analyzePassword);

let isPasswordVisible = false;
togglePasswordBtn.addEventListener('click', () => {
    isPasswordVisible = !isPasswordVisible;
    passwordInput.type = isPasswordVisible ? 'text' : 'password';
    togglePasswordBtn.textContent = isPasswordVisible ? '🙈' : '👁️';
});

async function generatePassword() {
    const length = parseInt(lengthSlider.value);
    const uppercase = toggleUppercase.checked;
    const digits = toggleDigits.checked;
    const symbols = toggleSymbols.checked;
    
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Генерируем...';
    
    try {
        const result = await fetchAPI('/generate', {
            method: 'POST',
            body: JSON.stringify({ length, uppercase, digits, symbols })
        });
        generatedPassword.value = result.password;
        updateUI(result);
        await loadHistory();
    } catch (error) {
        console.error('Generation failed:', error);
        generatedPassword.value = 'Ошибка генерации';
    } finally {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '✨ Сгенерировать пароль';
    }
}

generateBtn.addEventListener('click', generatePassword);

async function copyPassword() {
    const password = generatedPassword.value;
    if (!password || password === 'Нажмите Generate' || password === 'Ошибка генерации') return;
    
    try {
        await navigator.clipboard.writeText(password);
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '✓ Скопировано!';
        copyBtn.classList.add('btn-success');
        setTimeout(() => {
            copyBtn.innerHTML = '📋 Копировать';
            copyBtn.classList.remove('btn-success');
        }, 2000);
    } catch (err) {
        alert('Не удалось скопировать');
    }
}

copyBtn.addEventListener('click', copyPassword);

async function loadHistory() {
    try {
        const history = await fetchAPI('/history?limit=10');
        if (!history.items || history.items.length === 0) {
            historyTableBody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">Нет анализов</td></tr>';
            return;
        }
        historyTableBody.innerHTML = history.items.map(item => {
            const gpuTimeFormatted = formatGPUTime(item.entropy_bits);
            return `
            <tr>
                <td class="small">${new Date(item.analyzed_at).toLocaleString()}</td>
                <td class="font-monospace fw-bold">${item.entropy_bits.toFixed(1)} бит</td>
                <td><span class="badge" style="background:${item.strength_color}">${item.strength_label}</span></td>
                <td class="small">${gpuTimeFormatted}</td>
            </tr>
        `}).join('');
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

lengthSlider.addEventListener('input', (e) => {
    lengthValue.textContent = e.target.value;
});

loadHistory();
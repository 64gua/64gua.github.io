// stockAPI.js - 使用JSONP方式
async function getKLineData(stockCode, startDate, endDate, klineType = 'daily') {
    // ... 参数校验代码 ...
    
    return new Promise((resolve, reject) => {
        const symbol = getStockSymbol(stockCode);
        const callbackName = 'sina_jsonp_' + Date.now();
        
        // 构建URL
        const url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData';
        const params = new URLSearchParams({
            symbol: symbol,
            scale: '240',
            ma: 'no',
            datalen: '2000'
        });
        
        // 创建script标签
        const script = document.createElement('script');
        script.src = `${url}?${params.toString()}`;
        
        // 处理响应
        window[callbackName] = function(data) {
            delete window[callbackName];
            document.body.removeChild(script);
            
            try {
                // 处理数据
                const records = filterDataByDate(data, startDate, endDate);
                resolve(records);
            } catch (error) {
                reject(error);
            }
        };
        
        script.onerror = function() {
            delete window[callbackName];
            document.body.removeChild(script);
            reject(new Error('JSONP请求失败'));
        };
        
        document.body.appendChild(script);
    });
}

function filterDataByDate(rawData, startDate, endDate) {
    if (!Array.isArray(rawData) || rawData.length === 0) return [];
    
    const start = new Date(startDate);
    const end = new Date(endDate);
    const startTimestamp = start.getTime();
    const endTimestamp = end.getTime();
    
    const records = [];
    for (const item of rawData) {
        const dateStr = item.day;
        if (!dateStr) continue;
        
        const itemDate = new Date(dateStr);
        const itemTime = itemDate.getTime();
        
        if (itemTime >= startTimestamp && itemTime <= endTimestamp) {
            records.push({
                date: dateStr,
                open: parseFloat(item.open) || 0,
                high: parseFloat(item.high) || 0,
                low: parseFloat(item.low) || 0,
                close: parseFloat(item.close) || 0,
                volume: parseFloat(item.volume) || 0
            });
        }
    }
    
    records.sort((a, b) => new Date(a.date) - new Date(b.date));
    return records;
}
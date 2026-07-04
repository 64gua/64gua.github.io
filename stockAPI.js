/**
 * 新浪股票K线数据获取模块 (JavaScript版本)
 * 对应Python版本的 _get_from_sina 函数
 * 使用方式: StockAPI.getKLineData(stockCode, startDate, endDate)
 */

const StockAPI = (function() {
    'use strict';

    /**
     * 转换股票代码为新浪格式
     * @param {string} code - 股票代码，如 '600000' 或 'sh600000'
     * @returns {string} 新浪格式的symbol，如 'sh600000'
     */
    function getStockSymbol(code) {
        // 去除首尾空格
        code = code.trim();
        
        // 如果已经包含前缀，直接返回小写
        if (code.startsWith('sh') || code.startsWith('sz')) {
            return code.toLowerCase();
        }

        // === 指数特殊处理 ===
        // 上证指数
        if (code === '999999' || code === 'sh000001') {
            return 'sh000001';
        }
        // 深证成指
        if (code === '399001') {
            return 'sz399001';
        }
        // 创业板指
        if (code === '399006') {
            return 'sz399006';
        }
        // 科创50
        if (code === '000688') {
            return 'sh000688';
        }
        // 沪深300
        if (code === '000300') {
            return 'sh000300';
        }

        // === 股票处理 ===
        // 6开头或5开头 → 上海
        if (code.startsWith('6') || code.startsWith('5')) {
            return `sh${code}`;
        }
        // 其他（0、3开头等）→ 深圳
        else {
            return `sz${code}`;
        }
    }

    /**
     * 从新浪API获取K线数据
     * @param {string} stockCode - 股票代码，如 '600000' 或 'sh600000'
     * @param {string} startDate - 开始日期，格式 'YYYY-MM-DD'
     * @param {string} endDate - 结束日期，格式 'YYYY-MM-DD'
     * @param {string} klineType - K线类型: 'daily'(日线), 'weekly'(周线), 'monthly'(月线) ，默认 'daily'
     * @returns {Promise<Array>} 返回包含OHLCV数据的数组，按日期升序排列
     */
    async function getKLineData(stockCode, startDate, endDate, klineType = 'daily') {
        // 参数校验
        if (!stockCode || !startDate || !endDate) {
            throw new Error('参数不完整: 需要股票代码、开始日期、结束日期');
        }

        // 日期格式校验
        const start = new Date(startDate);
        const end = new Date(endDate);
        if (isNaN(start.getTime()) || isNaN(end.getTime())) {
            throw new Error('日期格式错误，请使用 YYYY-MM-DD 格式');
        }
        if (start > end) {
            throw new Error('开始日期不能晚于结束日期');
        }

        try {
            // 1. 转换为新浪symbol
            const symbol = getStockSymbol(stockCode);
            
            // 2. 构建请求URL
            const url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData';
            const params = new URLSearchParams({
                symbol: symbol,
                scale: '240',      // 日线
                ma: 'no',
                datalen: '2000'    // 获取足够多数据
            });

            // 3. 发起请求
            const response = await fetch(`${url}?${params.toString()}`, {
                method: 'GET',
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP错误: ${response.status} ${response.statusText}`);
            }

            // 4. 解析响应
            let text = await response.text();
            
            // 处理可能的JSONP包装
            if (text.startsWith('/*')) {
                const startIdx = text.indexOf('(');
                const endIdx = text.lastIndexOf(')');
                if (startIdx !== -1 && endIdx !== -1) {
                    text = text.substring(startIdx + 1, endIdx);
                }
            }

            let rawData;
            try {
                rawData = JSON.parse(text);
            } catch (e) {
                throw new Error(`JSON解析失败: ${e.message}\n原始返回: ${text.substring(0, 200)}`);
            }

            if (!Array.isArray(rawData) || rawData.length === 0) {
                console.warn('新浪API返回空数据');
                return [];
            }

            // 5. 过滤日期范围并转换数据
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

            // 6. 按日期升序排序
            records.sort((a, b) => new Date(a.date) - new Date(b.date));

            // 7. 根据klineType聚合（周线/月线）
            if (klineType === 'daily') {
                console.log(`✅ 获取到 ${records.length} 条日线数据 (${startDate} ~ ${endDate})`);
                return records;
            } else if (klineType === 'weekly') {
                const weeklyData = aggregateToWeekly(records);
                console.log(`✅ 从日线聚合生成 ${weeklyData.length} 条周线数据`);
                return weeklyData;
            } else if (klineType === 'monthly') {
                const monthlyData = aggregateToMonthly(records);
                console.log(`✅ 从日线聚合生成 ${monthlyData.length} 条月线数据`);
                return monthlyData;
            } else {
                throw new Error(`不支持的K线类型: ${klineType}`);
            }

        } catch (error) {
            console.error('获取K线数据失败:', error);
            throw error;
        }
    }

    /**
     * 聚合日线数据为周线 (使用周五作为周结束)
     * @param {Array} dailyData - 日线数据数组
     * @returns {Array} 周线数据数组
     */
    function aggregateToWeekly(dailyData) {
        if (!dailyData || dailyData.length === 0) return [];

        const weeklyMap = new Map();

        for (const item of dailyData) {
            const date = new Date(item.date);
            // 获取该日期所在周的周五
            const dayOfWeek = date.getDay(); // 0=周日, 1=周一, ...
            const diffToFriday = dayOfWeek === 0 ? 5 : (5 - dayOfWeek); // 周日→周五需要加5天
            const friday = new Date(date);
            friday.setDate(date.getDate() + diffToFriday);
            const weekKey = friday.toISOString().split('T')[0];

            if (!weeklyMap.has(weekKey)) {
                weeklyMap.set(weekKey, {
                    date: weekKey,
                    open: item.open,
                    high: item.high,
                    low: item.low,
                    close: item.close,
                    volume: item.volume
                });
            } else {
                const existing = weeklyMap.get(weekKey);
                existing.high = Math.max(existing.high, item.high);
                existing.low = Math.min(existing.low, item.low);
                existing.close = item.close; // 最后一天的收盘价
                existing.volume += item.volume;
            }
        }

        // 转为数组并按日期排序
        const result = Array.from(weeklyMap.values());
        result.sort((a, b) => new Date(a.date) - new Date(b.date));
        return result;
    }

    /**
     * 聚合日线数据为月线 (使用月末)
     * @param {Array} dailyData - 日线数据数组
     * @returns {Array} 月线数据数组
     */
    function aggregateToMonthly(dailyData) {
        if (!dailyData || dailyData.length === 0) return [];

        const monthlyMap = new Map();

        for (const item of dailyData) {
            const date = new Date(item.date);
            const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
            // 月线日期用该月最后一天
            const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
            const monthDate = lastDay.toISOString().split('T')[0];

            if (!monthlyMap.has(monthKey)) {
                monthlyMap.set(monthKey, {
                    date: monthDate,
                    open: item.open,
                    high: item.high,
                    low: item.low,
                    close: item.close,
                    volume: item.volume
                });
            } else {
                const existing = monthlyMap.get(monthKey);
                existing.high = Math.max(existing.high, item.high);
                existing.low = Math.min(existing.low, item.low);
                existing.close = item.close;
                existing.volume += item.volume;
            }
        }

        // 转为数组并按日期排序
        const result = Array.from(monthlyMap.values());
        result.sort((a, b) => new Date(a.date) - new Date(b.date));
        return result;
    }

    // 公开API
    return {
        getKLineData: getKLineData,
        getStockSymbol: getStockSymbol,  // 暴露供调试
        aggregateToWeekly: aggregateToWeekly,
        aggregateToMonthly: aggregateToMonthly
    };

})();

// 在浏览器环境中暴露全局变量
if (typeof window !== 'undefined') {
    window.StockAPI = StockAPI;
}

// 在Node.js环境中导出 (如果使用模块)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StockAPI;
}
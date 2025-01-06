import { useState, useEffect } from 'react';
import ApexCharts from 'react-apexcharts';
import { useDispatch, useSelector } from 'react-redux';
import { stockDetails } from './SearchSlice';
import { RootState } from '../../store/Store';

interface StockData {
    date: string;
    close: number;
}

interface TimeSeriesDaily {
    [key: string]: {
        '1. open': string;
        '2. high': string;
        '3. low': string;
        '4. close': string;
        '5. volume': string;
    };
}

export default function StockGraph({ symbol }: { symbol: string }) {

    const [stockDatas, setStockData] = useState<StockData[]>([]);
    const [timeframe, setTimeframe] = useState<string>('1w');
    const stockData = useSelector((state: any) => state.search.stockDetailsPayload);
    const stockDetailsSuccess = useSelector((state: any) => state.search.stockDetailsSuccess);
    const { loading } = useSelector(
        (state: RootState) => state.search
    );

    const dispatch = useDispatch()

    const apiKey = 'demo';

    useEffect(() => {
        if (!stockDetailsSuccess) {
            dispatch<any>(stockDetails(symbol))
        }
        fetchStockData();
    }, [timeframe]);

    const fetchStockData = async () => {
        try {
            let apiUrl = '';
            if (timeframe === '1w') {
                apiUrl = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=${apiKey}`;
            } else if (timeframe === '1m') {
                apiUrl = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=${apiKey}`;
            } else if (timeframe === '3m') {
                apiUrl = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=${apiKey}`;
            } else if (timeframe === '1y' || timeframe === 'all') {
                apiUrl = `https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=${apiKey}`;
            }

            const response = await fetch(apiUrl);
            const data = await response.json();

            if (data['Error Message']) {
                throw new Error('Error fetching data from Alpha Vantage');
            }

            let stockDataArray: StockData[] = [];
            if (timeframe === '1w') {
                stockDataArray = Object.entries(data['Time Series (Daily)'] as TimeSeriesDaily)
                    .slice(0, 7)
                    .map(([date, info], index) => {
                        if (index === 0 || index === 3 || index === 6) {
                            return {
                                date: date,
                                close: parseFloat(info['4. close'] ?? '0'),
                            };
                        }
                        return undefined;
                    })
                    .filter((item): item is StockData => item !== undefined);
            }

            else if (timeframe === '1m') {
                stockDataArray = Object.entries(data['Time Series (Daily)'] as TimeSeriesDaily)
                    .slice(0, 30)
                    .map(([date, info]) => {
                        const day = parseInt(date.split('-')[2], 10);
                        if ([1, 10, 20, 30].includes(day)) {
                            return {
                                date: `${new Date(date).toLocaleString('en-us', { month: 'short' })} ${new Date(date).getFullYear()}`,
                                close: parseFloat(info['4. close'] ?? '0'),
                            };
                        }
                        return undefined;
                    })
                    .filter((item): item is StockData => item !== undefined);
            }

            else if (timeframe === '3m') {
                const encounteredMonths = new Set<string>();
                stockDataArray = Object.entries(data['Time Series (Daily)'] as TimeSeriesDaily)
                    .slice(0, 90)
                    .map(([date, info]) => {
                        const parsedDate = new Date(date);
                        const monthYear = `${parsedDate.toLocaleString('en-us', { month: 'short' })} ${parsedDate.getFullYear()}`;
                        const day = parseInt(date.split('-')[2], 10);

                        if ([1, 10, 20].includes(day) && !encounteredMonths.has(monthYear)) {
                            encounteredMonths.add(monthYear);
                            return {
                                date: monthYear,
                                close: parseFloat(info['4. close']),
                            };
                        }
                        return undefined;
                    })
                    .filter((item): item is StockData => item !== undefined);
            }


            else if (timeframe === '1y') {
                const lastYear = new Date().getFullYear() - 1;
                const filteredData = Object.entries(data['Monthly Time Series'] as TimeSeriesDaily)
                    .filter(([date]) => {
                        const month = new Date(date).getMonth() + 1;
                        const year = new Date(date).getFullYear();
                        return [1, 4, 7, 10].includes(month) && year === lastYear;
                    })
                    .map(([date, info]) => {
                        return {
                            date: `${new Date(date).toLocaleString('en-us', { month: 'short' })} ${new Date(date).getFullYear()}`,
                            close: parseFloat(info['4. close']) || 0,
                        };
                    })
                    .reverse();
                stockDataArray = filteredData;
            }

            else if (timeframe === 'all') {
                const filteredData = Object.entries(data['Monthly Time Series'] as TimeSeriesDaily)
                    .filter(([date]) => {
                        const month = new Date(date).getMonth() + 1;
                        const year = new Date(date).getFullYear();
                        return [1, 4, 7, 10].includes(month) && year % 5 === 0;
                    })
                    .map(([date, info]) => {
                        return {
                            date: `${new Date(date).getFullYear()}`,
                            close: parseFloat(info['4. close']) || 0,
                        };
                    })
                    .reverse();
                const uniqueYears = new Set();
                stockDataArray = filteredData.filter((data) => {
                    const year = new Date(data.date).getFullYear();
                    if (uniqueYears.has(year)) {
                        return false;
                    } else {
                        uniqueYears.add(year);
                        return true;
                    }
                });
            }
            setStockData(stockDataArray);
        } catch (error) {
            console.error('Error fetching stock data:', error);
        }
    };


    const chartData = {
        options: {
            chart: {
                id: 'stock-price-chart',
                type: 'line',
                zoom: { enabled: true },
                toolbar: { show: true },
            },
            xaxis: {
                categories: stockDatas.map((data) => data.date),
            },
            tooltip: {
                x: { format: 'MMM yyyy' },
            },
        },
        series: [
            {
                name: `${symbol} Stock Price`,
                data: stockDatas.map((data) => data.close),
            },
        ],
    };


    function formatNumber(num: any): string {
        if (num === null || num === undefined || isNaN(num)) {
            return "N/A";
        }
        const parsedNum = parseFloat(num);
        if (isNaN(parsedNum)) {
            return "N/A";
        }
        let formattedNumber: string;
        if (parsedNum >= 1e9) {
            formattedNumber = (parsedNum / 1e9).toFixed(2) + "B";
        } else if (parsedNum >= 1e6) {
            formattedNumber = (parsedNum / 1e6).toFixed(2) + "M";
        } else if (parsedNum >= 1e3) {
            formattedNumber = (parsedNum / 1e3).toFixed(2) + "K";
        } else {
            formattedNumber = parsedNum.toFixed(2);
        }
        return formattedNumber;
    }


    return (
        <div className="container">
            <div className="row py-md-5">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h4>${stockData?.price}</h4>
                            <div className="timeframe-buttons">
                                <button
                                    onClick={() => setTimeframe('1w')}
                                    className={`timeframe-buttons btn ${timeframe === '1w' ? 'active' : ''}`}
                                >
                                    1W
                                </button>
                                <button
                                    onClick={() => setTimeframe('1m')}
                                    className={`timeframe-buttons btn ${timeframe === '1m' ? 'active' : ''}`}
                                >
                                    1M
                                </button>
                                <button
                                    onClick={() => setTimeframe('3m')}
                                    className={`timeframe-buttons btn ${timeframe === '3m' ? 'active' : ''}`}
                                >
                                    3M
                                </button>
                                <button
                                    onClick={() => setTimeframe('1y')}
                                    className={`timeframe-buttons btn ${timeframe === '1y' ? 'active' : ''}`}
                                >
                                    1Y
                                </button>
                                <button
                                    onClick={() => setTimeframe('all')}
                                    className={`timeframe-buttons btn ${timeframe === 'all' ? 'active' : ''}`}
                                >
                                    All
                                </button>
                            </div>

                            <div style={{ position: 'relative', height: '350px' }}>
                                {loading && (
                                    <div
                                        style={{
                                            position: 'absolute',
                                            top: '50%',
                                            left: '50%',
                                            transform: 'translate(-50%, -50%)',
                                            fontSize: '18px',
                                            fontWeight: 'bold',
                                            color: '#000',
                                        }}
                                    >
                                        Loading...
                                    </div>
                                )}
                                <ApexCharts
                                    options={chartData.options}
                                    series={chartData.series}
                                    type="line"
                                    height={350}
                                />
                            </div>
                        </div>
                    </div>
                </div>


                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h3 className="text-center py-3">Stock Details</h3>
                            <div className="container text-center">
                                <div className="row pb-3">
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Price</span>
                                        <br />
                                        <strong>$ {stockData?.price ? formatNumber(stockData.price) : "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Market Cap</span>
                                        <br />
                                        <strong>$ {stockData?.marketCap ? formatNumber(stockData.marketCap) : "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">P/E Ratio</span>
                                        <br />
                                        <strong>{stockData?.peRatio || "N/A"} X</strong>
                                    </div>
                                </div>

                                <div className="row pb-3">
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">WeekHigh52</span>
                                        <br />
                                        <strong>$ {stockData?.WeekHigh52 ? formatNumber(stockData.WeekHigh52) : "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">WeekLow52</span>
                                        <br />
                                        <strong>$ {stockData?.WeekLow52 ? formatNumber(stockData.WeekLow52) : "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">P/B Ratio</span>
                                        <br />
                                        <strong>{stockData?.pbRatio || "N/A"} X</strong>
                                    </div>
                                </div>

                                <div className="row pb-3">
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">PEG</span>
                                        <br />
                                        <strong>{stockData?.pegRatio || "N/A"} X</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">P/S</span>
                                        <br />
                                        <strong>{stockData?.psRatio ? stockData.psRatio : "N/A"} X</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Dividend Yield</span>
                                        <br />
                                        <strong>{stockData?.dividendYield ? `${stockData.dividendYield}%` : "N/A"}</strong>
                                    </div>
                                </div>

                                <div className="row pb-3">
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Revenue</span>
                                        <br />
                                        <strong>$ {stockData?.revenue ? formatNumber(stockData.revenue) : "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Earnings</span>
                                        <br />
                                        <strong>$ {stockData?.earnings ? formatNumber(stockData.earnings) : "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Gross Margin</span>
                                        <br />
                                        <strong>
                                            {stockData?.grossMargin
                                                ? ((parseFloat(stockData.grossMargin) / parseFloat(stockData.grossMargin)) * 100).toFixed(2)
                                                : "N/A"}
                                            %
                                        </strong>
                                    </div>
                                </div>

                                <div className="row pb-3">
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Operating Margin</span>
                                        <br />
                                        <strong>
                                            {stockData?.operatingMargin
                                                ? ((parseFloat(stockData.operatingMargin) / parseFloat(stockData.operatingMargin)) * 100).toFixed(2)
                                                : "N/A"}
                                            %
                                        </strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Profit Margin</span>
                                        <br />
                                        <strong>
                                            {stockData?.profitMargin
                                                ? ((parseFloat(stockData.profitMargin) / parseFloat(stockData.profitMargin)) * 100).toFixed(2)
                                                : "N/A"}
                                            %
                                        </strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Debt To Equity</span>
                                        <br />
                                        <strong>{stockData?.debtToEquity ? `${stockData.debtToEquity}%` : "N/A"}</strong>
                                    </div>
                                </div>

                                <div className="row pb-3">
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Operating Cash Flow</span>
                                        <br />
                                        <strong>$ {stockData?.operatingCashFlow ? formatNumber(stockData.operatingCashFlow) : "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Beta</span>
                                        <br />
                                        <strong>{stockData?.beta || "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Latest Quarter</span>
                                        <br />
                                        <strong>{stockData?.LatestQuarter || "N/A"}</strong>
                                    </div>
                                </div>

                                <div className="row pb-3">
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Ex Dividend</span>
                                        <br />
                                        <strong>{stockData?.exDividendDate || "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Next Earnings</span>
                                        <br />
                                        <strong>{stockData?.nextEarnings || "N/A"}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Next Dividend</span>
                                        <br />
                                        <strong>{stockData?.nextDividend || "N/A"}</strong>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

    );
};


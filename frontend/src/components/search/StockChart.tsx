import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/Store';
import { AppDispatch } from '../../store/Store';
import ApexCharts from 'react-apexcharts';
import { graphData } from './SearchSlice';

export default function StockChart({ symbol }: { symbol: string }) {

    const dispatch = useDispatch<AppDispatch>();
    const [timeframe, setTimeframe] = useState("1d");

    const { loading, error, graphDataPayload } = useSelector(
        (state: RootState) => state.search
    );

    useEffect(() => {
        dispatch(graphData({ symbol: symbol, range_type: timeframe }));
    }, [dispatch, symbol, timeframe]);

    if (error) return <p>Error: {error}</p>;

    const graphDataArray = Array.isArray(graphDataPayload?.graph_data)
        ? graphDataPayload.graph_data
        : [];

    const fontamentdata = Array.isArray(graphDataPayload?.full_data)
        ? graphDataPayload.full_data
        : [];

    if (graphDataArray.length === 0) return <p className='text-center'>Loading...</p>;


    const formatXaxisLabels = (timeframe: string) => {
        let categories: string[] = [];

        if (timeframe === "1d") {
            categories = graphDataArray.map((data: any) => {
                const date = new Date(data.date);
                return date.toLocaleTimeString().slice(0, 5);
            }).filter((label, index, self) => self.indexOf(label) === index);
        } else if (timeframe === "1w") {
            categories = graphDataArray.map((data: any) => {
                const date = new Date(data.date);
                return date.toLocaleDateString("en-US", { month: 'short', day: 'numeric' });
            }).filter((label, index, self) => self.indexOf(label) === index);
            categories = categories.slice(0, 7);
        } else if (timeframe === "1m") {
            categories = graphDataArray.map((data: any) => {
                const date = new Date(data.date);
                const day = date.getDate();
                const month = date.toLocaleString('en-US', { month: 'short' });
                return `${day}'${month}`;
            }).filter((label, index, self) => self.indexOf(label) === index);
        }
        else if (timeframe === "1y") {
            const uniqueMonths = new Map();
            graphDataArray.forEach((data: any) => {
                if (!data.month) return;

                const [year, month] = data.month.split("-");
                const monthName = new Date(`${year}-${month}-01`).toLocaleString('en-US', { month: 'short' });
                const shortYear = year.slice(-2);
                const formattedDate = `${monthName}'${shortYear}`;

                if (!uniqueMonths.has(formattedDate)) {
                    uniqueMonths.set(formattedDate, formattedDate);
                }
            });
            categories = Array.from(uniqueMonths.values());
        }

        else if (timeframe === "max" || timeframe === "all") {
            categories = graphDataArray.map((data: any) => {
                const date = new Date(data.month);
                const month = date.toLocaleString('en-US', { month: 'short' });
                const year = date.getFullYear().toString().slice(-2);

                return `${month}'${year}`;
            }).filter((label, index, self) => self.indexOf(label) === index);
        }
        return categories;
    };


    const chartData = {
        options: {
            chart: {
                id: 'stock-price-chart',
                type: 'line',
                toolbar: { show: true },
            },
            xaxis: {
                categories: formatXaxisLabels(timeframe),
                labels: {
                    show: true,
                    rotate: -45,
                    rotateAlways: true,
                    style: {
                        fontSize: '12px',
                        colors: undefined,
                    },
                },
                tickAmount: 6,
                min: 0,
                max: graphDataArray.length - 1,
            },
            yaxis: {
                labels: {
                    formatter: (value: number) => `$${value.toFixed(2)}`,
                },
                title: {
                    text: 'Price (USD)',
                },
            },
            tooltip: {
                x: { format: 'MMM dd, yyyy' },
                y: {
                    formatter: (value: number) => `$${value.toFixed(2)}`,
                },
            },
        },
        series: [
            {
                name: `${symbol} Stock Price`,
                data: graphDataArray.map((data: any) => data.close),
            },
        ],
    };

    function formatNumber(num: any): string {
        if (!num || isNaN(num)) return "N/A";
        const parsedNum = parseFloat(num);
        if (parsedNum >= 1e9) return (parsedNum / 1e9).toFixed(2) + "B";
        if (parsedNum >= 1e6) return (parsedNum / 1e6).toFixed(2) + "M";
        if (parsedNum >= 1e3) return (parsedNum / 1e3).toFixed(2) + "K";
        return parsedNum.toFixed(2);
    }


    return (
        <section className=''>
            <div className="container">
                <div className="row py-md-5">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-body">
                                <h4 className="pt-2">
                                    {fontamentdata[0]?.Price
                                        ? `$${parseFloat(fontamentdata[0]?.Price.replace("USD", "").trim())}`
                                        : "-"}
                                </h4>
                                <div className="timeframe-buttons pb-3">
                                    {["1d", "1w", "1m", "1y", "max"].map((tf) => (
                                        <button
                                            key={tf}
                                            onClick={() => setTimeframe(tf)}
                                            className={`btn ${timeframe === tf ? "btn-primary" : "btn-secondary"} mx-1`}
                                        >
                                            {tf.toUpperCase()}
                                        </button>
                                    ))}
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
                                            <strong>{fontamentdata[0]?.Price
                                                ? `$${parseFloat(fontamentdata[0]?.Price.replace("USD", "").trim())}`
                                                : "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Market Cap</span>
                                            <br />
                                            <strong>$ {fontamentdata[0]?.MarketCap || "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">P/E Ratio</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.PE || "N/A"} X</strong>
                                        </div>
                                    </div>

                                    <div className="row pb-3">
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">WeekHigh52</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.YearHigh || "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">YearLow</span>
                                            <br />
                                            <strong>$ {fontamentdata[0]?.EPS || "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">P/B Ratio</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.EPS || "N/A"} X</strong>
                                        </div>
                                    </div>

                                    <div className="row pb-3">
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Beta</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.Beta || "N/A"} X</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">P/S</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.RSI || "N/A"} X</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Volume</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.Volume || "N/A"}</strong>
                                        </div>
                                    </div>

                                    <div className="row pb-3">
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Revenue</span>
                                            <br />
                                            <strong>$ {fontamentdata[0]?.revenueGrowth ? formatNumber(fontamentdata[0]?.revenueGrowth) : "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Earnings</span>
                                            <br />
                                            <strong>$ {fontamentdata[0]?.EarningGrowthTTM ? formatNumber(fontamentdata[0]?.EarningGrowthTTM) : "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Gross Margin</span>
                                            <br />
                                            <strong>
                                                {fontamentdata[0]?.FreeCashFlowPerShareTTM ? `${(parseFloat(fontamentdata[0]?.FreeCashFlowPerShareTTM) * 100).toFixed(2)}%` : "N/A"}
                                            </strong>
                                        </div>
                                    </div>

                                    <div className="row pb-3">
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">One Day Volatility</span>
                                            <br />
                                            <strong>
                                                {fontamentdata[0]?.OneDayVolatility
                                                    ? `${(parseFloat(fontamentdata[0]?.OneDayVolatility) * 100).toFixed(2)}%`
                                                    : "N/A"}
                                            </strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Profit Margin</span>
                                            <br />
                                            <strong>
                                                {fontamentdata[0]?.ProfitMarginsTTM
                                                    ? `${(parseFloat(fontamentdata[0]?.ProfitMarginsTTM) * 100).toFixed(2)}%`
                                                    : "N/A"}
                                            </strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Debt To Equity</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.DebtEquityRatioTTM ? `${fontamentdata[0]?.DebtEquityRatioTTM}%` : "N/A"}</strong>
                                        </div>
                                    </div>

                                    <div className="row pb-3">
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Operating Cash Flow</span>
                                            <br />
                                            <strong>$ {fontamentdata[0]?.operatingCashFlow ? formatNumber(fontamentdata[0]?.operatingCashFlow) : "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Payout Ratio</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.PayoutRatioTTM || "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Latest Quarter</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.PriceToBookRatioTTM || "N/A"}</strong>
                                        </div>
                                    </div>

                                    <div className="row pb-3">
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Ex Dividend</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.DividendYieldTTM || "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Net Income Growth</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.NetIncomeGrowth || "N/A"}</strong>
                                        </div>
                                        <div className="col-12 col-sm-6 col-md-4">
                                            <span className="stock-details-p">Sector</span>
                                            <br />
                                            <strong>{fontamentdata[0]?.Sector || "N/A"}</strong>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

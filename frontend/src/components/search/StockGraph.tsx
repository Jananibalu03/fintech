import { useState, useEffect, useRef } from "react";
import ApexCharts from "react-apexcharts";
import { useDispatch, useSelector } from "react-redux";
import { graphData } from "./SearchSlice";
import { RootState, AppDispatch } from "../../store/Store";


interface StockData {
    date: string;
    close: number;
}


export default function StockGraph({ symbol }: { symbol: string }) {
    const [timeframe, setTimeframe] = useState<string>("1w");
    const stockData = useSelector((state: RootState) => state.search.graphDataPayload);
    console.log("1", stockData);

    const loading = useSelector((state: RootState) => state.search.loading);
    const dispatch = useDispatch<AppDispatch>();

    const hasFetched = useRef<Set<string>>(new Set());

    useEffect(() => {
        if (!symbol || !timeframe || loading) return;

        const dataKey = `${symbol}-${timeframe}`; // Unique key for each symbol-timeframe combination

        if (!hasFetched.current.has(dataKey)) {
            hasFetched.current.add(dataKey); // Mark this combination as fetched

            dispatch(graphData({ symbol, range_type: timeframe }));
        }
    }, [symbol, timeframe, loading, dispatch]);

    const stockDatas: StockData[] = stockData?.[symbol]?.[timeframe] || [];

    console.log("wwwwwww", stockDatas);

    const chartData = {
        options: {
            chart: { id: "stock-price-chart", type: "line", zoom: { enabled: true }, toolbar: { show: true } },
            xaxis: { categories: stockDatas.map((data) => data.date) },
            tooltip: { x: { format: "MMM yyyy" } },
        },
        series: [{ name: `${symbol} Stock Price`, data: stockDatas.map((data) => data.close) }],
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
        <div className="container">
            <div className="row py-md-5">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h4>${stockData?.[symbol]?.price ?? "N/A"}</h4>
                            <div className="timeframe-buttons">
                                {["1w", "1m", "3m", "1y", "all"].map((tf) => (
                                    <button
                                        key={tf}
                                        onClick={() => setTimeframe(tf)}
                                        className={`btn ${timeframe === tf ? "btn-primary" : "btn-secondary"}`}
                                    >
                                        {tf.toUpperCase()}
                                    </button>
                                ))}
                            </div>

                            <div style={{ position: "relative", height: "350px" }}>
                                {loading && (
                                    <div
                                        style={{
                                            position: "absolute",
                                            top: "50%",
                                            left: "50%",
                                            transform: "translate(-50%, -50%)",
                                            fontSize: "18px",
                                            fontWeight: "bold",
                                            color: "#000",
                                        }}
                                    >
                                        Loading...
                                    </div>
                                )}
                                <ApexCharts options={chartData.options} series={chartData.series} type="line" height={350} />
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
                                        <strong>$ {formatNumber(stockData?.[symbol]?.price)}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Market Cap</span>
                                        <br />
                                        <strong>$ {formatNumber(stockData?.[symbol]?.marketCap)}</strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">P/E Ratio</span>
                                        <br />
                                        <strong>{stockData?.[symbol]?.peRatio || "N/A"} X</strong>
                                    </div>
                                </div>

                                <div className="row pb-3">
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Operating Margin</span>
                                        <br />
                                        <strong>
                                            {stockData?.[symbol]?.operatingMargin
                                                ? `${(parseFloat(stockData[symbol].operatingMargin) * 100).toFixed(2)}%`
                                                : "N/A"}
                                        </strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Profit Margin</span>
                                        <br />
                                        <strong>
                                            {stockData?.[symbol]?.profitMargin
                                                ? `${(parseFloat(stockData[symbol].profitMargin) * 100).toFixed(2)}%`
                                                : "N/A"}
                                        </strong>
                                    </div>
                                    <div className="col-12 col-sm-6 col-md-4">
                                        <span className="stock-details-p">Dividend Yield</span>
                                        <br />
                                        <strong>
                                            {stockData?.[symbol]?.dividendYield ? `${stockData[symbol].dividendYield}%` : "N/A"}
                                        </strong>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}

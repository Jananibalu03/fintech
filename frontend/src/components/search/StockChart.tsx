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
                return date.toLocaleTimeString().slice(0, 5); // Hourly labels (HH:mm)
            }).filter((label, index, self) => self.indexOf(label) === index); // Remove duplicate labels
        } else if (timeframe === "1w") {
            categories = graphDataArray.map((data: any) => {
                const date = new Date(data.date);
                return date.toLocaleDateString("en-US", { month: 'short', day: 'numeric' });
            }).filter((label, index, self) => self.indexOf(label) === index); // Remove duplicate dates
            categories = categories.slice(0, 7); // Limit to 7 days
        } else if (timeframe === "1m") {
            categories = graphDataArray.map((data: any) => {
                const date = new Date(data.date);
                const day = date.getDate();
                const month = date.toLocaleString('en-US', { month: 'short' });
                return `${day}'${month}`;
            }).filter((label, index, self) => self.indexOf(label) === index);
        }
        else if (timeframe === "1y") {
            categories = graphDataArray.map((data: any) => {
                const date = new Date(data.date);
                const day = date.getDate();
                const month = date.toLocaleString('en-US', { month: 'short', year: "2-digit" });
                return `${day}'${month}`;
            }).filter((label, index, self) => self.indexOf(label) === index);
        }

        else if (timeframe === "max" || timeframe === "all") {
            categories = graphDataArray.map((data: any) => {
                const date = new Date(data.date);
                const day = date.getDate();
                const month = date.toLocaleString('en-US', { month: 'short', year: "2-digit" });
                return `${day}'${month}`;
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
                categories: formatXaxisLabels(timeframe), // Dynamically updated categories
                labels: {
                    show: true,
                    rotate: -45, // Rotate labels for better readability
                    rotateAlways: true, // Keep labels rotated
                    style: {
                        fontSize: '12px', // Adjust font size for readability
                        colors: undefined, // Set label color if needed
                    },
                },
                tickAmount: 6, // Adjust number of ticks if needed
                min: 0, // Ensure the axis starts at the first data point
                max: graphDataArray.length - 1, // Ensure the axis ends at the last data point
            },
            yaxis: {
                labels: {
                    formatter: (value: number) => `$${value.toFixed(2)}`, // Format Y-axis labels as currency
                },
                title: {
                    text: 'Price (USD)', // Y-axis title
                },
            },
            tooltip: {
                x: { format: 'MMM dd, yyyy' },
                y: {
                    formatter: (value: number) => `$${value.toFixed(2)}`, // Format tooltip values
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


    return (
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
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}

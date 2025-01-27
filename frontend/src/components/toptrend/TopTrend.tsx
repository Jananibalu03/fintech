import { useNavigate } from 'react-router-dom';

export default function TopTrend() {
    const navigate = useNavigate();

    const trends = [
        { title: "Volatility", description: "Stocks with high price swings, offering great opportunities for short-term gains.", path: "/VolatilityDetails" },
        { title: "52 Week High", description: "Top stocks that have reached their highest price in the past year.", path: "/52-week-high-stocks" },
        { title: "52 Week Low", description: "Stocks trading near their 1-year lows, potentially undervalued.", path: "/52-week-low-stocks" },
        { title: "Low P/E Ratio", description: "Stocks with a low price-to-earnings ratio, indicating they may be undervalued.", path: "/low-pe-ratio" },
        { title: "Today’s Top Gain", description: "Stocks with the highest growth in value today, offering quick profit potential.", path: "/top-gain" },
        { title: "Today’s Top Loss", description: "Stocks with big losses today may offer discounted buying opportunities.", path: "/top-loss" },
        { title: "Top Perform", description: "Stocks with the best performance overall, indicating strong market position.", path: "/top-perform" },
        { title: "Best Stocks Under $10", description: "Stocks under $10, ideal for those looking for low-cost opportunities with potential upside.", path: "/best-stocks-under-$10" },
        { title: "Under $50", description: "Stocks priced under $50, offering a balance between affordability and growth potential.", path: "/best-stocks-under-$50" },
        { title: "Negative Beta", description: "Stocks that tend to move opposite of the overall market, useful for hedging risk.", path: "/negative-beta" },
        { title: "Low Beta", description: "Stocks with low volatility compared to the market, ideal for conservative investors.", path: "/lowbeta" },
        { title: "High Risk, High Reward", description: "Stocks that offer significant risk but also potential for large returns.", path: "/high-risk-high-reward" },
        { title: "Debit-Free Stocks", description: "Stocks with low or no debt, making them safer investments with stable returns.", path: "/debitfree" },
        { title: "Dividend", description: "Stocks offering reliable dividend payments, ideal for income-focused investors.", path: "/dividend" },
       
        { title: "High Dividend Yield", description: "High-dividend stocks offer strong returns for income investors.", path: "/high-dividend" },
    ];

    return (
        <section>
            <div className="top-trend p-5">
                <h3 className="ps-md-5">Top Trend</h3>
            </div>
            <div className="container">
                <div className="row d-flex justify-content-center mb-5">
                    {trends.map((trend, index) => (
                        <div key={index} className="col-md-4 new-caed mt-4">
                            <div className="card custom-card" onClick={() => navigate(trend.path)}>
                                <div className="card-body p-4">
                                    <h4>{trend.title}</h4>
                                    <br />
                                    <p>{trend.description}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

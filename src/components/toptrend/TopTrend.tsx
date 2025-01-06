import { useNavigate } from 'react-router-dom';

export default function TopTrend() {
    const navigate = useNavigate();

    const handleCardClick = () => {
        navigate('/search');
    };


    const handleVolatilityDetails = () => {
        navigate('/VolatilityDetails');
    };

    const handle52weekshigh = () => {
        navigate('/52-week-high-stocks');
    }

    const handle52weekslow = () => {
        navigate('/52-week-low-stocks');
    }


    const handleunderten = () => {
        navigate('/52-week-low-stocks');
    }

    return (
        <section>
            <div className='top-trend p-5'>
                <h3 className='ps-md-5'>Top Trend</h3>
            </div>

            <div className="container">
                <div className="row d-flex justify-content-center mb-5">

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleVolatilityDetails}>
                            <div className="card-body p-4">
                                <h4>Volatility</h4><br />
                                <p>Stocks with high price swings, offering great opportunities for short-term gains.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handle52weekshigh}>
                            <div className="card-body p-4">
                                <h4>52 Week High</h4><br />
                                <p>Top stocks that have reached their highest price in the past year.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handle52weekslow}>
                            <div className="card-body p-4">
                                <h4>52 Week Low</h4><br />
                                <p>Stocks trading near their 1-year lows, potentially undervalued.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleunderten}>
                            <div className="card-body p-4">
                                <h4>Best Stocks Under $10</h4><br />
                                <p>Stocks under $10, ideal for those looking for low-cost opportunities with potential upside.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>Under $50</h4><br />
                                <p>Stocks priced under $50, offering a balance between affordability and growth potential.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>Negative Beta</h4><br />
                                <p>Stocks that tend to move opposite of the overall market, useful for hedging risk.</p>
                            </div>
                        </div>
                    </div>


                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>Low Beta</h4><br />
                                <p>Stocks with low volatility compared to the market, ideal for conservative investors.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>High Risk, High Reward</h4><br />
                                <p>Stocks that offer significant risk but also potential for large returns.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>Debit-Free Stocks</h4><br />
                                <p>Stocks with low or no debt, making them safer investments with stable returns.</p>
                            </div>
                        </div>
                    </div>


                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>Dividend</h4><br />
                                <p>Stocks offering reliable dividend payments, ideal for income-focused investors.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>Low P/E Ratio</h4><br />
                                <p>Stocks with a low price-to-earnings ratio, indicating they may be undervalued.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>Today’s Top Gain</h4><br />
                                <p>Stocks with the highest growth in value today, offering quick profit potential.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>Today’s Top Loss</h4><br />
                                <p>Stocks with big losses today may offer discounted buying opportunities.</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>Top Perform</h4><br />
                                <p>Stocks with the best performance overall, indicating strong market position.</p>
                            </div>
                        </div>
                    </div>


                    <div className="col-md-4 new-caed mt-4">
                        <div className="card custom-card" onClick={handleCardClick}>
                            <div className="card-body p-4">
                                <h4>High Dividend Yield</h4><br />
                                <p>High-dividend stocks offer strong returns for income investors.</p>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </section>
    );
}

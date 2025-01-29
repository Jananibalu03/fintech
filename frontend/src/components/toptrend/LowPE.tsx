import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { lowperatio } from './TopTrendSlice';

interface Stock {
  Symbol: string;
  Name: string;
  Price: string;
  Change: string;
  Volume: string;
  MarketCap: string;
  Beta: number;
  PERatio: number;
  FreeCashFlowTTM: string;
  ProfitMarginsTTM: string;
  DividendPayoutRatioTTM: string;
  RevenueGrowthTTM: string;
  DebtToEquityRatioTTM: string;
  PriceToBookRatioTTM: string;
  ProfitMarginTTM: string;
  Sector: string;
}

export default function LowPE() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [sortConfig, setSortConfig] = useState<{
    key: keyof Stock | null;
    direction: 'ascending' | 'descending';
  }>({
    key: null,
    direction: 'ascending',
  });
  const [searchTerm, setSearchTerm] = useState('');

  const dispatch = useDispatch();

  useEffect(() => {
    dispatch<any>(lowperatio({ page: 1, limit: 10 })).then((data: any) => {
      setStocks(data.payload);
    });
  }, [dispatch]);

  const handleSort = (key: keyof Stock) => {
    setSortConfig((prevState) => ({
      key,
      direction:
        prevState.key === key && prevState.direction === 'ascending'
          ? 'descending'
          : 'ascending',
    }));
  };

  const getSortIcon = (key: keyof Stock) =>
    sortConfig.key === key ? (sortConfig.direction === 'ascending' ? ' ▲' : ' ▼') : '';

  const filteredStocks = stocks.filter((stock) =>
    Object.values(stock).some((val) => val.toString().toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const sortedStocks = [...filteredStocks].sort((a, b) => {
    if (!sortConfig.key) return 0;
    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];
    if (aValue < bValue) return sortConfig.direction === 'ascending' ? -1 : 1;
    if (aValue > bValue) return sortConfig.direction === 'ascending' ? 1 : -1;
    return 0;
  });

  const columns = [
    { key: 'Symbol', label: 'Symbol' },
    { key: 'Name', label: 'Stock Name' },
    { key: 'Price', label: 'Current Price' },
    { key: 'Change', label: 'Change' },
    { key: 'Volume', label: 'Volume' },
    { key: 'MarketCap', label: 'Market Cap' },
    { key: 'Beta', label: 'Beta' },
    { key: 'PERatio', label: 'PE Ratio' },
    { key: 'FreeCashFlowTTM', label: 'Free Cash Flow TTM' },
    { key: 'ProfitMarginsTTM', label: 'Profit Margins TTM' },
    { key: 'DividendPayoutRatioTTM', label: 'Dividend Payout Ratio TTM' },
    { key: 'RevenueGrowthTTM', label: 'Revenue Growth TTM' },
    { key: 'DebtToEquityRatioTTM', label: 'Debt To Equity Ratio TTM' },
    { key: 'PriceToBookRatioTTM', label: 'Price To Book Ratio TTM' },
    { key: 'ProfitMarginTTM', label: 'Profit Margin TTM' },
    { key: 'Sector', label: 'Sector' },
  ];

  return (
    <section>
      <div className="d-flex toptrend-sub-banner p-5">
        <div className="container">
          <div className="row d-flex justify-content-between">
            <div className="col-md-8">
              <h3>Low PE Stocks</h3>
              <p>Explore stocks with low price-to-earnings ratios.</p>
            </div>
            <div className="col-md-3 text-end my-4">
              <input
                type="text"
                placeholder="Search stocks..."
                className="form-control"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="container mb-5">
        <div style={{ overflowX: 'auto' }}>
          <table className="table table-bordered mb-0">
            <thead>
              <tr>
                {columns.map(({ key, label }) => (
                  <th
                    key={key}
                    onClick={() => handleSort(key as keyof Stock)}
                    style={{ padding: '20px', whiteSpace: 'nowrap', cursor: 'pointer' }}
                    aria-label={`Sort by ${label}`}
                  >
                    {label} {getSortIcon(key as keyof Stock)}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {sortedStocks.length > 0 ? (
                sortedStocks.map((stock, index) => (
                  <tr key={index}>
                    <td>{stock.Symbol}</td>
                    <td>{stock.Name}</td>
                    <td>{stock.Price || 'Data not available'}</td>
                    <td>{stock.Change || 'Data not available'}</td>
                    <td>{stock.Volume || 'Data not available'}</td>
                    <td>{stock.MarketCap || 'Data not available'}</td>
                    <td>{stock.Beta || 'Data not available'}</td>
                    <td>{stock.PERatio || 'Data not available'}</td>
                    <td>{stock.FreeCashFlowTTM || 'Data not available'}</td>
                    <td>{stock.ProfitMarginsTTM || 'Data not available'}</td>
                    <td>{stock.DividendPayoutRatioTTM || 'Data not available'}</td>
                    <td>{stock.RevenueGrowthTTM || 'Data not available'}</td>
                    <td>{stock.DebtToEquityRatioTTM || 'Data not available'}</td>
                    <td>{stock.PriceToBookRatioTTM || 'Data not available'}</td>
                    <td>{stock.ProfitMarginTTM || 'Data not available'}</td>
                    <td>{stock.Sector || 'Data not available'}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={10} style={{ textAlign: 'center' }}>
                    No data available
                  </td>
                </tr>
              )}

            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

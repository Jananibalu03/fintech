import { useState, useEffect } from 'react';
import { Pagination } from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import { hignin52 } from './TopTrendSlice';
import { RootState } from '../../store/Store';

export default function HighWeeks52() {
  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);

  const dispatch = useDispatch();
  const hignin52Payload = useSelector((state: RootState) => state.TopTrend.hignin52Payload || []);

  useEffect(() => {
    dispatch(hignin52({ page: currentPage, limit: itemsPerPage }));
  }, [dispatch, currentPage, itemsPerPage]);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    dispatch(hignin52({ page, limit: itemsPerPage }));
  };


  const handleSort = (key: string) => {
    const direction =
      sortConfig.key === key && sortConfig.direction === "asc" ? "desc" : "asc";
    setSortConfig({ key, direction });
  };


  const parseValue = (value: any) => {
    if (value == null || value === '') return 0;  // Return a default value for null or empty values
    if (typeof value === 'string') {
      // Remove any non-numeric characters for strings
      return !isNaN(value.replace(/[^\d.-]/g, '')) ? parseFloat(value.replace(/[^\d.-]/g, '')) : value.toLowerCase();
    }
    return value;  // Return the value as-is if it's a number
  };

  const getSortIcon = (column: string) => {
    if (!sortConfig || sortConfig.key !== column) return '';  // No sorting
    return sortConfig.direction === 'asc' ? '▲' : '▼';  // Show up/down arrow
  };


  const columnHeaders = [
    { displayName: 'Symbol', dataKey: 'symbol' },
    { displayName: 'Stock Name', dataKey: 'stockName' },
    { displayName: 'Current Price', dataKey: 'currentPrice' },
    { displayName: '52 Weeks High', dataKey: 'high52Weeks' },
    { displayName: '52 Weeks Low', dataKey: 'low52Weeks' },
    { displayName: 'Change', dataKey: 'change' },
    { displayName: 'Volume', dataKey: 'volume' },
    { displayName: 'Beta', dataKey: 'beta' },
    { displayName: 'Sector', dataKey: 'sector' },
    { displayName: 'Market Cap', dataKey: 'marketCap' },
    { displayName: 'SMA50', dataKey: 'sma50' },
    { displayName: 'SMA200', dataKey: 'sma200' },
    { displayName: 'RSI', dataKey: 'rsi' },
    { displayName: 'Dividend Yield', dataKey: 'dividendYield' },
    { displayName: '1D Change', dataKey: 'change1D' },
    { displayName: '1M Change', dataKey: 'change1M' },
    { displayName: '1Y Change', dataKey: 'change1Y' },
  ];

  const data = Array.isArray(hignin52Payload) ? hignin52Payload : [hignin52Payload];

  const filteredData = data.filter((stock: any) => {
    const symbol = stock.symbol || ''; // Adjust to match API field names
    const stockName = stock.stockName || '';
    return (
      symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
      stockName.toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  const sortedData = [...filteredData].sort((a, b) => {
    if (!sortConfig || !sortConfig.key) return 0;
    const aValue = parseValue(a[sortConfig.key]);
    const bValue = parseValue(b[sortConfig.key]);
    if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
    return 0;
  });

  const getNumberColor = (value: number | string) => {
    const numericValue = Number(value);
    if (isNaN(numericValue)) return "";
    if (numericValue < 0) return "text-danger";
    if (numericValue > 0) return "text-success";
    return "";
  };


  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentItems = sortedData.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <section>
      <div className="d-flex toptrend-sub-banner p-5">
        <div className="container">
          <div className="row d-flex justify-content-between">
            <div className="col-md-8">
              <h3>52 Weeks High Stocks</h3>
              <p>List of stocks with their 52-week highs, low prices, and other stock data.</p>
            </div>
            <div className="col-md-3 text-end my-4">
              <input
                type="text"
                placeholder="Search stocks..."
                className="form-control"
                onChange={(e) => setSearchTerm(e.target.value)}
                value={searchTerm}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="container mb-5">
        <div style={{ overflowX: 'auto' }}>
          <table className="table table-bordered table-hover mb-md-0" style={{ borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                {columnHeaders.map(({ displayName, dataKey }) => (
                  <th
                    key={dataKey}
                    style={{ padding: '20px', whiteSpace: 'nowrap', cursor: 'pointer' }}
                    onClick={() => handleSort(dataKey)}
                  >
                    {displayName} {getSortIcon(dataKey)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {currentItems.length > 0 ? (
                currentItems.map((stock, index) => (
                  <tr key={`${stock.Symbol}-${index}`}>
                    <td style={{ padding: '12px', cursor: 'pointer' }} className="table-active">{stock.Symbol}</td>
                    <td style={{ padding: '12px' }}>{stock.Name}</td>
                    <td style={{ padding: '12px' }}>${stock.Price}</td>
                    <td style={{ padding: '12px' }}>${stock['52WeeksHigh']}</td>
                    <td style={{ padding: '12px' }}>${stock['52WeeksLow']}</td>
                    <td
                      style={{
                        padding: '12px',
                        color: stock.Change < 0 ? 'red' : 'green',
                      }}
                    >
                      {stock.Change}
                    </td>
                    <td style={{ padding: '12px' }}>{stock.Volume}</td>
                    <td style={{ padding: '12px' }}>{stock.Beta}</td>
                    <td style={{ padding: '12px' }}>{stock.Sector}</td>
                    <td style={{ padding: '12px' }}>{stock.MarketCap}</td>
                    <td style={{ padding: '12px' }}>{stock.SMA50}</td>
                    <td style={{ padding: '12px' }}>{stock.SMA200}</td>
                    <td style={{ padding: '12px' }}>{stock.RSI}</td>
                    <td style={{ padding: '12px' }}>{stock.DividendYieldTTM}</td>
                    <td
                      style={{
                        padding: '12px',
                        color: stock['1D'] < 0 ? 'red' : 'green',
                      }}
                    >
                      {stock['1D']}
                    </td>
                    <td
                      style={{
                        padding: '12px',
                        color: stock['1M'] < 0 ? 'red' : 'green',
                      }}
                    >
                      {stock['1M']}
                    </td>
                    <td
                      style={{
                        padding: '12px',
                        color: stock['1Y'] < 0 ? 'red' : 'green',
                      }}
                    >
                      {stock['1Y']}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={columnHeaders.length} style={{ textAlign: 'center' }}>No data available</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="d-flex justify-content-center m-3">
          <Pagination
            current={currentPage}
            pageSize={itemsPerPage}
            total={filteredData.length}
            onChange={handlePageChange}
            showSizeChanger={false}
          />
        </div>
      </div>
    </section>
  );
}

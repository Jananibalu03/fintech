import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { lowperatio } from './TopTrendSlice';
import { RootState } from '../../store/Store';
import { Pagination } from 'antd';


export default function LowPE() {

  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({
    key: "",
    direction: "asc",
  });

  const dispatch = useDispatch();
  const { lowperatioPayload, loading } = useSelector(
    (state: RootState) => state.TopTrend
  );

  function debounce<T extends (...args: any[]) => void>(func: T, delay: number): T {
    let timer: ReturnType<typeof setTimeout>;
    return function (this: any, ...args: Parameters<T>) {
      clearTimeout(timer);
      timer = setTimeout(() => func.apply(this, args), delay);
    } as T;
  }

  const fetchData = debounce((Search, page) => {
    dispatch<any>(lowperatio({ Search, page, limit: itemsPerPage }));
  }, 500);

  useEffect(() => {
    fetchData(searchTerm, currentPage);
  }, [searchTerm, currentPage, dispatch]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const filteredData = (lowperatioPayload?.data || lowperatioPayload || []).filter((item: any) =>
    item.Name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.Symbol?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedData = [...filteredData].sort((a, b) => {
    if (sortConfig.key) {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];
      if (aValue < bValue) return sortConfig.direction === "asc" ? -1 : 1;
      if (aValue > bValue) return sortConfig.direction === "asc" ? 1 : -1;
    }
    return 0;
  });

  const currentItems = sortedData;

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const handleSort = (key: string) => {
    const direction =
      sortConfig.key === key && sortConfig.direction === "asc" ? "desc" : "asc";
    setSortConfig({ key, direction });
  };

  const getNumberColor = (value: number | string) => {
    const numericValue = Number(value);
    if (isNaN(numericValue)) return "";
    if (numericValue < 0) return "text-danger";
    if (numericValue > 0) return "text-success";
    return "";
  };

  const columns = [
    { key: 'Symbol', label: 'Symbol' },
    { key: 'Name', label: 'Stock Name' },
    { key: 'Price', label: 'Current Price' },
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
                onChange={handleSearchChange}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="container mb-5">
        <div className="table-responsive mb-0" style={{ overflowX: 'auto' }}>
          <table className="table table-hover table-bordered mb-0">
            <thead>
              <tr>
                {columns.map((header) => (
                  <th
                    key={header.key}
                    onClick={() => handleSort(header.key)}
                    style={{ padding: "20px", whiteSpace: "nowrap", cursor: "pointer" }}
                  >
                    {header.label}
                    {sortConfig.key === header.key ? (
                      sortConfig.direction === "asc" ? (
                        " ▲"
                      ) : (
                        " ▼"
                      )
                    ) : (
                      ""
                    )}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {currentItems.length > 0 ? (
                currentItems.map((stock, index) => (
                  <tr key={index}>
                    <td style={{ padding: '12px', cursor: "pointer" }} className='table-active'>{stock.Symbol}</td>
                    <td>{stock.Name}</td>
                    <td className={getNumberColor(stock.Price)}>{stock.Price}</td>

                    <td>{stock.Volume}</td>
                    <td>{stock.MarketCap}</td>
                    <td>{stock.Beta}</td>
                    <td className={getNumberColor(stock.PERatio)}>{stock.PERatio}</td>
                    <td className={getNumberColor(stock.FreeCashFlowTTM)}>{stock.FreeCashFlowTTM}</td>
                    <td>{stock.ProfitMarginsTTM}</td>
                    <td className={getNumberColor(stock.DividendPayoutRatioTTM)}>{stock.DividendPayoutRatioTTM}</td>
                    <td>{stock.RevenueGrowthTTM}</td>
                    <td className={getNumberColor(stock.DebtToEquityRatioTTM)}>{stock.DebtToEquityRatioTTM}</td>
                    <td className={getNumberColor(stock.PriceToBookRatioTTM)}>{stock.PriceToBookRatioTTM}</td>
                    <td>{stock.ProfitMarginTTM}</td>
                    <td>{stock.Sector}</td>
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
        <div className="d-flex justify-content-center m-3">
          <Pagination
            current={currentPage}
            pageSize={itemsPerPage}
            onChange={handlePageChange}
            showSizeChanger={false}
            total={lowperatioPayload?.totalCount || 100}
          />

        </div>
      </div>
    </section>
  );
}

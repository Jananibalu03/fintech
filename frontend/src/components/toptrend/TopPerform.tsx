import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store/Store';
import { topperform } from './TopTrendSlice';
import { Pagination } from 'antd';


export default function TopPerform() {

  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: "", direction: 'asc' });


  const dispatch = useDispatch();
  const { topperformPayload, loading } = useSelector(
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
    dispatch<any>(topperform({ Search, page, limit: itemsPerPage }));
  }, 500);


  useEffect(() => {
    fetchData(searchTerm, currentPage);
  }, [searchTerm, currentPage, dispatch]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const filteredData = (topperformPayload?.data || topperformPayload || []).filter((item: any) =>
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

  const headers = [
    { label: "Symbol", key: "Symbol" },
    { label: "Name", key: "Name" },
    { label: "Price", key: "Price" },

    { label: 'DayHigh', key: 'DayHigh' },
    { label: 'DayLow', key: 'DayLow' },
    { label: "1D", key: "1D" },
    { label: "1M", key: "1M" },
    { label: "1Y", key: "1Y" },
    { label: "Volume", key: "Volume" },
    { label: "MarketCap", key: "Marketap" },
    { label: '52 Weeks High', key: '52WeeksHigh' },
    { label: '52 Weeks Low', key: '52WeeksLow' },
    { label: "SMA50", key: "SMA50" },
    { label: "SMA200", key: "SMA200" },
    { label: "Beta", key: "Beta" },
    { label: "PERatio", key: "PERatio" },
    { label: "EPS", key: "EPS" },
    { label: "RSI", key: "RSI" },
    { label: "FreeCashFlowTTM", key: "FreeCashFlowTTM" },
    { label: "ProfitMarginsTTM", key: "ProfitMarginsTTM" },
    { label: "DividendYieldTTM", key: "DividendYieldTTM" },
    { label: "RevenueGrowthTTM", key: "RevenueGrowthTTM" },
    { label: "Sector", key: "Sector" },
  ];

  const getNumberColor = (value: number | string) => {
    const numericValue = Number(value);
    if (isNaN(numericValue)) return "";
    if (numericValue < 0) return "text-danger";
    if (numericValue > 0) return "text-success";
    return "";
  };


  return (
    <section>

      <div className="d-flex toptrend-sub-banner p-5">
        <div className="container">
          <div className="row d-flex justify-content-between">
            <div className="col-md-8">
              <h3>Top Performing Stocks</h3>
              <p>Stocks that have gained the Top Performing Stocks</p>
            </div>

            <div className="col-md-3 text-end my-4">
              <input
                type="text"
                placeholder="Search stocks..."
                value={searchTerm}
                onChange={handleSearchChange}
                className="form-control"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="container mb-5">
        {loading ? (
          <div className="d-flex justify-content-center">Loading...</div>
        ) : (
          <>
        <div style={{ overflowX: "auto" }}>
          <table className="table table-bordered table-hover mb-0">
            <thead>
              <tr>
                {headers.map((header) => (
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
                currentItems.map((stock: any) => (
                  <tr key={stock.Symbol}>
                    <td style={{ padding: '12px', cursor: "pointer" }} className="table-active">{stock.Symbol}</td>
                    <td style={{ padding: '12px', whiteSpace: 'nowrap' }}>{stock.Name}</td>
                    <td
                      style={{ cursor: "pointer" }}
                      className={getNumberColor(stock.Price)}
                    >
                      {stock.Price ? `$${parseFloat(stock.Price.replace("USD", "").trim())}` : "-"}
                    </td>

                    < td style={{
                      padding: '12px',
                      color: 'green',
                    }}> ${stock['DayHigh']} </td>
                    < td style={{
                      padding: '12px',
                      color: 'red',
                    }}> ${stock['DayLow']} </td>

                    <td className={getNumberColor(stock["1D"])}>{stock["1D"]}</td>
                    <td className={getNumberColor(stock["1M"])}>{stock["1M"]}</td>
                    <td className={getNumberColor(stock["1Y"])}>{stock["1Y"]}</td>
                    <td>{stock.Volume}</td>
                    <td>{stock.MarketCap}</td>
                    < td style={{
                      padding: '12px',
                      color: 'green',
                    }}> ${stock['52WeeksHigh']} </td>
                    < td style={{
                      padding: '12px',
                      color: 'red',
                    }}> ${stock['52WeeksLow']} </td>
                    <td>{stock.SMA50}</td>
                    <td>{stock.SMA200}</td>
                    <td>{stock.Beta}</td>
                    <td>{stock.PERatio}</td>
                    <td>{stock.EPS}</td>
                    <td>{stock.RSI}</td>
                    <td>{stock.FreeCashFlowTTM}</td>
                    <td>{stock.ProfitMarginsTTM}</td>
                    <td>{stock.DividendYieldTTM}</td>
                    <td>{stock.RevenueGrowthTTM}</td>
                    <td>{stock.Sector}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={13} className="text-center">
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
            total={topperformPayload?.totalCount || 100}
            onChange={handlePageChange}
            showSizeChanger={false}
          />
        </div>
          </>
        )}

      </div>
    </section>
  );
}

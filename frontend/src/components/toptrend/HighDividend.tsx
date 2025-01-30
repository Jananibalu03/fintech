import { useEffect, useState } from 'react';
import { Pagination } from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import { highdividend } from './TopTrendSlice';
import { RootState } from '../../store/Store';

export default function HighDividend() {

  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({
    key: "",
    direction: "asc",
  });

  const dispatch = useDispatch();
  const { highdividendPayload, error, loading } = useSelector(
    (state: RootState) => state.TopTrend
  );

  useEffect(() => {
    dispatch<any>(highdividend({ page: currentPage, limit: itemsPerPage }));
  }, [currentPage, dispatch]);


  const filteredData =
    (highdividendPayload?.data || highdividendPayload || []).filter((item: any) =>
      item.Name && item.Name.toLowerCase().includes(searchTerm.toLowerCase())
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
    { label: "Volume", key: "Volume" },
    { label: "MarketCap", key: "MarketCap" },
    { label: "52WeeksLow", key: "52WeeksLow" },
    { label: "52WeeksLow", key: "52WeeksLow" },
    { label: "Beta", key: "Beta" },
    { label: "PERatio", key: "PERatio" },
    { label: "EPS", key: "EPS" },
    { label: "PayoutRatioTTM", key: "PayoutRatioTTM" },
    { label: "DividendYieldTTM", key: "DividendYieldTTM" },
    { label: "DividendPerShareTTM", key: "DividendPerShareTTM" },
    { label: "RevenueGrowthTTM", key: "RevenueGrowthTTM" },
    { label: "NetIncomeGrowth", key: "NetIncomeGrowth" },
    { label: "FreeCashFlowTTM", key: "FreeCashFlowTTM" },
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
              <h3>Hign Dividend</h3>
              <p>Stocks with Hign Dividend, offering great opportunities for Long-term gains.</p>
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
        {error && <div className="alert alert-danger">{error}</div>}
        {loading ? (
          <div>Loading...</div>
        ) : (
          <>
            <div className="table-responsive mb-0">
              <table className="table table-hover table-bordered mb-0">
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
                    currentItems.map((stock, index) => (
                      <tr key={index}>
                        <td style={{ padding: '12px', cursor: "pointer" }} className='table-active'>{stock.Symbol}</td>
                        <td style={{ padding: '12px', cursor: "pointer" }}>{stock.Name}</td>
                        <td style={{ padding: '1px 20px', cursor: "pointer" }} className={getNumberColor(stock.Price)}>{stock.Price}</td>
                        <td>{stock.Volume}</td>
                        <td>{stock.MarketCap}</td>
                        < td style={{ padding: '12px' }}> ${stock['52WeeksHigh']} </td>
                        < td style={{ padding: '12px' }}> ${stock['52WeeksLow']} </td>
                        <td>{stock.Beta}</td>
                        <td>{stock.PERatio}</td>
                        <td>{stock.EPS}</td>
                        <td>{stock.PayoutRatioTTM}</td>
                        <td>{stock.DividendYieldTTM}</td>
                        <td>{stock.DividendPerShareTTM}</td>
                        <td>{stock.RevenueGrowthTTM}</td>
                        <td>{stock.NetIncomeGrowth}</td>
                        <td>{stock.FreeCashFlowTTM}</td>
                        <td>{stock.Sector}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={16} className="text-center">
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
                total={highdividendPayload?.totalCount || 100}
              />

            </div>
          </>
        )}
      </div>
    </section>
  );
}

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface ProfileState {
    loading: boolean;
    error: string | null;
    searchDataSuccess: boolean;
    searchDataPayload: any;
    stockDataSuccess: boolean;
    stockDataPayload: any;
    stockDetailsPayload: any;
    stockDetailsSuccess: boolean
}

const initialState: ProfileState = {
    loading: false,
    error: null,
    searchDataSuccess: false,
    searchDataPayload: null,
    stockDataSuccess: false,
    stockDataPayload: null,
    stockDetailsSuccess: false,
    stockDetailsPayload: null
};


export const searchData = createAsyncThunk(
    "search/searchData",
    async (query: string) => {
        const response = await axios.get(
            `https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=${query}&apikey=V7RG8B2EWK1PKQQE`
        );
        const matches = response.data.bestMatches.map((match: any) => ({
            symbol: match["1. symbol"],
            name: match["2. name"],
        }));
        return matches;
    }
);


export const fetchStockData = createAsyncThunk(
    'search/fetchStockData',
    async ({ symbol, timeframe }: { symbol: string, timeframe: string }) => {
        const response = await axios.get(
            `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=${symbol}&apikey=demo`
        );
        const timeSeries = response.data["Time Series (Daily)"];
        const formattedData = Object.entries(timeSeries).map(([date, values]: [string, any]) => ({
            date,
            close: parseFloat(values["4. close"]),
        }));
        return formattedData;
    }
);

export const stockDetails = createAsyncThunk(
    "search/stockDetails",
    async (symbol: string) => {
        const [quoteResponse, overviewResponse] = await Promise.all([
            axios.get(`https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo`),
            axios.get(`https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo`)
        ]);

        const quoteData = quoteResponse.data;
        const overviewData = overviewResponse.data;

        return {
            price: quoteData['Global Quote']['05. price'],
            marketCap: overviewData['MarketCapitalization'],
            peRatio: overviewData['PERatio'],
            pbRatio: overviewData['PBRatio'],
            psRatio: overviewData['PSRatio'],
            pegRatio: overviewData['PEGRatio'],
            dividendYield: overviewData['DividendYield'],
            revenue: overviewData['RevenueTTM'],
            earnings: overviewData['NetIncomeTTM'],
            grossMargin: overviewData['GrossProfitTTM'] / overviewData['RevenueTTM'],
            operatingMargin: overviewData['OperatingIncomeTTM'] / overviewData['RevenueTTM'],
            profitMargin: overviewData['NetIncomeTTM'] / overviewData['RevenueTTM'],
            debtToEquity: overviewData['DebtToEquity'],
            operatingCashFlow: overviewData['OperatingCashflow'],
            beta: overviewData['Beta'],
            nextEarnings: overviewData['NextEarningsDate'],
            exDividendDate: overviewData['ExDividendDate'],
            nextDividend: overviewData['NextDividend'],
            WeekHigh52: overviewData['52WeekHigh'],
            WeekLow52: overviewData['52WeekLow'],
            Sector: overviewData['Sector'],
            LatestQuarter: overviewData['LatestQuarter'],
        };
    }
);


const searchSlice = createSlice({
    name: 'search',
    initialState,
    reducers: {},

    extraReducers: (builder) => {
        builder
            .addCase(searchData.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(searchData.fulfilled, (state, action) => {
                state.loading = false;
                state.searchDataSuccess = true;
                state.searchDataPayload = action.payload;
            })
            .addCase(searchData.rejected, (state, action) => {
                state.loading = false;
                state.searchDataSuccess = false;
                state.error = action.error.message || 'Search data fetch failed';
            })
            .addCase(fetchStockData.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchStockData.fulfilled, (state, action) => {
                state.loading = false;
                state.stockDataSuccess = true;
                state.stockDataPayload = action.payload;
            })
            .addCase(fetchStockData.rejected, (state, action) => {
                state.loading = false;
                state.stockDataSuccess = false;
                state.error = action.error.message || 'Stock data fetch failed';
            })
            .addCase(stockDetails.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(stockDetails.fulfilled, (state, action) => {
                state.loading = false;
                state.stockDetailsSuccess = true;
                state.stockDetailsPayload = action.payload;

            })
            .addCase(stockDetails.rejected, (state, action) => {
                state.loading = false;
                state.stockDetailsSuccess = false;
                state.error = action.error.message || 'Stock details fetch failed';
            });
    },
});



export default searchSlice.reducer;

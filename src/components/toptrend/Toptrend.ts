import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface ProfileState {
    loading: boolean;
    error: string | null;
    searchDataSuccess: boolean;
    searchDataPayload: any;
}

const initialState: ProfileState = {
    loading: false,
    error: null,
    searchDataSuccess: false,
    searchDataPayload: null,
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


const toptrendSlice = createSlice({
    name: 'toptrend',
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
    },
});

export default toptrendSlice.reducer;

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface ToptrendState {
    loading: boolean;
    error: string | null;
    volatilityPayload: any | null;
    volatilitySuccess: boolean;
}

const initialState: ToptrendState = {
    loading: false,
    error: null,
    volatilityPayload: null,
    volatilitySuccess: false
};

export const volatility = createAsyncThunk(
    "toptrend/volatility",
    async (query: string) => {
        const response = await axios.get(
            `https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=${query}&apikey=V7RG8B2EWK1PKQQE`
        )
        return response;
    }
);


const toptrendSlice = createSlice({
    name: 'toptrend',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(volatility.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(volatility.fulfilled, (state, action) => {
                state.loading = false;
                state.volatilitySuccess = true;
                state.volatilityPayload = action.payload;
            })
            .addCase(volatility.rejected, (state, action) => {
                state.loading = false;
                state.volatilitySuccess = false;
                state.error = action.error.message || 'volatility data fetch failed';
            })
    },
});


export default toptrendSlice.reducer;

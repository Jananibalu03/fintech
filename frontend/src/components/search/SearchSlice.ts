import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { AuthService } from '../../service/authServer';


interface ProfileState {
    loading: boolean;
    error: string | null;
    searchDataSuccess: boolean;
    searchDataPayload: any;
    graphDataPayload: any;
    graphDataSuccess: boolean
}

const initialState: ProfileState = {
    loading: false,
    error: null,
    searchDataSuccess: false,
    searchDataPayload: null,
    graphDataSuccess: false,
    graphDataPayload: null
};


export const searchData = createAsyncThunk(
    'volatility/searchData',
    async (symbol: string, { rejectWithValue }) => {
        try {
            const data = await AuthService.searchData(symbol);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);


export const graphData = createAsyncThunk(
    'volatility/graphData',
    async ({ symbol, range_type }: { symbol: string; range_type: string }, { rejectWithValue }) => {

        try {
            const data = await AuthService.graphData(symbol, range_type);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
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

            .addCase(graphData.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(graphData.fulfilled, (state, action) => {
                state.loading = false;
                state.graphDataSuccess = false;
                state.graphDataPayload = action.payload;
            })

            .addCase(graphData.rejected, (state, action) => {
                state.loading = false;
                state.graphDataSuccess = false;
                state.error = action.error.message || 'Search data fetch failed';
            })
    },
});

export default searchSlice.reducer;

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { AuthService } from '../../service/authServer';

interface ToptrendState {
    filter(arg0: (stock: any) => any): unknown;
    loading: boolean;
    error: string | null;
    fetchVolatilityPayload: any | null;
    fetchVolatilitySuccess: boolean;
    hignin52Success: boolean;
    hignin52Payload: any,
    lowperatioPayload: any,
    lowperatioSuccess: boolean,
    topgainSuccess: boolean,
    topgainPayload: any,
    toplossSuccess: boolean,
    toplossPayload: any,
}

const initialState: ToptrendState = {
    loading: false,
    error: null,
    fetchVolatilityPayload: null,
    fetchVolatilitySuccess: false,
    hignin52Payload: null,
    hignin52Success: false,
    lowperatioSuccess: false,
    lowperatioPayload: null,
    topgainSuccess: false,
    topgainPayload: null,
    toplossPayload: null,
    toplossSuccess: false,

};

export const fetchVolatility = createAsyncThunk(
    'volatility/fetchVolatility',
    async (_, { rejectWithValue }) => {
        try {
            const data = await AuthService.volatility();
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);

export const hignin52 = createAsyncThunk(
    'volatility/hignin52',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.hignin52(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);

export const lowperatio = createAsyncThunk(
    'volatility/lowperatio',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.lowperatio(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);
export const topgain = createAsyncThunk(
    'volatility/topgain',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.topgain(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);
export const toploss = createAsyncThunk(
    'volatility/toploss',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.toploss(page, limit);  
            console.log(data);
                      
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);


const toptrendSlice = createSlice({
    name: 'toptrend',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder

            .addCase(fetchVolatility.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchVolatility.fulfilled, (state, action) => {
                state.loading = false;
                state.fetchVolatilitySuccess = true;
                state.fetchVolatilityPayload = action.payload;
            })
            .addCase(fetchVolatility.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch transaction history';
            })
            .addCase(hignin52.pending, (state) => {
                state.loading = true;
            })
            .addCase(hignin52.fulfilled, (state, action) => {
                state.loading = false;
                state.hignin52Success = true;
                state.hignin52Payload = action.payload;
            })
            .addCase(hignin52.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch 52 Weeks data history';
            })

            .addCase(lowperatio.pending, (state) => {
                state.loading = true;
            })
            .addCase(lowperatio.fulfilled, (state, action) => {
                state.loading = false;
                state.lowperatioSuccess = true;
                state.lowperatioPayload = action.payload;
            })
            .addCase(lowperatio.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

            .addCase(topgain.pending, (state) => {
                state.loading = true;
            })
            .addCase(topgain.fulfilled, (state, action) => {
                state.loading = false;
                state.topgainSuccess = true;
                state.topgainPayload = action.payload;
            })
            .addCase(topgain.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

            .addCase(toploss.pending, (state) => {
                state.loading = true;
            })
            .addCase(toploss.fulfilled, (state, action) => {
                state.loading = false;
                state.toplossSuccess = true;
                state.toplossPayload = action.payload;
            })
            .addCase(toploss.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

    },
});

export default toptrendSlice.reducer;

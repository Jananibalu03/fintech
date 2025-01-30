import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { AuthService } from '../../service/authServer';

interface ToptrendState {
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
    topperformSuccess: boolean,
    topperformPayload: null,
    underfiftydollorSuccess: boolean,
    underfiftydollorPayload: null,
    undertendollarSuccess: boolean,
    undertendollarPayload: null,
    lowbetaSuccess: boolean,
    lowbetaPayload: null,
    highrandrSuccess: boolean,
    highrandrPayload: null,
    debtfreestockPayload: null,
    debtfreestockSuccess: boolean;
    dividendPayload: null,
    dividendSuccess: boolean,
    highdividendPayload: null,
    highdividendSuccess: boolean,
    negativebetaPayload: null,
    negativebetaSuccess: boolean,
    lowin52Payload:null,
    lowin52Success:boolean
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
    topperformSuccess: false,
    topperformPayload: null,
    underfiftydollorSuccess: false,
    underfiftydollorPayload: null,
    undertendollarSuccess: false,
    undertendollarPayload: null,
    lowbetaSuccess: false,
    lowbetaPayload: null,
    highrandrSuccess: false,
    highrandrPayload: null,
    debtfreestockSuccess: false,
    debtfreestockPayload: null,
    dividendPayload: null,
    dividendSuccess: false,
    highdividendPayload: null,
    highdividendSuccess: false,
    negativebetaPayload: null,
    negativebetaSuccess: false,
    lowin52Payload: null,
    lowin52Success: false
};

export const fetchVolatility = createAsyncThunk(
    'volatility/fetchVolatility',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.fetchVolatility(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);


export const hignin52 = createAsyncThunk(
    'volatility/hignin52',
    async ({ Search, page, limit }: { Search:any, page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.hignin52(Search, page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);


export const lowin52 = createAsyncThunk(
    'volatility/lowin52',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.lowin52(page, limit);
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
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);


export const topperform = createAsyncThunk(
    'volatility/topperform',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.topperform(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);


export const underfiftydollor = createAsyncThunk(
    'volatility/underfiftydollor',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.underfiftydollor(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);


export const undertendollar = createAsyncThunk(
    'volatility/undertendollar',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.undertendollar(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);


export const negativebeta = createAsyncThunk(
    'volatility/negativebeta',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.negativebeta(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);

export const lowbeta = createAsyncThunk(
    'volatility/lowbeta',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.lowbeta(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);

export const highriskandreward = createAsyncThunk(
    'volatility/highriskandreward',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.highriskandreward(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);


export const debtfreestocks = createAsyncThunk(
    'volatility/debtfreestocks',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.debtfreestocks(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);

export const dividend = createAsyncThunk(
    'volatility/dividend',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.dividend(page, limit);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);

export const highdividend = createAsyncThunk(
    'volatility/highdividend',
    async ({ page, limit }: { page: number; limit: number }, { rejectWithValue }) => {
        try {
            const data = await AuthService.highdividend(page, limit);
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

            .addCase(lowin52.pending, (state) => {
                state.loading = true;
            })
            .addCase(lowin52.fulfilled, (state, action) => {
                state.loading = false;
                state.lowin52Success = true;
                state.lowin52Payload = action.payload;
            })
            .addCase(lowin52.rejected, (state, action) => {
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

            .addCase(topperform.pending, (state) => {
                state.loading = true;
            })
            .addCase(topperform.fulfilled, (state, action) => {
                state.loading = false;
                state.topperformSuccess = true;
                state.topperformPayload = action.payload;
            })
            .addCase(topperform.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

            .addCase(underfiftydollor.pending, (state) => {
                state.loading = true;
            })
            .addCase(underfiftydollor.fulfilled, (state, action) => {
                state.loading = false;
                state.underfiftydollorSuccess = true;
                state.underfiftydollorPayload = action.payload;
            })
            .addCase(underfiftydollor.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

            .addCase(undertendollar.pending, (state) => {
                state.loading = true;
            })
            .addCase(undertendollar.fulfilled, (state, action) => {
                state.loading = false;
                state.undertendollarSuccess = true;
                state.undertendollarPayload = action.payload;
            })
            .addCase(undertendollar.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

            .addCase(negativebeta.pending, (state) => {
                state.loading = true;
            })
            .addCase(negativebeta.fulfilled, (state, action) => {
                state.loading = false;
                state.negativebetaSuccess = true;
                state.negativebetaPayload = action.payload;
            })
            .addCase(negativebeta.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

            .addCase(lowbeta.pending, (state) => {
                state.loading = true;
            })
            .addCase(lowbeta.fulfilled, (state, action) => {
                state.loading = false;
                state.lowbetaSuccess = true;
                state.lowbetaPayload = action.payload;
            })
            .addCase(lowbeta.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

            .addCase(highriskandreward.pending, (state) => {
                state.loading = true;
            })
            .addCase(highriskandreward.fulfilled, (state, action) => {
                state.loading = false;
                state.highrandrSuccess = true;
                state.highrandrPayload = action.payload;
            })
            .addCase(highriskandreward.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

            .addCase(debtfreestocks.pending, (state) => {
                state.loading = true;
            })
            .addCase(debtfreestocks.fulfilled, (state, action) => {
                state.loading = false;
                state.debtfreestockSuccess = true;
                state.debtfreestockPayload = action.payload;
            })
            .addCase(debtfreestocks.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

            .addCase(dividend.pending, (state) => {
                state.loading = true;
            })
            .addCase(dividend.fulfilled, (state, action) => {
                state.loading = false;
                state.dividendSuccess = true;
                state.dividendPayload = action.payload;
            })
            .addCase(dividend.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })


            .addCase(highdividend.pending, (state) => {
                state.loading = true;
            })
            .addCase(highdividend.fulfilled, (state, action) => {
                state.loading = false;
                state.highdividendSuccess = true;
                state.highdividendPayload = action.payload;
            })
            .addCase(highdividend.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch low pe data history';
            })

    },
});

export default toptrendSlice.reducer;

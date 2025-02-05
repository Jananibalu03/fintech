import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { AuthService } from '../service/authServer';


interface ProfileState {
    loading: boolean;
    error: string | null;
    BotDataSuccess: boolean;
    BotDataPayload: any;
}

const initialState: ProfileState = {
    loading: false,
    error: null,
    BotDataSuccess: false,
    BotDataPayload: null,
};


export const BotData = createAsyncThunk(
    'bot/BotData',
    async (message: any, { rejectWithValue }) => {
        try {
            const data = await AuthService.BotData(message);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data || 'An error occurred');
        }
    }
);




const BotSlice = createSlice({
    name: 'search',
    initialState,
    reducers: {},

    extraReducers: (builder) => {
        builder
            .addCase(BotData.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(BotData.fulfilled, (state, action) => {
                state.loading = false;
                state.BotDataSuccess = true;
                state.BotDataPayload = action.payload;
            })
            .addCase(BotData.rejected, (state, action) => {
                state.loading = false;
                state.BotDataSuccess = false;
                state.error = action.error.message || 'Search data fetch failed';
            })

           
    },
});

export default BotSlice.reducer;


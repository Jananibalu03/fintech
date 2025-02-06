import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { AuthService } from "../service/authServer";
import Cookies from "js-cookie";


interface LoginState {
    loading: boolean;
    error: string | null;
    loginSuccess: boolean;
    loginPayload: any;
    isAuthenticated: boolean;
    registrationPayload: any,
    registrationSuccess: boolean;
    resetpasswordPayload: any;
    resetpasswordSuccess: boolean;
    forgetpasswordPayload:any;
    forgetpasswordSuccess:boolean
}

const initialState: LoginState = {
    loading: false,
    error: null,
    loginSuccess: false,
    loginPayload: null,
    isAuthenticated: !!Cookies.get("access_token"),
    registrationPayload: null,
    registrationSuccess: false,
    resetpasswordSuccess: false,
    resetpasswordPayload: null,
    forgetpasswordSuccess:false,
    forgetpasswordPayload:null
};

export const login = createAsyncThunk(
    "auth/login",
    async (payload: any, { rejectWithValue }) => {
        try {
            const data = await AuthService.login(payload);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.message);
        }
    }
);

export const registration = createAsyncThunk(
    "auth/registration",
    async (payload: any, { rejectWithValue }) => {
        try {
            const data = await AuthService.registration(payload);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.message);
        }
    }
);

export const forgetpassword = createAsyncThunk(
    "auth/forgetpassword",
    async (payload, { rejectWithValue }) => {
        try {
            const data = await AuthService.forgetpassword(payload);
            return data;
        } catch (error:any) {
            return rejectWithValue(error.message);
        }
    }
);

export const resetpassword = createAsyncThunk(
    "auth/resetpassword",
    async (payload: { token: string; password: string; confirm_password: string }, { rejectWithValue }) => {
        try {
            const data = await AuthService.resetpassword(payload);
            return data;
        } catch (error: any) {
            return rejectWithValue(error.message);
        }
    }
);


const loginSlice = createSlice({
    name: "login",
    initialState,
    reducers: {
        logout: (state) => {
            AuthService.logout();
            state.isAuthenticated = false;
            state.loginSuccess = false;
            state.loginPayload = null;
        },
    },

    extraReducers: (builder) => {
        builder
            .addCase(login.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(login.fulfilled, (state, action) => {
                state.loading = false;
                state.loginSuccess = true;
                state.loginPayload = action.payload;
                state.isAuthenticated = true;
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                state.loginSuccess = false;
                state.error = action.payload as string;
            })

            .addCase(registration.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(registration.fulfilled, (state, action) => {
                state.loading = false;
                state.registrationSuccess = true;
                state.registrationPayload = action.payload;
            })
            .addCase(registration.rejected, (state, action) => {
                state.loading = false;
                state.registrationSuccess = false;
                state.error = action.payload as string;
            })

            .addCase(forgetpassword.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(forgetpassword.fulfilled, (state, action) => {
                state.loading = false;
                state.forgetpasswordSuccess = true;
                state.forgetpasswordPayload = action.payload;
            })
            .addCase(forgetpassword.rejected, (state, action) => {
                state.loading = false;
                state.forgetpasswordSuccess = false;
                state.error = action.payload as string;
            })

            .addCase(resetpassword.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(resetpassword.fulfilled, (state, action) => {
                state.loading = false;
                state.resetpasswordSuccess = true;
                state.resetpasswordPayload = action.payload;
            })
            .addCase(resetpassword.rejected, (state, action) => {
                state.loading = false;
                state.resetpasswordSuccess = false;
                state.error = action.payload as string;
            });
    },
});

export const { logout } = loginSlice.actions;
export default loginSlice.reducer;

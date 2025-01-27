import { configureStore } from '@reduxjs/toolkit';
import searchReducer from "../components/search/SearchSlice";
import toptrendReducer from '../components/toptrend/Toptrend';


const store = configureStore({
    reducer: {
        search: searchReducer,
        TopTrend: toptrendReducer
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;

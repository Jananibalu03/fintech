import axios from 'axios';
import { BASE_URL } from '../config/config';
import Cookies from "js-cookie";
import { baseApi } from "../../interceptor";

export const AuthService = {

    login: async (payload: any) => {
        try {
            const response = await baseApi.post("authapi/login", payload);
            if (response.data?.access_token) {
                Cookies.set("access_token", response.data.access_token, { expires: 7 });
            }
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || "An error occurred while logging in");
        }
    },
    logout: () => {
        Cookies.remove("access_token");
    },

    registration: async (payload: any) => {
        try {
            const response = await axios.post(`${BASE_URL}authapi/register`, payload);
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    forgetpassword: async (payload: any) => {
        try {
            const response = await axios.post(`${BASE_URL}authapi/forgotpassword`, payload);
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while sending the request');
        }
    },

    resetpassword: async (payload: { token: string; password: string; confirm_password: string }) => {
        try {
            const response = await axios.post(
                `${BASE_URL}authapi/resetpassword?token=${payload.token}`, 
                {
                    password: payload.password,
                    confirm_password: payload.confirm_password  
                },
                {
                    headers: { "Content-Type": "application/json" }
                }
            );
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while resetting the password');
        }
    },

    fetchVolatility: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/volatility`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    hignin52: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/52weekshigh`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    lowin52: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/52weekslow`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    lowperatio: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/lowperatio`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    topgain: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/todaytopgain`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    toploss: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/todaytoploss`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    topperform: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/topperformance`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    underfiftydollor: async (Seach: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/abovetendoller`, {
                params: { Seach, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    undertendollar: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/undertendollar`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    negativebeta: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/negativebeta`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    lowbeta: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/lowbeta`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    highriskandreward: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/highriskandreward`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    debtfreestocks: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/debtfreestocks`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    dividend: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/dividend`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    highdividend: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/highdividendyield`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    searchData: async (symbol: string) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/Search`, {
                params: { symbol },
            });
            return response.data;
        } catch (error: any) {
            console.error('Error fetching search data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    graphData: async (symbol: string, range_type: any) => {
        try {
            const response = await axios.get(`${BASE_URL}api/stock/graph`, {
                params: { symbol, range_type },
            });
            return response.data;
        } catch (error: any) {
            console.error('Error fetching search data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    BotData: async (message: string) => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/botapi/chatbot", {
                message,
            });
            return response.data;
        } catch (error: any) {
            console.error("Error fetching bot response:", error);
            throw new Error(error.response?.data?.message || "An error occurred while fetching the data");
        }
    }
};

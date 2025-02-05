import axios from 'axios';
import { BASE_URL } from '../config/config';

export const AuthService = {

    fetchVolatility: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}volatility`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    hignin52: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}52weekshigh`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    lowin52: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}52weekslow`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    lowperatio: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}lowperatio`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    topgain: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}todaytopgain`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    toploss: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}todaytoploss`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    topperform: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}topperformance`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    underfiftydollor: async (Seach: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}abovetendoller`, {
                params: { Seach, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    undertendollar: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}undertendollar`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    negativebeta: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}negativebeta`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    lowbeta: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}lowbeta`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    highriskandreward: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}highriskandreward`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    debtfreestocks: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}debtfreestocks`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    dividend: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}dividend`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    highdividend: async (Search: any, page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}highdividendyield`, {
                params: { Search, page, limit },
            });
            return response.data;
        } catch (error: any) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    searchData: async (symbol: string) => {
        try {
            const response = await axios.get(`${BASE_URL}Search`, {
                params: { symbol }, // This will correctly append ?symbol=ibm
            });
            return response.data;
        } catch (error: any) {
            console.error('Error fetching search data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    graphData: async (symbol: string, range_type: any) => {
        try {
            const response = await axios.get(`${BASE_URL}graph`, {
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

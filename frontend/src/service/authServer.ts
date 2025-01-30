import axios from 'axios';
import { BASE_URL } from '../config/config';

export const AuthService = {

    fetchVolatility: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}volatility`, {
                params: { page, limit },
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

    lowperatio: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}lowperatio`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    topgain: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}todaytopgain`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    toploss: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}todaytoploss`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    topperform: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}todaytoploss`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },


    underfiftydollor: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}abovetendoller`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    undertendollar: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}undertendollar`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    negativebeta: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}negativebeta`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    lowbeta: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}lowbeta`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    highriskandreward: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}highriskandreward`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    debtfreestocks: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}debtfreestocks`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    dividend: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}dividend`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

    highdividend: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}highdividendyield`, {
                params: { page, limit },
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching 52-week high data:', error);
            throw new Error(error.response?.data?.message || 'An error occurred while fetching the data');
        }
    },

};

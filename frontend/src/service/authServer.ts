import axios from 'axios';
import { BASE_URL } from '../config/config';

export const AuthService = {

    volatility: async () => {
        const response = await axios.get(`${BASE_URL}volatility?page=${1}&limit=${10}`);
        return response.data;
    },

    hignin52: async (page: number, limit: number) => {
        try {
            const response = await axios.get(`${BASE_URL}52weekshigh`, {
                params: { page, limit },
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
};

import axios, { InternalAxiosRequestConfig } from "axios";
import { toast } from "react-toastify";
import Cookies from "js-cookie";


export const BASE_URL = import.meta.env.VITE_BASE_URL;

const baseApi = axios.create({
    baseURL: BASE_URL,
});

baseApi.interceptors.request.use(
    function (config: InternalAxiosRequestConfig) {
        const access_token = Cookies.get('access_token');

        if (config.headers) {

            if (access_token) {
                config.headers['Authorization'] = `Bearer ${access_token}`;
            }
        }

        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);

baseApi.interceptors.response.use(

    (response) => response,
    (error) => {
        console.error("Error details:", error);

        if (error.response) {
            const { status, data, headers } = error.response;
            console.error("Response error details:", {
                status,
                data,
                headers
            });

            switch (status) {
                case 400:
                    handleBadRequest(data);
                    break;
                case 401:
                    handleUnauthorized(data);
                    break;
                case 404:
                    handleNotFound(data.detail || data);
                    break;
                case 500:
                    handleServerError(data.validationMessage || data);
                    break;
                default:
                    console.error("Unhandled status code:", status);
                    break;
            }
        } else if (error.request) {
            toast.error("No response received from server. Please try again.");
        } else {
            toast.error("An unexpected error occurred.");
        }

        return Promise.reject(error);
    }
);


function handleBadRequest(error: any) {
    toast.error(error.message || "Bad request.");
}

function handleUnauthorized(error: any) {
    toast.error(error.message || "Unauthorized access.");
}

function handleNotFound(error: any) {
    toast.error(error || "Resource not found.");
}

function handleServerError(error: any) {
    toast.error(error || "Internal server error.");
}

export { baseApi };

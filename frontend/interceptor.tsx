import axios from "axios";
import { toast } from "react-toastify";

export const BASE_URL = import.meta.env.VITE_BASE_URL;

const baseApi = axios.create({
    baseURL: BASE_URL,
});

baseApi.interceptors.request.use(
    function (config) {
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);

baseApi.interceptors.response.use(
    (response) => response,
    (error) => {
        console.log(error);
        switch (error.response.status) {
            case 400:
                handleBadRequest(error.response.data);
                break;
            case 401:
                handleUnauthorizaton(error.response.data);
                break;
            case 404:
                handleNotFound(error.response.data.detail);
                break;
            case 500:
                handleServerError(error.response.data.validationMessage);
                break;
            default:
                break;
        }
        return error.response;
    }
);

function handleBadRequest(error: any) {
    toast.error(error.message);
}

function handleUnauthorizaton(error: any) {
    toast.error(error.message);
}

function handleNotFound(error: any) {
    toast.error(error);
}

function handleServerError(error: any) {
    toast.error(error);
}

export { baseApi };


import api from "./api"

export const getCompanies = async(startIdx) => {

    try{
        const response = await api.get(`/companies?startIdx=${startIdx}`)
        return response
    } catch(e) {
        throw new Error("Error occured while fetching companies: ", e)
    }
}

export const getStock = async(name) => {

    try{
        const response = await api.get(`search/${name}`)
        return response
    } catch(e) {
        throw new Error("Error occured while fetching Stock: ", e)
    }
}

export const getStockData = async(symbol) => {

    try{
        const response = await api.get(`/data/${symbol}`)

        return response
    } catch(e) {
        throw new Error("Error occured while fetching Stock data: ", e)
    }
}

export const getStockSummary = async(symbol) => {

    try{
        const response = await api.get(`/summary/${symbol}`)

        return response
    } catch(e) {
        throw new Error("Error occured while fetching Stock Summary: ", e)
    }
}

export const getComparision = async(s1, s2) => {

    try{
        const response = await api.get(`/compare?symbol1=${s1}&symbol2=${s2}`)

        return response
    } catch(e) {
        throw new Error("Error occured while fetching comparision data: ", e)
    }
}
import {api} from "./conifgs/axiosConfig";


export const AuthorizationApi = {
  signin: async (username, password) => {
    return await api.request({
      url: `/auth/signin/`,
      method: "POST",
      data: {username: username, password: password},
    });
  },

  signup: async (username, password) => {
    return await api.request({
      url: `/auth/signup/`,
      method: "POST",
      data: {"username": username, "password": password},
    })
  }
}
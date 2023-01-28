import {api} from "./conifgs/axiosConfig";


export const TodoistApi = {
  getAllProjects: async (token) => {
    return await api.request({
      url: `/projects/`,
      method: "GET",
      headers: {"Authorization": `Token ${token}`},
    })
  },

  removeProject: async (id, token) => {
    return await api.request({
      url: `/projects/${id}`,
      method: "DELETE",
      headers: {"Authorization": `Token ${token}`},
    })
  },

  createProject: async (data, token) => {
    return await api.request({
      url: `/projects/`,
      method: "POST",
      data: data,
      headers: {"Authorization": `Token ${token}`},
    })
  },

  getCollatedTasks: async (key, token) => {
    return await api.request({
      url: `/collated/${key}`,
      method: "GET",
      headers: {"Authorization": `Token ${token}`},
    })
  },

  getProjectTasks:  async (id, token) => {
    return await api.request({
      url: `/projects/${id}/tasks`,
      method: "GET",
      headers: {"Authorization": `Token ${token}`},
    })
  },

  createTask: async (project_id, data, token) => {
    return await api.request({
      url: `/projects/${project_id}/tasks`,
      method: "POST",
      data: data,
      headers: {"Authorization": `Token ${token}`},
    })
  },

  removeTask: async (project_id, id, token) => {
    return await api.request({
      url: `/projects/${project_id}/tasks/${id}`,
      method: "DELETE",
      headers: {"Authorization": `Token ${token}`},
    })
  },
}
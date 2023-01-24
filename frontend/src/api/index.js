import axios from "axios"


const API_URL = 'http://localhost:8000/api'


const todoistAPI = {
    getProjectTasks: async (task_key) => {
        return await axios({
            method: 'GET',
            url: `${API_URL}/projects/${task_key}/tasks`,
            headers: { 'Authorization': 'Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NzQ5Nzc2NTEsInN1YiI6ImFjY2VzcyJ9.UN625pGDHKgiKQIsPpnpPw67-S5h3skI9BFVi1ncljg' }
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    getUserProjects: async () => {
        return await axios({
            method: 'GET',
            url: `${API_URL}/projects`,
            headers: { 'Authorization': 'Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NzQ5Nzc2NTEsInN1YiI6ImFjY2VzcyJ9.UN625pGDHKgiKQIsPpnpPw67-S5h3skI9BFVi1ncljg' }
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    getCollatedTasks: async (collated_key) => {
        return await axios({            method: 'GET',
            url: `${API_URL}/collated/${collated_key.toLowerCase()}`,
            headers: { 'Authorization': 'Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NzQ5Nzc2NTEsInN1YiI6ImFjY2VzcyJ9.UN625pGDHKgiKQIsPpnpPw67-S5h3skI9BFVi1ncljg' }
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    addNewProject: async (new_project_data) => {
        return await axios({
            method: 'POST',
            url: `${API_URL}/projects`,
            headers: { 'Authorization': 'Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NzQ5Nzc2NTEsInN1YiI6ImFjY2VzcyJ9.UN625pGDHKgiKQIsPpnpPw67-S5h3skI9BFVi1ncljg' },
            data: new_project_data
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    deleteProject: async (project_id) => {
        return await axios({
            method: 'DELETE',
            url: `${API_URL}/projects`,
            headers: { 'Authorization': 'Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NzQ5Nzc2NTEsInN1YiI6ImFjY2VzcyJ9.UN625pGDHKgiKQIsPpnpPw67-S5h3skI9BFVi1ncljg' }
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    addNewTask: async (project_id, new_task_data) => {
        return await axios({
            method: 'POST',
            url: `${API_URL}/projects/${project_id}/tasks/`,
            headers: { 'Authorization': 'Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NzQ5Nzc2NTEsInN1YiI6ImFjY2VzcyJ9.UN625pGDHKgiKQIsPpnpPw67-S5h3skI9BFVi1ncljg' },
            data: new_task_data
        }).catch(error => {
            if (error.responpse) {
                return error.response.data
            }
        })
    },

    addNewProjsdadaect: async (collated_key) => {
        return await axios({
            method: 'GET',
            url: `${API_URL}/collated/${collated_key.toLowerCase()}`,
            headers: { 'Authorization': 'Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NzQ5Nzc2NTEsInN1YiI6ImFjY2VzcyJ9.UN625pGDHKgiKQIsPpnpPw67-S5h3skI9BFVi1ncljg' }
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    agetProjectTasasdadasdks: async (project) => {
        return await axios({
            method: 'GET',
            url: `${API_URL}/projects/${project}`,
            headers: { 'Authorization': 'Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NzQ5Nzc2NTEsInN1YiI6ImFjY2VzcyJ9.UN625pGDHKgiKQIsPpnpPw67-S5h3skI9BFVi1ncljg' }
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    }
}

export { todoistAPI };
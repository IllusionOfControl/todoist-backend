import axios from "axios"


const API_URL = 'http://192.168.24.64:8000'


const todoistAPI = {

    getProjectTasks: async (task_key) => {
        return await axios({
            method: 'GET',
            url: `${API_URL}/projects/${task_key}/tasks`,
            headers: { 'Authorization': 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NjA3NTY1ODgsInN1YiI6ImFjY2VzcyJ9._EfD0m_peFl0dRupDKLx1W8NPwJAu3MX-y3YB8ku9gs' }
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
            headers: { 'Authorization': 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NjA3NTY1ODgsInN1YiI6ImFjY2VzcyJ9._EfD0m_peFl0dRupDKLx1W8NPwJAu3MX-y3YB8ku9gs' }
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    getCollatedTasks: async (collated_key) => {
        return await axios({
            method: 'GET',
            url: `${API_URL}/collated/${collated_key.toLowerCase()}`,
            headers: { 'Authorization': 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NjA3NTY1ODgsInN1YiI6ImFjY2VzcyJ9._EfD0m_peFl0dRupDKLx1W8NPwJAu3MX-y3YB8ku9gs' }
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
            headers: { 'Authorization': 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NjA3NTY1ODgsInN1YiI6ImFjY2VzcyJ9._EfD0m_peFl0dRupDKLx1W8NPwJAu3MX-y3YB8ku9gs' },
            data: new_project_data
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    deleteProject: async (project_id) => {
        return await axios({
            method: 'GET',
            url: `${API_URL}/projects`,
            headers: { 'Authorization': 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NjA3NTY1ODgsInN1YiI6ImFjY2VzcyJ9._EfD0m_peFl0dRupDKLx1W8NPwJAu3MX-y3YB8ku9gs' }
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    addNewTask: async (project_id, new_task_data) => {
        return await axios({
            method: 'GET',
            url: `${API_URL}/projects/${project_id}/tasks/`,
            headers: { 'Authorization': 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NjA3NTY1ODgsInN1YiI6ImFjY2VzcyJ9._EfD0m_peFl0dRupDKLx1W8NPwJAu3MX-y3YB8ku9gs' },
            data: new_task_data
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    },

    addNewProjsdadaect: async (collated_key) => {
        return await axios({
            method: 'GET',
            url: `${API_URL}/collated/${collated_key.toLowerCase()}`,
            headers: { 'Authorization': 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NjA3NTY1ODgsInN1YiI6ImFjY2VzcyJ9._EfD0m_peFl0dRupDKLx1W8NPwJAu3MX-y3YB8ku9gs' }
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
            headers: { 'Authorization': 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NjA3NTY1ODgsInN1YiI6ImFjY2VzcyJ9._EfD0m_peFl0dRupDKLx1W8NPwJAu3MX-y3YB8ku9gs' }
        }).catch(error => {
            if (error.response) {
                return error.response.data
            }
        })
    }
}

export { todoistAPI };
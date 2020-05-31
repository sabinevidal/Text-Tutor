import axios  from 'axios';

export function availableClasses() {
    return axios.get('/api/subjects').then(function (response) {
       return response.data;
    })
 }
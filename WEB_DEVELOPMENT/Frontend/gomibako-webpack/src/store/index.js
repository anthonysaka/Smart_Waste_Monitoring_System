import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

const API_URL = process.env.API_URL

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user : localStorage.getItem('userdata') || {'default':'default'}
  },
  mutations: {
    auth_request(state){
        state.status = 'loading'
      },
    auth_success(state, token, user){
      state.status = 'success'
      state.token = token
      state.user = user
    },
    auth_error(state){
      state.status = 'error'
    },
    logout(state){
      state.status = ''
      state.token = ''
      state.user = ''
    },

  },
  actions: {
    login({commit}, user){
        return new Promise(async(resolve, reject) => {
          commit('auth_request'),
          await axios({url: `${API_URL}/login`, data: user, method: 'POST' })
          .then(resp => {
            const token = resp.data.token
            const userr = resp.data.user[0]
            localStorage.setItem('userdata', JSON.stringify(userr))
            localStorage.setItem('token', token)
            axios.defaults.headers.common['Authorization'] = token
            commit('auth_success', token, userr)
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error')
            localStorage.removeItem('userdata')
            localStorage.removeItem('token')
            reject(err)
          })
        })
    },
    logout({commit}){
        return new Promise((resolve, reject) => {
          commit('logout')
          localStorage.removeItem('token')
          localStorage.removeItem('userdata')
          console.log("BORRe")
          delete axios.defaults.headers.common['Authorization']
          resolve()
        })
    }
  },
  getters : {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    userLogged: state => state.user,

  }
})
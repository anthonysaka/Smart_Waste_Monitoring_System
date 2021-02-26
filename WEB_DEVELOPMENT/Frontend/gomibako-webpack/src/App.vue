<template>
  <div id="app">

    <div class="wrapper">
      <!-- Sidebar  -->
      <nav id="sidebar" class="active" v-if="isLoggedIn">
        <div class="sidebar-header">
          <h3>Gomibako System</h3>
          <strong>GS</strong>
        </div>

        <ul class="list-unstyled components">

          <li>
            <router-link to="/home">
              <i class="fas fa-tachometer-alt"></i>
              Home
            </router-link>
          </li>
          <li>
            <router-link to="/detailbins">
              <i class="fas fa-dumpster"></i>
              Bins
            </router-link>
          </li>
          <li>
            <router-link to="/trucks">
              <i class="fas fa-truck"></i>
              Trucks
            </router-link>
          </li>
          <li>
            <router-link to="/routing">
              <i class="fas fa-route"></i>
              Routes
            </router-link>
          </li>
          <li>
            <router-link to="/globaladmin" v-if="userlogged.type == 'Admin'">
              <i class="fas fa-users-cog"></i>
              ADMIN
            </router-link>
          </li>
           <li class="mt-4">
              <a v-on:click="logout" class="fas fa-sign-out-alt "></a>
              Logout
          </li>

        </ul>
      </nav>

      <!-- Content Wrapper -->
      <div id="content-wrapper" class="container-fluid">
        <!-- Top NavBar-->
        <nav class="navbar sticky-top navbar-expand-lg shadow" v-if="isLoggedIn">
          
         <!--  <a class="navbar-brand clearfix mb-2 ml-auto" href="/"><img src="@/assets/img/gomibako_logo_text.png"
              alt="Logo" title="Logo" /></a> -->
          <ul class="navbar-nav ml-auto">
            <button class=" navbar-toggler btn btn-dark d-inline-block d-lg-none ml-auto" type="button"
              data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
              aria-expanded="false" aria-label="Toggle navigation">
              <i class="fas fa-align-justify"></i>
            </button>
            <div class="collapse navbar-collapse flex-grow-0" id="navbarSupportedContent">
              <ul class="nav navbar-nav ml-auto">
                <li class="nav-item">
                  <a class="nav-link" href="#">Usuario logueado:  <b-badge variant="primary" v-if="isLoggedIn">{{userlogged.username}}</b-badge></a>
                </li>
              </ul>
            </div>
          </ul>
        </nav>

        <!-- Main Content  -->
        <div id="content">
          <!-- Begin Page Content -->
          <div class="container-fluid">
            <router-view v-on:childToParent="onChildClick"/>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';
var socket = io.connect("http://localhost:5000")
import Swal from 'sweetalert2';

export default {
  data(){
    return{
      userlogged: '',
      count: 0,
    }
  },
  computed : {
      isLoggedIn : function(){ return this.$store.getters.isLoggedIn},
    },
    methods: {
      logout: function () {
        this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/login')
        })
      },
      onChildClick (value) {
        console.log(value)
        this.userlogged = value
      },
      showToast(data) {
    
        if (data.code == '1'){
          Swal.fire({
            position: 'top-end',
            icon: 'warning',
            title: 'FULL',
            text: data.devName,
            showConfirmButton: false,
            toast: true,
            timer: 5000
          })
          
        } else {
          Swal.fire({
            position: 'top-end',
            icon: 'error',
            title: 'OVERLOAD',
            text: data.devName,
            showConfirmButton: false,
            toast: true,
            timer: 5000
          })
          
        }
        
      }

    },
    created: function () {
    this.$http.interceptors.response.use(undefined, function (err) {
      return new Promise(function (resolve, reject) {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch(logout)
        }
        throw err;
      });
    });

    socket.on("mqtt_message", fetchedData => {
                    var data = JSON.parse(fetchedData)
                    this.showToast(data)
                })
    
  },

  
}
</script>

<style>
  @import './assets/styles/main.css';
</style>
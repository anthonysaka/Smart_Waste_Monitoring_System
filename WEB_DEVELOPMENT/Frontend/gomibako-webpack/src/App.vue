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
              <i class="fas fa-home"></i>
              Home
            </router-link>
          </li>
          <li>
            <router-link to="/dashboard">
              <i class="fas fa-tachometer-alt"></i>
              Dashboard
            </router-link>
          </li>
          <li>
            <router-link to="/detailbins">
              <i class="fas fa-dumpster"></i>
              Bins
            </router-link>
          </li>
          <li>
            <router-link to="/">
              <i class="fas fa-dumpster"></i>
              Routing
            </router-link>
          </li>
          <li>
            <router-link to="/globaladmin" v-if="userlogged.type == 'Admin'">
              <i class="fas fa-users-cog"></i>
              ADMIN
            </router-link>
          </li>
           <li>
            <router-link to="" >
              <i v-on:click="logout" class="fas fa-sign-out-alt"></i>
              Logout
            </router-link>
          </li>

        </ul>
      </nav>

      <!-- Content Wrapper -->
      <div id="content-wrapper" class="container-fluid">
        <!-- Top NavBar-->
        <nav class="navbar sticky-top navbar-expand-lg shadow" v-if="isLoggedIn">
          <!--           <button type="button" id="sidebarToggleTop" class="btn btn-info">
            <i class="fas fa-align-justify"></i>
          </button> -->
          <!-- Topbar Search -->
         <!--  <form class="d-none d-sm-inline-block form-inline  ml-md-3 my-2 my-md-0 mw-100 navbar-search">
            <div class="input-group">
              <input type="text" class="form-control bg-light" placeholder="Search for..." aria-label="Search">
              <div class="input-group-append">
                <button class="btn btn-primary"  type="button">
                  <i class="fas fa-search fa-sm"></i>
                </button>
              </div>
            </div>
          </form> -->
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

export default {
  data(){
    return{
      userlogged: ''
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
    
  },

  
}
</script>

<style>
  @import './assets/styles/main.css';
</style>
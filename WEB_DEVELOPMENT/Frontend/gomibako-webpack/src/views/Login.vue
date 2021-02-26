<template>
  <div class="login">

    <div class="limiter">
      <div class="container-login100">
        <div class="wrap-login100">
          <div class="login100-pic js-tilt" data-tilt>
            <img src="../assets/img/Logo_Gomibako_Blue.png" alt="IMG">
          </div>


          <b-form @submit.prevent="login" class="login100-form validate-form">
           
            <div class="card-body mb-4" style="display: flex;justify-content: center;">
              <h5 class="h5 text-gray-800 my-0"><strong> SISTEMA GOMIBAKO </strong></h5>
            </div>
         

            
              <b-form-group class="wrap-input100 validate-input" label="USUARIO:" label-for="inputUserName">
                <b-form-input class="input100" id="inputUserName" v-model="username" required placeholder="usuario">
                </b-form-input>
              </b-form-group>
            

    
              <b-form-group label="CONTRASENA:" label-for="inputUserPassword">
                <b-form-input class="input100" id="inputUserPassword" type="password" v-model="password" required
                  placeholder="contrasena">
                </b-form-input>
              </b-form-group>
  

            <div class="container-login100-form-btn">
              <b-button class="login100-form-btn" type="submit" variant="primary">ENTRAR</b-button>
            </div>
          </b-form>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
export default {
  data(){
    return{
      username:"",
      password:"",
    
    }
  },
  methods: {
    login: function () {
        let username = this.username
        let password = this.password
        this.$store.dispatch('login', { username, password })
       .then(() => {
        this.$router.push('/home')   
       } 
       )
       .catch(err => console.log(err))
      }
  },
  mounted(){
    console.log(process.env.API_URL)
  }

}
</script>

<style >
 

</style>
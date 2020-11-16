<template>
  <div class="login">
    <b-container class="w-50">
      <div class="card px-5 py-5">

        <h4 class="mt-4"> LOGIN </h4>
        <hr class="line">

        <b-form @submit.prevent="login">
        <b-form-group label="Username:" label-for="inputUserName">
          <b-form-input class="w-50" id="inputUserName" v-model="username"  required placeholder="Ej.: Juan">
          </b-form-input>
        </b-form-group>

        <b-form-group label="Password:" label-for="inputUserPassword">
          <b-form-input class="w-50" id="inputUserPassword" type="password" v-model="password" required placeholder="Ej.: Juan">
          </b-form-input>
        </b-form-group>

         <b-button class="mr-2" type="submit" variant="primary">Aplicar</b-button>

      
      </b-form>

      </div>
      
      
    </b-container>



      
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

<style>

</style>
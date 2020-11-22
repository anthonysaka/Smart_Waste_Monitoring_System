<template>
  <div class="truck">
      <b-container fluid>
          <b-tabs content-class="mt-3" justified>

            <b-tab title="[+] Camiones">
                <b-container @submit="addTruck">
                    <b-form>
                        <h4 class="mt-4"> INFORMACION GENERAL</h4>
                        <hr class="line">
                        <b-row>
                            <b-col cols="6">
                                <b-form-group label="No. de placa:" label-for="inputPlaca">
                                    <b-input id="inputPlaca" v-model="placa" required placeholder="Ej.:A543215"></b-input>
                                </b-form-group>
                            </b-col>
                            <b-col cols="6">
                                <b-form-group label="Ano:" label-for="inputAno">
                                    <b-input id="inputAno" v-model="ano" placeholder="Ej.:2016"></b-input>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col cols="6">
                                <b-form-group label="Marca:" label-for="inputMarca">
                                    <b-input id="inputMarca" v-model="marca" placeholder="Ej.:Isuzu"></b-input>
                                </b-form-group>
                            </b-col>
                            <b-col cols="6">
                                <b-form-group label="Modelo:" label-for="inputModelo">
                                    <b-input id="inputModelo" v-model="modelo" placeholder="Ej.:GA-Series"></b-input>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <h4 class="mt-4"> PARAMETROS DEL CAMION</h4>
                        <hr class="line">
                        <b-row class="mb-4">
                            <b-col cols="6">
                                <b-form-group label="Capacidad de carga(Kg):" label-for="inputPlaca">
                                    <b-input id="inputPlaca" v-model="cap_kg" required placeholder="Ej.:A543215"></b-input>
                                </b-form-group>
                            </b-col>
                            <b-col cols="6">
                                <b-form-group label="Capacidad de volumen (m^3):" label-for="inputPlaca">
                                    <b-input id="inputPlaca" v-model="cap_vol" required placeholder="Ej.:A543215"></b-input>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        
                    <b-button class="mr-2" type="submit" variant="primary">Registrar</b-button>
                    <b-button variant="danger">Cancelar</b-button>
                    
                    </b-form>
                </b-container>
            </b-tab>

            <b-tab title="Camiones">
            </b-tab>
          </b-tabs>

      </b-container>
  </div>
</template>

<script>
import axios from 'axios';
const API_URL = process.env.API_URL;
export default {
    data(){
        return{
            userlogged: JSON.parse(localStorage.getItem('userdata')),
            placa:null,
            ano:null,
            marca:null,
            modelo:null,
            cap_kg:null,
            cap_vol:null,

        }
    },
    methods:{
        async addTruck() {
            try {
                var res = await axios.post(`${API_URL}/truck`,
                                            {
                                                "placa":this.placa,
                                                "ano":this.ano,
                                                "marca": this.marca,
                                                "modelo": this.modelo,
                                                "cap_kg":this.cap_kg,
                                                "cap_vol":this.cap_vol,
                                                "rncCompa":this.userlogged.rnc_compa
                                            });

                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
            
        },
    },

}
</script>

<style>

</style>
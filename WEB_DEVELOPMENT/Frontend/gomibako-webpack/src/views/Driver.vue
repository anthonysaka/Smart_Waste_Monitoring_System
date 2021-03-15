<template>
  <div class="driver">
      <b-container fluid>
          <b-tabs content-class="mt-3" justified>
            <b-tab title="Choferes" active>
                <b-jumbotron class="jumbotron">
                    <div class="card mb-4">
                        <div class="card-body">
                        <h5 class="h5 text-gray-800 my-0"><strong> LISTADO DE CHOFERES</strong></h5>
                        </div>
                    </div>


                    <b-container style="display: flex;justify-content: center;">
                        <b-input-group size="md" class="mb-4 w-50">
                        <b-form-input v-model="filter" type="search" id="filterInput" placeholder="Escribe para buscar"></b-form-input>
                        </b-input-group>

                    </b-container>
                    

                    <b-col cols="12">
                    <div class="card">
                        <div class="card-body">
                            <b-table responsive="sm" borderless hover :items="itemsDriver" :fields="fieldsDriver" head-variant="light" selectable
                                select-mode="single" @row-selected="onRowSelected" :filter="filter"
                                :filter-included-fields="filterOn">

                                <!-- Example scoped slot for select state illustrative purposes -->
                                <template #cell(selected)="{ rowSelected }">
                                <template v-if="rowSelected">
                                    <span aria-hidden="true">&check;</span>
                                    <span class="sr-only">Selected</span>
                                </template>
                                <template v-else>
                                    <span aria-hidden="true">&nbsp;</span>
                                    <span class="sr-only">Not selected</span>
                                </template>
                                </template>

                            </b-table>
                        </div>
                    </div>
                    </b-col>
                </b-jumbotron>
            </b-tab>

             <b-tab title="[+] Chofer">
                 <b-container>
                    <h4 class="mt-4"> INFORMACION REQUERIDA </h4>
                    <hr class="line">

                    <b-form @submit.prevent="addDriver">
                        <b-form-group label="Primer nombre:" label-for="inputDriverName">
                            <b-form-input id="inputDriverName" v-model="formDriver.firstname" required placeholder="Ej.: Juan">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group label="Primer apellido:" label-for="inputDriverLastname">
                            <b-form-input id="inputDriverLastname" v-model="formDriver.lastname" required placeholder="Ej.: Almonte">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group label="E-mail:" label-for="inputDriverEmail">
                            <b-form-input id="inputDriverEmail" v-model="formDriver.email" type="email" required placeholder="Ej.: username@dominio.com">
                            </b-form-input>
                        </b-form-group>

                        <b-button class="mr-2" type="submit" variant="primary">Aplicar</b-button>
                        <b-button @click="onResetDriver" variant="danger">Cancelar</b-button>
                    </b-form>
                 </b-container>
                </b-tab>

            
          </b-tabs>

      </b-container>
  </div>
</template>

<script>
import axios from 'axios';
const API_URL = process.env.API_URL;
import Swal from 'sweetalert2';

export default {
    data(){
        return {
            userlogged: JSON.parse(localStorage.getItem('userdata')),
            formDriver: {
                firstname: '',
                lastname:'',
                email:'',
            },
            fieldsDriver: [
                {
                    key: 'selected',
                    label: '[*]',
                    sortable: true
                }, 
                {
                    key: 'username',
                    label: 'USUARIO',
                    sortable: true
                },
                {
                    key: 'email',
                    label: 'EMAIL',
                    sortable: true,
                },
                {
                    key: 'firstname',
                    label: 'NOMBRE',
                    sortable: true,
                },
                {
                    key: 'lastname',
                    label: 'APELLIDO',
                    sortable: true,
                },
                {
                    key: 'date',
                    label: 'FECHA REGISTRO',
                    sortable: true,
                },
            ],
            itemsDriver:[],
            selectedTable: null,

            filter: null,
            filterOn:[],

        }
    },
    methods:{
        async addDriver(evt) {
            try {
                evt.preventDefault()
                 var res = await axios.post(`${API_URL}/driver`,
                                            {
                                                "firstname":this.formDriver.firstname,
                                                "lastname":this.formDriver.lastname,
                                                "email": this.formDriver.email,
                                                "rncCompa": this.userlogged.rnc_compa,
                                            });

                console.log(res.status)
               
                Swal.fire(
                    'Registrado con exito!',
                    '',
                    'success'
                )
                 this.onResetDriver();
                
            } catch (error) {
                Swal.fire(
                    'Uups, ha ocurrido un error!',
                    '',
                    'error'
                )
                console.log(error)
            }
            
        },
        async loadDriver(){
            try {
                var res = await axios.get(`${API_URL}/driver`,{ params: {rncComp: this.userlogged.rnc_compa}});

                for (var i = 0; i < res.data.length; i++) {      
                    let row = {username:res.data[i].username,email:res.data[i].email,firstname:res.data[i].first_name,lastname:res.data[i].last_name,date:res.data[i].created_date}
                    this.itemsDriver.push(row);
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
           
        },
        onResetDriver() {
            this.formDriver.firstname = ""
            this.formDriver.lastname = ""
            this.formDriver.email = ""
        },
        onRowSelected(items) {
            this.selectedTable = items;
        },

       
    },
    mounted(){
            this.$emit('childToParent', this.userlogged) 
            this.loadDriver();
    }  

}
</script>

<style>

</style>
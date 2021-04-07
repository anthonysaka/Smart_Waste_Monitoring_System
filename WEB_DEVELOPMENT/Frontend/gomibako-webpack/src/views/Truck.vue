<template>
  <div class="truck">
      <b-container fluid>
          <b-tabs content-class="mt-3" justified>

            <b-tab title="Camiones" active>
                <b-jumbotron class="jumbotron">
                    <div class="card mb-4">
                        <div class="card-body">
                        <h5 class="h5 text-gray-800 my-0"><strong> LISTADO DE CAMIONES</strong></h5>
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
                            <b-table responsive="sm" borderless hover :items="itemsTruck" :fields="fieldsTruck" head-variant="light" selectable
                                select-mode="single" @row-selected="onRowSelectedTruck" :filter="filter"
                                :filter-included-fields="filterOn">
                        
                                <template #cell(editK)="row">
                                    <b-button size="sm" @click="edit(row.item, row.index, $event.target)" class="mr-1">Editar</b-button>
                                    <b-button size="sm"   @click="deleteTruck(row.item, row.index, $event.target)" class="mr-1" variant='danger'>Eliminar</b-button>
                                </template>

                            </b-table>

                             <!-- Edit modal -->
                        <b-modal :id="editModal.id" :title="editModal.title"  hide-footer hide-header body-bg-variant="dark" header-bg-variant="dark" 
                            header-text-variant="dark" size="lg" @hide="resetEditModal" >

                     <b-container @submit.prevent="editTruck">
                        <b-form>
                            <h3 class="mt-4"> EDITAR </h3>
                            <h4 class="mt-4"> INFORMACION GENERAL</h4>
                            <hr class="line">
                            <b-row>
                                <b-col cols="6">
                                    <b-form-group label="Codigo:" label-for="inputCode">
                                        <b-input id="inputCode"  v-model="code" required readonly></b-input>
                                    </b-form-group>
                                </b-col>
                            </b-row>
                            <b-row>
                                <b-col cols="6">
                                    <b-form-group label="No. de placa:" label-for="inputPlaca">
                                        <b-input id="inputPlaca"  v-model="placa" required readonly></b-input>
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
                                    <b-form-group label="Capacidad de carga(Kg):" label-for="inputCarga">
                                        <b-input id="inputCarga" v-model="cap_kg" required placeholder="Ej.:400"></b-input>
                                    </b-form-group>
                                </b-col>
                                <b-col cols="6">
                                    <b-form-group label="Capacidad de volumen (pulg^3):" label-for="inputVol">
                                        <b-input id="inputVol" v-model="cap_vol" required placeholder="Ej.:10000"></b-input>
                                    </b-form-group>
                                </b-col>
                            </b-row>
                            
                        <b-button class="mr-2" type="submit" variant="primary">Guardar</b-button>
                        <b-button @click="$bvModal.hide(editModal.id)" variant="danger">Cancelar</b-button>
                        
                        </b-form>
                    </b-container>

                            
                            
                        </b-modal>
                        </div>
                    </div>
                    </b-col>
                </b-jumbotron>
            </b-tab>

            <b-tab title="[+] Camiones">
                <b-container @submit.prevent="addTruck">
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
                                <b-form-group label="Capacidad de carga(Kg):" label-for="inputCarga">
                                    <b-input id="inputCarga" v-model="cap_kg" required placeholder="Ej.:400"></b-input>
                                </b-form-group>
                            </b-col>
                            <b-col cols="6">
                                <b-form-group label="Capacidad de volumen (pulg^3):" label-for="inputVol">
                                    <b-input id="inputVol" v-model="cap_vol" required placeholder="Ej.:10000"></b-input>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        
                    <b-button class="mr-2" type="submit" variant="primary">Registrar</b-button>
                    <b-button @click="onReset" variant="danger">Cancelar</b-button>
                    
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
        return{
            userlogged: JSON.parse(sessionStorage.getItem('userdata')),
            code:null,
            placa:null,
            ano:null,
            marca:null,
            modelo:null,
            cap_kg:null,
            cap_vol:null,

            fieldsTruck: [
                {
                    key: 'code',
                    label: 'CODE',
                    sortable: true
                },
                {
                    key: 'placa',
                    label: 'PLACA',
                    sortable: true,
                },
                {
                    key: 'year',
                    label: 'A\u00D1O',
                    sortable: true,
                },
                {
                    key: 'marca',
                    label: 'MARCA',
                    sortable: true,
                },
                {
                    key: 'modelo',
                    label: 'MODELO',
                    sortable: true,
                },
                {
                    key: 'capVol',
                    label: 'CAPACIDAD VOLUMENTRICA [pulg^3]',
                    sortable: true,
                },
                {
                    key: 'capPeso',
                    label: 'CAPACIDAD PESO[kg]',
                    sortable: true,
                },
                {
                    key: 'date',
                    label: 'Fecha registro',
                    sortable: true,
                },{
                    key: 'editK',
                    label: 'Opciones',
                   
                },
            ],
            itemsTruck:[],
            selectedTableTruck: null,

            filter: null,
            filterOn:[],
            editModal: {
                id: 'edit-modal',
                title: '',
                content: ''
            },
            auxTruckInfo: []

        }
    },
    methods:{
        edit(item, index, button) {
          
            this.editModal.title = `Row index: ${index}`
            this.editModal.content = this.auxTruckInfo[index]
            this.code = this.auxTruckInfo[index].code
            this.placa = this.auxTruckInfo[index].placa
            this.ano=this.auxTruckInfo[index].ano
            this.marca=this.auxTruckInfo[index].marca
            this.modelo=this.auxTruckInfo[index].modelo
            this.cap_kg=this.auxTruckInfo[index].cap_carga_kg
            this.cap_vol=this.auxTruckInfo[index].cap_carga_vol
            this.$root.$emit('bv::show::modal', this.editModal.id, button)
        },
         resetEditModal() {
            this.editModal.title = ''
            this.editModal.content = ''
         
        },
        async deleteTruck(item, index, button){
            this.fcode = this.auxTruckInfo[index].code
                try{
                 var res = await axios.delete(`${API_URL}/truck`,
                                            {
                                                params:{"code":this.code,}
                                            });
                console.log(res.status)
                  Swal.fire(
                    'Eliminado con exito!',
                    res.response,
                    'success'
                ).then(function() {
                  window.location = "/drivers"
                });
                } catch (error) {
                    Swal.fire(
                        'Uups, ha ocurrido un error!',
                        '',
                        'error'
                    )
                    console.log(error)
                }


        },
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
                Swal.fire(
                    'Registrado con exito!',
                    '',
                    'success'
                ).then(function() {
                   this.loadAvailableTrucks();
                   this.onReset()
                });
            } catch (error) {
                Swal.fire(
                    'Uups, ha ocurrido un error!',
                    '',
                    'error'
                )
                console.log(error)
            }
            
        },
        async editTruck() {
            try {
                var res = await axios.put(`${API_URL}/truck`,
                                            {   "code":this.code,
                                                "ano":this.ano,
                                                "marca": this.marca,
                                                "model": this.modelo,
                                                "cap_kg":this.cap_kg,
                                                "cap_vol":this.cap_vol,
                                            });

                console.log(res.status)
                
                Swal.fire(
                    'Editado con exito!',
                    '',
                    'success'
                ).then(function() {
                    window.location = "/trucks";
                });
            } catch (error) {
                Swal.fire(
                    'Uups, ha ocurrido un error!',
                    '',
                    'error'
                )
                console.log(error)
            }
            
        },
        onReset(){
            this.placa = ""
            this.ano = ""
            this.marca = ""
            this.modelo = ""
            this.cap_kg = ""
            this.cap_vol = ""        
        },
        onRowSelectedTruck(items) {
            this.selectedTableTruck = items;
        },
        async loadAvailableTrucks(){
            try {
                var res = await axios.get(`${API_URL}/truck`,{ params: {rncComp: this.userlogged.rnc_compa}});

               for (var i = 0; i < res.data.length; i++) {      
                    let row = {code:res.data[i].code,placa:res.data[i].placa,year:res.data[i].ano,marca:res.data[i].marca,modelo:res.data[i].modelo,capVol:res.data[i].cap_carga_vol,capPeso:res.data[i].cap_carga_kg,date:res.data[i].created_date}
                    this.itemsTruck.push(row);
                    this.auxTruckInfo.push(res.data[i])
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
            
        },
    },
    mounted(){
        this.$emit('childToParent', this.userlogged)
         this.loadAvailableTrucks();
    }

}
</script>

<style>

</style>
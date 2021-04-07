<template>
    <div class="adminpanel">
        <b-container fluid>
            <b-tabs content-class="mt-3" justified>

                <b-tab title="Listado" active>
                    <b-container fluid>
                        <b-tabs>
                            <b-tab title="Empresas" active>
                                <b-jumbotron class="jumbotron pt-4">
                                    <div class="card mb-4">
                                        <div class="card-body">
                                            <h5 class="h5 text-gray-800 my-0"><strong> LISTADO DE EMPRESAS </strong></h5>
                                        </div>
                                    </div>

                                    <b-container style="display: flex;justify-content: center;">
                                        <b-input-group size="md" class="mb-4 w-50">
                                            <b-form-input v-model="filterCompany" type="search" id="filterInput" placeholder="Escribe para buscar"></b-form-input>
                                        </b-input-group>
                                    </b-container>

                                    <b-col cols="12">
                                        <div class="card ">  
                                            <div class="card-body">
                                                <b-table responsive="sm" borderless hover :items="itemsCompany" :fields="fieldsCompany" head-variant="light" selectable
                                                    select-mode="single" :filter="filterCompany"
                                                    :filter-included-fields="filterOnCompany">

                                                    <template #cell(optsCompa)="row">
                                                        <b-button size="sm"  @click="sh_editCompany(row.item, row.index, $event.target)" class="mr-1">Editar</b-button>
                                                        <b-button size="sm"   @click="deleteCompany(row.item, row.index, $event.target)" class="mr-1" variant='danger'>Eliminar</b-button>
                                                    </template>

                                                </b-table>

                                                <b-modal :id="editModalCompany.id" :title="editModalCompany.title"  hide-footer hide-header body-bg-variant="dark" header-bg-variant="dark" 
                                                    header-text-variant="dark" size="lg" @hide="resetEditModalCompany" >

                                                    <b-container @submit.prevent="editCompany">
                                                            <b-form  >
                                                            <h3 class="mt-4"> EDITAR </h3>
                                                            <h4 class="mt-4"> INFORMACION GENERAL</h4>
                                                            <hr class="line">
                                                
                                                            <b-form-group label="RNC:" label-for="inputRNC">
                                                                <b-input id="inputRNC" v-model="formCompany.rnc" required  readonly placeholder="Ej.:654321">
                                                                </b-input>
                                                            </b-form-group>

                                                            <b-form-group label="Nombre de la empresa:" label-for="inputNameComp">
                                                                <b-form-input id="inputNameComp" v-model="formCompany.name" required placeholder="Ej.: Gomibako.SRL">
                                                                </b-form-input>
                                                            </b-form-group>

                                                            <b-form-group label="Provincia:" label-for="inputProvi">
                                                                <b-form-select id="inputProvi" v-model="formCompany.provincia" :options='provinciaList' required>
                                                                </b-form-select>
                                                            </b-form-group>

                                                            <b-form-group label="Direcion:" label-for="inputAddress">
                                                                <b-form-input id="inputAddress" v-model="formCompany.address" required
                                                                    placeholder="Ej.: Av. 27 de febrero, Santiago de los caballeros"></b-form-input>
                                                            </b-form-group>

                                                            <b-form-group class="mb-4" label="Ubicacion:" >
                                                                    <b-form-input id="inputUbication" v-model="formCompany.coordinates" readonly
                                                                    placeholder="Ej.: Av. 27 de febrero, Santiago de los caballeros"></b-form-input>
                                                            </b-form-group>

                                                            <b-button class="mr-2" type="submit" variant="primary">Guardar</b-button>
                                                            <b-button @click="$bvModal.hide(editModalCompany.id)" variant="danger">Cancelar</b-button>
                                                        </b-form>

                                                    </b-container>
                                                </b-modal>
                                                </div>
                                            </div>
                                        </b-col>

                                </b-jumbotron>
                            </b-tab>

                            
                            <b-tab title="Usuarios" >
                                <b-jumbotron class="jumbotron pt-4">
                                    <div class="card mb-4">
                                        <div class="card-body">
                                            <h5 class="h5 text-gray-800 my-0"><strong> LISTADO DE USUARIOS</strong></h5>
                                        </div>
                                    </div>

                                    <b-container style="display: flex;justify-content: center;">
                                        <b-input-group size="md" class="mb-4 w-50">
                                            <b-form-input v-model="filterUser" type="search" id="filterInput" placeholder="Escribe para buscar"></b-form-input>
                                        </b-input-group>
                                    </b-container>

                                    <b-col cols="12">
                                        <div class="card ">  
                                            <div class="card-body">
                                                <b-table responsive="sm" borderless hover :items="itemsUser" :fields="fieldsUser" head-variant="light" selectable
                                                    select-mode="single" :filter="filterUser"
                                                    :filter-included-fields="filterOnUser">

                                                    <template #cell(optsUser)="row">
                                                        <b-button size="sm"  @click="sh_editUser(row.item, row.index, $event.target)" class="mr-1">Editar</b-button>
                                                        <b-button size="sm"   @click="deleteUser(row.item, row.index, $event.target)" class="mr-1" variant='danger'>Eliminar</b-button>
                                                    </template>
                                                    
                                                </b-table>

                                                <b-modal :id="editModalUser.id" :title="editModalUser.title"  hide-footer hide-header body-bg-variant="dark" header-bg-variant="dark" 
                                                header-text-variant="dark" size="lg" @hide="resetEditModalUser" >
                                                    <b-container>
                                                        <h3 class="mt-4"> EDITAR </h3>
                                                        <h4 class="mt-4"> INFORMACION USUARIO</h4>
                                                        <hr class="line">

                                                        <b-form @submit.prevent="editUser">
                                                             <b-form-group label="ID:" label-for="inputUserID">
                                                                <b-form-input id="inputUserID" v-model="formUser.id" required readonly placeholder="Ej.: ID">
                                                                </b-form-input>
                                                            </b-form-group>
                                                            <b-form-group label="Username:" label-for="inputUsername">
                                                                <b-form-input id="inputUsername" v-model="formUser.username" required readonly placeholder="Ej.: username">
                                                                </b-form-input>
                                                            </b-form-group>
                                                            <b-form-group label="Primer nombre:" label-for="inputUserName">
                                                                <b-form-input id="inputUserName" v-model="formUser.firstname" required placeholder="Ej.: Juan">
                                                                </b-form-input>
                                                            </b-form-group>

                                                            <b-form-group label="Primer apellido:" label-for="inputUserLastname">
                                                                <b-form-input id="inputUserLastname" v-model="formUser.lastname" required placeholder="Ej.: Almonte">
                                                                </b-form-input>
                                                            </b-form-group>

                                                            <b-form-group label="E-mail:" label-for="inputUserEmail">
                                                                <b-form-input id="inputUserEmail" v-model="formUser.email" type="email" required placeholder="Ej.: username@dominio.com">
                                                                </b-form-input>
                                                            </b-form-group>

                                                            <b-form-group class="mb-4" label="Tipo:" label-for="inputUserType">
                                                                 <b-form-input id="inputUserType" v-model="formUser.type" required readonly>
                                                                </b-form-input>
                                                            </b-form-group>

                                                            <b-form-group class="mb-4" label="Empresa a la que pertenece:" label-for="inputUserRNC">
                                                               <b-form-input id="inputUserRNC" v-model="formUser.rncComp" readonly required>
                                                                </b-form-input>
                                                            </b-form-group>

                                                            <b-button class="mr-2" type="submit" variant="primary">Guardar</b-button>
                                                            <b-button @click="$bvModal.hide(editModalUser.id)" variant="danger">Cancelar</b-button>
                                                        </b-form>
                                                    </b-container>

                                                </b-modal>

                                            </div>
                                        </div>
                                    </b-col>
                                </b-jumbotron>
                            </b-tab>

                            <b-tab title="Basureros">
                                <b-jumbotron class="jumbotron pt-4">
                                    <div class="card mb-4">
                                        <div class="card-body">
                                            <h5 class="h5 text-gray-800 my-0"><strong> LISTADO DE BASUREROS</strong></h5>
                                        </div>
                                    </div>

                                    <b-container style="display: flex;justify-content: center;">
                                        <b-input-group size="md" class="mb-4 w-50">
                                            <b-form-input v-model="filterBins" type="search" id="filterInput" placeholder="Escribe para buscar"></b-form-input>
                                        </b-input-group>
                                    </b-container>

                                    <b-col cols="12">
                                        <div class="card ">  
                                            <div class="card-body">
                                                <b-table responsive="sm" borderless hover :items="itemsBins" :fields="fieldsBins" head-variant="light" selectable
                                                    select-mode="single" :filter="filterBins"
                                                    :filter-included-fields="filterOnBins">

                                                    <template #cell(optsBin)="row">
                                                        <b-button size="sm"  @click="sh_editBin(row.item, row.index, $event.target)" class="mr-1">Editar</b-button>
                                                       <!-- <b-button size="sm"   @click="deleteBin(row.item, row.index, $event.target)" class="mr-1" variant='danger'>Eliminar</b-button>-->
                                                    </template>
                                                    
                                                </b-table>

                                                <b-modal :id="editModalBins.id" :title="editModalBins.title"  hide-footer hide-header body-bg-variant="dark" header-bg-variant="dark" 
                                                header-text-variant="dark" size="lg" @hide="resetEditModalBin" >
                                                    <b-container>
                                                        <h3 class="mt-4"> EDITAR </h3>
                                                        <h4 class="mt-4"> INFORMACION BASURERO</h4>
                                                        <hr class="line">

                                                         <b-form @submit.prevent="editBasurero">                       
                        
                                                            <b-form-group label="EUI:" label-for="inputDeviceEUI">
                                                                <b-form-input id="inputDeviceEUI" v-model="formBin.deviceEui" required readonly placeholder="Ej.: 01A3B45B7890F23A">
                                                                </b-form-input>
                                                            </b-form-group>

                                                            <b-form-group label="Nombre:" label-for="inputDeviceName">
                                                                <b-form-input id="inputDeviceName" v-model="formBin.name" required readonly placeholder="Ej.: 01A3B45B7890F23A">
                                                                </b-form-input>
                                                            </b-form-group>

                                                            <b-form-group label="Empresa a la que pertenece:" label-for="inputBinCompa">
                                                                <b-form-select id="inputBinCompa" v-model="formBin.rncComp" :options="listAvailableCompanies" required></b-form-select>
                                                            </b-form-group>

                                                            <b-form-group class="mb-4" label="Ubicacion:" >
                                                                    <b-form-input id="inputUbication" v-model="formBin.location" required
                                                                    placeholder="Ej.: Lat, Long"></b-form-input>
                                                            </b-form-group>


                                                            <b-form-group label="Tipo:" label-for="inputBinType">
                                                                <b-form-select id="inputBinType" v-model="formBin.type" :options="listBinTypes" required></b-form-select>
                                                            </b-form-group>

                                                            <b-form-group label="Tipo(s) de material de basura:" v-if="formBin.type == 'Tradicional - 1 contenedor'">
                                                                <b-form-radio-group
                                                                    id="checkbox-group-1"
                                                                    v-model="formBin.selectedMaterial"
                                                                    :options="chk_materialbasura"
                                                                    :checked="formBin.material"
                                                                    name="flavour-1"
                                                                > </b-form-radio-group>
                                                            </b-form-group>

                                                            <b-form-group class="mb-4" label="Descripcion:" label-for="inputBinDescrip">
                                                                <b-form-input id="inputBinDescrip" v-model="formBin.descrip" required placeholder="Ej.: Gomibako.SRL">
                                                                </b-form-input>
                                                            </b-form-group>

                                                            <b-button class="mr-2" type="submit" variant="primary">Guardar</b-button>
                                                            <b-button @click="$bvModal.hide(editModalBins.id)" variant="danger">Cancelar</b-button>

                                                        </b-form>

                                                     
                                                    </b-container>

                                                </b-modal>

                                            </div>
                                        </div>
                                    </b-col>
                                </b-jumbotron>
                            </b-tab>

                        </b-tabs>
                    </b-container>
                  

                </b-tab>

                <b-tab title="[+] Empresa" >
                    <b-container>
                        <h4 class="mt-4"> INFORMACION EMPRESA </h4>
                        <hr class="line">

                        <b-form @submit.prevent="addCompany" v-if="show">

                            <b-form-group label="RNC:" label-for="inputRNC">
                                <b-input id="inputRNC" v-model="formCompany.rnc" required placeholder="Ej.:654321">
                                </b-input>
                            </b-form-group>

                            <b-form-group label="Nombre de la empresa:" label-for="inputNameComp">
                                <b-form-input id="inputNameComp" v-model="formCompany.name" required placeholder="Ej.: Gomibako.SRL">
                                </b-form-input>
                            </b-form-group>

                            <b-form-group label="Provincia:" label-for="inputProvi">
                                <b-form-select id="inputProvi" v-model="formCompany.provincia" :options='provinciaList' required>
                                </b-form-select>
                            </b-form-group>

                            <b-form-group label="Direcion:" label-for="inputAddress">
                                <b-form-input id="inputAddress" v-model="formCompany.address" required
                                    placeholder="Ej.: Av. 27 de febrero, Santiago de los caballeros"></b-form-input>
                            </b-form-group>

                            <b-form-group class="mb-4" label="Ubicacion:" >
                                <h5 id="coordinatesCompa" class="coordinates"><b-badge variant="primary"></b-badge></h5>
                                <div class="card shadow">
                                    <div class="card-body">
                                        <div id="mapCompa" style="height: 350px;
                                    width: 100%;"></div>
                                    </div>
                                </div>

                            </b-form-group>

                            <b-button class="mr-2" type="submit" variant="primary">Registrar</b-button>
                            <b-button @click="onResetCompany" variant="danger">Cancelar</b-button>
                        </b-form>

                    </b-container>
                    
                </b-tab>

                <b-tab title="[+] Usuario a empresa">
                    <b-container>
                        <h4 class="mt-4"> INFORMACION USUARIO </h4>
                    <hr class="line">

                    <b-form @submit.prevent="addUser" v-if="show">
                        <b-form-group label="Primer nombre:" label-for="inputUserName">
                            <b-form-input id="inputUserName" v-model="formUser.firstname" required placeholder="Ej.: Juan">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group label="Primer apellido:" label-for="inputUserLastname">
                            <b-form-input id="inputUserLastname" v-model="formUser.lastname" required placeholder="Ej.: Almonte">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group label="E-mail:" label-for="inputUserEmail">
                            <b-form-input id="inputUserEmail" v-model="formUser.email" type="email" required placeholder="Ej.: username@dominio.com">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group class="mb-4" label="Tipo:" label-for="inputUserType">
                            <b-form-select id="inputUserType" v-model="formUser.type" :options="listTypes" required></b-form-select>
                        </b-form-group>


                         <b-form-group class="mb-4" label="Empresa a la que pertenece:" label-for="inputUserCompany">
                            <b-form-select id="inputUserCompany" v-model="formUser.rncComp" :options="listAvailableCompanies" required></b-form-select>
                        </b-form-group>

                        <b-button class="mr-2" type="submit" variant="primary">Aplicar</b-button>
                        <b-button @click="onResetUser" variant="danger">Cancelar</b-button>
                    </b-form>
                    </b-container>
                    
                </b-tab>

                <b-tab title="[+] Basurero">
                    <b-container>
                        <h4 class="mt-4"> INFORMACION BASURERO </h4>
                    <hr class="line">

                    <b-form @submit.prevent="addBasurero" v-if="show">                       
                        
                        <b-form-group label="DeviceEUI:" label-for="inputDeviceEUI">
                            <b-form-input id="inputDeviceEUI" v-model="formBin.deviceEui" required placeholder="Ej.: 01A3B45B7890F23A">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group label="Empresa a la que pertenece:" label-for="inputBinCompa">
                            <b-form-select id="inputBinCompa" v-model="formBin.rncComp" :options="listAvailableCompanies" required></b-form-select>
                        </b-form-group>

                        <b-form-group label="Ubicacion:" >
                            <h5 id="coordinates" class="coordinates"><b-badge variant="primary"></b-badge></h5>
                            <div class="card shadow">
                                <div class="card-body">
                                    <div id="map" style="height: 350px;
                                width: 100%;"></div>
                                </div>
                            </div>

                        </b-form-group>

                        <b-form-group label="Tipo:" label-for="inputBinType">
                            <b-form-select id="inputBinType" v-model="formBin.type" :options="listBinTypes" required></b-form-select>
                        </b-form-group>

                        <b-form-group label="Tipo(s) de material de basura:" v-if="formBin.type == 'Tradicional - 1 contenedor'">
                            <b-form-radio-group
                                id="checkbox-group-1"
                                v-model="formBin.selectedMaterial"
                                :options="chk_materialbasura"
                                name="flavour-1"
                            > </b-form-radio-group>
                        </b-form-group>

                        <b-form-group class="mb-4" label="Descripcion:" label-for="inputBinDescrip">
                            <b-form-input id="inputBinDescrip" v-model="formBin.descrip" required placeholder="Ej.: Gomibako.SRL">
                            </b-form-input>
                        </b-form-group>

                        <b-button class="mr-2" type="submit" variant="primary">Aplicar</b-button>
                        <b-button @click="onResetBasurero" variant="danger">Cancelar</b-button>

                    </b-form>
                    </b-container>
                    
                </b-tab>
           
            </b-tabs>

        </b-container>
    </div>
</template>

<script>
import axios from 'axios';
import mapboxgl from "mapbox-gl";
const API_URL = process.env.API_URL;
import Swal from 'sweetalert2';

export default {
    data() {
        return {
            userlogged: JSON.parse(sessionStorage.getItem('userdata')),
            formCompany: {
                rnc: '',
                name: '',
                provincia: '',
                address:'',
                coordinates:''
            },
            formUser: {
                firstname: '',
                lastname:'',
                email:'',
                rncComp:'',
                type:'',
                id:'',
                username:''
                
            },
            formBin: {
                deviceEui:'',
                rncComp:'',
                type:'',
                descrip:'',
                selectedMaterial:'plastico/metal/papel-carton',
                name:'',
                material:'',
                location:'',

            },
            provinciaList: ['La Vega','Puerto Plata','Punta Cana','Santiago', 'Santo Domingo'],
            listBinTypes: ['Tradicional - 1 contenedor','Reciclaje - 3 contenedores'],
            listAvailableCompanies: [],
            listTypes:['Admin','Cliente'],
            chk_materialbasura:[
                { text: 'Plastico', value: 'plastico' },
                { text: 'Metal', value: 'metal' },
                { text: 'Papel/Carton', value: 'papel/carton' },
                { text: 'Organico', value: 'organico' }
                ],
            show: true,
            accessToken: 'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw',

            filterCompany: null,
            filterOnCompany: [],
            itemsCompany: [],
            fieldsCompany:[
                {
                    key: 'rnc',
                    label: 'RNC',
                    sortable: true
                },
                {
                    key: 'name',
                    label: 'NOMBRE',
                    sortable: true
                },
                {
                    key: 'provincia',
                    label: 'PROVINCIA',
                    sortable: true,
                },
                {
                    key: 'address',
                    label: 'DIRECCION',
                    sortable: true,
                },
                {
                    key: 'coordinates',
                    label: 'COORDS',
                    sortable: true,
                },
                {
                    key: 'created_date',
                    label: 'FECHA REGISTRO',
                    sortable: true,
                },
                {
                    key: 'optsCompa',
                    label: 'Opciones',
                   
                },
            ],
            auxCompanyInfo: [],
            editModalCompany: {
                id: 'edit-modal-company',
                title: '',
                content: ''
            },

            filterUser: null,
            filterOnUser: [],
            itemsUser: [],
            fieldsUser:[
                {
                    key: 'id',
                    label: 'ID',
                    sortable: true
                },
                {
                    key: 'username',
                    label: 'USERNAME',
                    sortable: true
                },
                {
                    key: 'email',
                    label: 'EMAIL',
                    sortable: true
                },
                {
                    key: 'first_name',
                    label: 'NOMBRE',
                    sortable: true,
                },
                {
                    key: 'last_name',
                    label: 'APELLIDO',
                    sortable: true,
                },
                {
                    key: 'type',
                    label: 'TIPO',
                    sortable: true,
                },
                {
                    key: 'rnc_compa',
                    label: 'RNC',
                    sortable: true,
                },
                {
                    key: 'created_date',
                    label: 'Fecha Registro',
                    sortable: true,
                },
                {
                    key: 'optsUser',
                    label: 'Opciones',
                   
                },
            ],
            auxUserInfo: [],
            editModalUser: {
                id: 'edit-modal-user',
                title: '',
                content: ''
            },

            filterBins: null,
            filterOnBins: [],
            fieldsBins: [
                {
                    key: 'name',
                    label: 'NOMBRE',
                    sortable: true
                },
                {
                    key: 'description',
                    label: 'DRESCRIP.',
                    sortable: true
                },
                {
                    key: 'deviceeui',
                    label: 'EUI',
                    sortable: true
                },   
                {
                    key: 'type',
                    label: 'TIPO',
                    sortable: true,
                },
                {
                    key: 'material',
                    label: 'CONTENIDO',
                    sortable: true,
                },
                {
                    key: 'location',
                    label: 'UBICACION',
                    sortable: true,
                },
                {
                    key: 'rnc_compa',
                    label: 'RNC',
                    sortable: true
                }, 
                {
                    key: 'description',
                    label: 'DESCRIPCION',
                    sortable: true,
                },
                {
                    key: 'date',
                    label: 'FECHA REGISTRO',
                    sortable: true,
                },
                {
                    key: 'optsBin',
                    label: 'Opciones',
                   
                },

            ],
            itemsBins: [ ],
            auxBinsInfo: [],
            editModalBins: {
                id: 'edit-modal-bin',
                title: '',
                content: ''
            },

    
        }
    },
    methods: {
        sh_editCompany(item, index, button) {
          
            this.editModalCompany.title = `Row index: ${index}`
            this.editModalCompany.content = this.auxCompanyInfo[index]
            console.log(this.editCompany.content)
            this.formCompany.rnc = this.auxCompanyInfo[index].rnc
            this.formCompany.name = this.auxCompanyInfo[index].name
            this.formCompany.provincia = this.auxCompanyInfo[index].provincia
            this.formCompany.address = this.auxCompanyInfo[index].address
            this.formCompany.coordinates = this.auxCompanyInfo[index].coordinates
            this.$root.$emit('bv::show::modal', this.editModalCompany.id, button)
        },
        async editCompany(evt) {
            try {
                evt.preventDefault()
                 var res = await axios.put(`${API_URL}/clientCompany/0`,
                                            {
                                                "rnc":this.formCompany.rnc,
                                                "name":this.formCompany.name,
                                                "provincia":this.formCompany.provincia,
                                                "address":this.formCompany.address,
                                            });

                console.log(res.status)
               
                Swal.fire(
                    'Modificado con exito!',
                    '',
                    'success'
                ).then(function() {
                    window.location = "/globaladmi"
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
        async deleteCompany(item, index, button){
            this.formCompany.rnc = this.auxCompanyInfo[index].rnc
                try{
                 var res = await axios.delete(`${API_URL}/clientCompany/0`,
                                            {
                                                params:{"rnc":this.formCompany.rnc,}
                                            });

                console.log(res.status)
                  Swal.fire(
                    'Eliminado con exito!',
                    res.response,
                    'success'
                ).then(function() {
                  this.loadAvailableCompanies()
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
        resetEditModalCompany() {
            this.editModalCompany.title = ''
            this.editModalCompany.content = ''
         
        },
        
        sh_editUser(item, index, button) {            
          
            this.editModalUser.title = `Row index: ${index}`
            this.editModalUser.content = this.auxUserInfo[index]

            this.formUser.id = this.auxUserInfo[index].id
            this.formUser.username = this.auxUserInfo[index].username
            this.formUser.firstname = this.auxUserInfo[index].first_name
            this.formUser.lastname = this.auxUserInfo[index].last_name
            this.formUser.email = this.auxUserInfo[index].email
            this.formUser.type = this.auxUserInfo[index].type
            this.formUser.rncComp = this.auxUserInfo[index].rnc_compa
         
            this.$root.$emit('bv::show::modal', this.editModalUser.id, button)
        },
        async editUser(evt) {
            try {
                evt.preventDefault()
                 var res = await axios.put(`${API_URL}/user`,
                                            {
                                                "id":this.formUser.id,
                                                "firstname": this.formUser.firstname,
                                                "lastname":this.formUser.lastname,
                                                "email":this.formUser.email,
                                            });

                console.log(res.status)
               
                Swal.fire(
                    'Modificado con exito!',
                    '',
                    'success'
                ).then(function() {
                    window.location = "/globaladmin"
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
        async deleteUser(item, index, button){
            this.formUser.id = this.auxUserInfo[index].id
                try{
                 var res = await axios.delete(`${API_URL}/user`,
                                            {
                                                params:{"id":this.formUser.id,}
                                            });
                console.log(res.status)
                  Swal.fire(
                    'Eliminado con exito!',
                    res.response,
                    'success'
                ).then(function() {
                  window.location = "/globaladmin"
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
        resetEditModalUser() {
            this.editModalUser.title = ''
            this.editModalUser.content = ''
         
        },

        sh_editBin(item, index, button) {            
          
            this.editModalBins.title = `Row index: ${index}`
            this.editModalBins.content = this.auxBinsInfo[index]

            this.formBin.name = this.auxBinsInfo[index].name
            this.formBin.deviceEui = this.auxBinsInfo[index].deviceeui
            this.formBin.rncComp = this.auxBinsInfo[index].rnc_compa
            this.formBin.type = this.auxBinsInfo[index].type
            this.formBin.material = this.auxBinsInfo[index].material_waste
            this.formBin.descrip = this.auxBinsInfo[index].description
            this.formBin.location = this.auxBinsInfo[index].coordinates

            this.$root.$emit('bv::show::modal', this.editModalBins.id, button)
        },
        async editBasurero(evt) {
            try {
                evt.preventDefault()
                 var res = await axios.put(`${API_URL}/dustbin/0`,
                                            {
                                                "deviceeui":this.formBin.deviceEui,
                                                "coordinates": this.formBin.location,
                                                "description":this.formBin.location,
                                                "type": this.formBin.type,
                                                "material":this.formBin.selectedMaterial,
                                                "rncComp": this.formBin.rncComp.split("RNC:")[1],
                                            });

                console.log(res.status)
               
                Swal.fire(
                    'Modificado con exito!',
                    '',
                    'success'
                ).then(function() {
                    window.location = "/globaladmin"
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
        resetEditModalBin() {
            this.editModalBins.title = ''
            this.editModalBins.content = ''
         
        },
        async addCompany() {
            try {
                var coord = document.getElementById('coordinatesCompa').textContent.split(" ")
                var coor = coord[1]+","+coord[3];
                var res = await axios.post(`${API_URL}/clientCompany/0`,
                                            {
                                                "rnc":this.formCompany.rnc,
                                                "name":this.formCompany.name,
                                                "provincia": this.formCompany.provincia,
                                                "address": this.formCompany.address,
                                                "coordinates":coor
                                            });

                console.log(res.status)
                  Swal.fire(
                    'Registrado con exito!',
                    res.response,
                    'success'
                )
                this.loadAvailableCompanies()
            } catch (error) {
                Swal.fire(
                    'Uups, ha ocurrido un error!',
                    '',
                    'error'
                )
                console.log(error)
            }
            
        },
        async addUser(evt) {
            try {
                evt.preventDefault()
                 var res = await axios.post(`${API_URL}/user`,
                                            {
                                                "firstname":this.formUser.firstname,
                                                "lastname":this.formUser.lastname,
                                                "email": this.formUser.email,
                                                "rncComp": this.formUser.rncComp.split("RNC:")[1],
                                                "typeU":this.formUser.type
                                            });

                console.log(res.status)
                this.onResetUser();
                Swal.fire(
                    'Registrado con exito!',
                    res.response,
                    'success'
                )
                this.loadUser()
                
            } catch (error) {
                Swal.fire(
                    'Uups, ha ocurrido un error!',
                    '',
                    'error'
                )
                console.log(error)
            }
            
        },
        async addBasurero(evt){
            try {
                evt.preventDefault()
                var coord = document.getElementById('coordinates').textContent.split(" ")
                var coor = parseFloat(coord[1]).toFixed(6)+","+parseFloat(coord[3]).toFixed(6);
                var res = await axios.post(`${API_URL}/dustbin/0`,
                                            {
                                                "deviceEui":this.formBin.deviceEui,
                                                "rncComp":this.formBin.rncComp.split("RNC:")[1],
                                                "type": this.formBin.type,
                                                "descrip": this.formBin.descrip,
                                                "mWaste": this.formBin.selectedMaterial,
                                                "coordinates": coor
                                            });
                console.log(res.status)
                this.onResetBasurero();
                Swal.fire(
                    'Registrado con exito!',
                    '',
                    'success'
                )
            } catch (error) {
                Swal.fire(
                    'Uups, ha ocurrido un error!',
                    '',
                    'error'
                )
                console.log(error)
            }
        },
        onResetCompany() {
            this.formCompany.rnc = ""
            this.formCompany.name = "",
            this.formCompany.provincia = ""
            this.formCompany.address = ""
           
        },
        onResetUser() {
            this.formUser.firstname = ""
            this.formUser.lastname = ""
            this.formUser.email = ""
            this.formUser.rncComp = ""   
        },
        onResetBasurero() {
            this.formBin.deviceEui = ""
            this.formBin.rncComp = ""
            this.formBin.type = ""
            this.formBin.descrip = ""
            this.formBin.selectedMaterial = ""
              
        },        
        async loadAvailableCompanies(){
            try {
                var res = await axios.get(`${API_URL}/clientCompany/0`);

                for (var i = 0; i < res.data.length; i++) {
                    this.listAvailableCompanies.push("NOMBRE: " + res.data[i].name + " - RNC:" + res.data[i].rnc)        
                    let row = {rnc:res.data[i].rnc,name:res.data[i].name,provincia:res.data[i].provincia,address:res.data[i].address,
                                coordinates:res.data[i].coordinates,created_date:res.data[i].created_date}
                    this.itemsCompany.push(row);
                    this.auxCompanyInfo.push(res.data[i])
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }


        },
        async loadUser(){
            try {
                var res = await axios.get(`${API_URL}/user`);

                for (var i = 0; i < res.data.length; i++) {
                    let row = {id:res.data[i].id,username:res.data[i].username,email:res.data[i].email,first_name:res.data[i].first_name,last_name:res.data[i].last_name,
                                type:res.data[i].type,rnc_compa:res.data[i].rnc_compa,created_date:res.data[i].created_date}
                    this.itemsUser.push(row);
                    this.auxUserInfo.push(res.data[i])
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }


        },
        async loadAvailableBins(){
            try {
                console.log(this.userlogged.rnc_compa)
                var res = await axios.get(`${API_URL}/dustbin/2`);

                for (var i = 0; i < res.data.length; i++) {
                    let row = {name:res.data[i].name,type:res.data[i].type,material:res.data[i].material_waste,location:res.data[i].coordinates,description:res.data[i].description,
                        deviceeui: res.data[i].deviceeui,rnc_compa:res.data[i].rnc_compa,date:res.data[i].created_date}
                    this.itemsBins.push(row) 
                    this.auxBinsInfo.push(res.data[i])
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
        },
        create_map_point_dragdable_bin(){
            mapboxgl.accessToken = this.accessToken;
            var coordinates = document.getElementById('coordinates');
            var map = new mapboxgl.Map({
                
                    container: "map",
                    style: "mapbox://styles/mapbox/streets-v11",
                    center: [-70.703692, 19.415888],
                    zoom: 11,
                });
            var canvas = map.getCanvasContainer();
            var geojson = {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-70.703692, 19.415888]
                    }
                }]
            };
            

            function onMove(e) {
                var coords = e.lngLat;

                // Set a UI indicator for dragging.
                canvas.style.cursor = 'grabbing';

                // Update the Point feature in `geojson` coordinates
                // and call setData to the source layer `point` on it.
                geojson.features[0].geometry.coordinates = [coords.lng, coords.lat];
                map.getSource('point').setData(geojson);

            }

            function onUp(e) {
                var coords = e.lngLat;
                // Print the coordinates of where the point had
                // finished being dragged to on the map.
                coordinates.style.display = 'block';
                coordinates.innerHTML =
                    'Long: ' + coords.lng + ' Lat: ' + coords.lat;
                canvas.style.cursor = '';

                // Unbind mouse/touch events
                map.off('mousemove', onMove);
                map.off('touchmove', onMove);
            }

            map.on('load', function () {
                // Add a single point to the map
                map.addSource('point', {
                    'type': 'geojson',
                    'data': geojson
                });

                map.addLayer({
                    'id': 'point',
                    'type': 'circle',
                    'source': 'point',
                    'paint': {
                        'circle-radius': 10,
                        'circle-color': '#3887be'
                    }
                });

                // When the cursor enters a feature in the point layer, prepare for dragging.
                map.on('mouseenter', 'point', function () {
                    map.setPaintProperty('point', 'circle-color', '#3bb2d0');
                    canvas.style.cursor = 'move';
                });

                map.on('mouseleave', 'point', function () {
                    map.setPaintProperty('point', 'circle-color', '#3887be');
                    canvas.style.cursor = '';
                });

                map.on('mousedown', 'point', function (e) {
                    // Prevent the default map drag behavior.
                    e.preventDefault();

                    canvas.style.cursor = 'grab';

                    map.on('mousemove', onMove);
                    map.once('mouseup', onUp);
                });

                map.on('touchstart', 'point', function (e) {
                    if (e.points.length !== 1) return;

                    // Prevent the default map drag behavior.
                    e.preventDefault();

                    map.on('touchmove', onMove);
                    map.once('touchend', onUp);
                });
            });
        },
        create_map_point_dragdable_compa(){
            mapboxgl.accessToken = this.accessToken;
            var coordinates = document.getElementById('coordinatesCompa');
            var map = new mapboxgl.Map({
                
                    container: "mapCompa",
                    style: "mapbox://styles/mapbox/streets-v11",
                    center: [-70.703692, 19.415888],
                    zoom: 11,
                });
            var canvas = map.getCanvasContainer();
            var geojson = {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-70.703692, 19.415888]
                    }
                }]
            };

            function onMove(e) {
                var coords = e.lngLat;

                // Set a UI indicator for dragging.
                canvas.style.cursor = 'grabbing';

                // Update the Point feature in `geojson` coordinates
                // and call setData to the source layer `point` on it.
                geojson.features[0].geometry.coordinates = [coords.lng, coords.lat];
                map.getSource('point').setData(geojson);

            }

            function onUp(e) {
                var coords = e.lngLat;

                // Print the coordinates of where the point had
                // finished being dragged to on the map.
                coordinates.style.display = 'block';
                coordinates.innerHTML =
                    'Long: ' + coords.lng + ' Lat: ' + coords.lat;
                canvas.style.cursor = '';

                // Unbind mouse/touch events
                map.off('mousemove', onMove);
                map.off('touchmove', onMove);
            }

            map.on('load', function () {
                // Add a single point to the map
                map.addSource('point', {
                    'type': 'geojson',
                    'data': geojson
                });

                map.addLayer({
                    'id': 'point',
                    'type': 'circle',
                    'source': 'point',
                    'paint': {
                        'circle-radius': 10,
                        'circle-color': '#3887be'
                    }
                });

                // When the cursor enters a feature in the point layer, prepare for dragging.
                map.on('mouseenter', 'point', function () {
                    map.setPaintProperty('point', 'circle-color', '#3bb2d0');
                    canvas.style.cursor = 'move';
                });

                map.on('mouseleave', 'point', function () {
                    map.setPaintProperty('point', 'circle-color', '#3887be');
                    canvas.style.cursor = '';
                });

                map.on('mousedown', 'point', function (e) {
                    // Prevent the default map drag behavior.
                    e.preventDefault();

                    canvas.style.cursor = 'grab';

                    map.on('mousemove', onMove);
                    map.once('mouseup', onUp);
                });

                map.on('touchstart', 'point', function (e) {
                    if (e.points.length !== 1) return;

                    // Prevent the default map drag behavior.
                    e.preventDefault();

                    map.on('touchmove', onMove);
                    map.once('touchend', onUp);
                });
            });       
        },
    },
    mounted() {
        this.$emit('childToParent', this.userlogged)
        this.loadAvailableCompanies();
        this.create_map_point_dragdable_bin();
        this.create_map_point_dragdable_compa();
        this.loadUser()
        this.loadAvailableBins()
                        
    }
}
</script>

<style>

</style>
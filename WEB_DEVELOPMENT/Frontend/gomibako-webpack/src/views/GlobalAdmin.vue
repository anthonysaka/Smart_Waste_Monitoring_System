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
                                                            <b-button size="sm"  class="mr-1">Editar</b-button>
                                                            <b-button size="sm"  class="mr-1">Eliminar</b-button>
                                                        </template>
                                                      


                                                    </b-table>
                                                </div>
                                            </div>
                                        </b-col>

                                </b-jumbotron>
                            </b-tab>
                            <b-tab title="Usuarios" >
                            </b-tab>
                            <b-tab title="Basureros">
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
                address:''
            },
            formUser: {
                firstname: '',
                lastname:'',
                email:'',
                rncComp:''
                
            },
            formBin: {
                deviceEui:'',
                rncComp:'',
                type:'',
                descrip:'',
                selectedMaterial:'plastico/metal/papel-carton',
                
            },
            provinciaList: ['La Vega','Puerto Plata','Punta Cana','Santiago', 'Santo Domingo'],
            listBinTypes: ['Tradicional - 1 contenedor','Reciclaje - 3 contenedores'],
            listAvailableCompanies: [],
            chk_materialbasura:[
                { text: 'Plastico', value: 'plastico' },
                { text: 'Metal', value: 'metal' },
                { text: 'Papel/Carton', value: 'papel/carton' },
                { text: 'Organico', value: 'organico' }
                ],
            show: true,
            accessToken: 'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw',

            filterCompany: null,
            itemsCompany: [],
            fieldsCompany:[
                {
                    key: 'rnc',
                    label: 'RNC',
                    sortable: true
                },
                {
                    key: 'name',
                    label: 'Nombre',
                    sortable: true
                },
                {
                    key: 'provincia',
                    label: 'Provincia',
                    sortable: true,
                },
                {
                    key: 'address',
                    label: 'Direccion',
                    sortable: true,
                },
                {
                    key: 'coordinates',
                    label: 'Coords',
                    sortable: true,
                },
                {
                    key: 'created_date',
                    label: 'Fecha Registro',
                    sortable: true,
                },
                {
                    key: 'optsCompa',
                    label: 'Opciones',
                   
                },
            ]
    
        }
    },
    methods: {
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
                                                "rncComp": this.formUser.rncComp.split("RNC:")[1]
                                            });

                console.log(res.status)
                this.onResetUser();
                Swal.fire(
                    'Registrado con exito!',
                    res.response,
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
                        
    }
}
</script>

<style>

</style>
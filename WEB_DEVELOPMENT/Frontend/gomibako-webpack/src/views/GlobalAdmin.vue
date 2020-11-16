<template>
    <div class="adminpanel">
        <b-container>
            <b-tabs content-class="mt-3" justified>

                <b-tab title="Listado">

                </b-tab>

                <b-tab title="(+) Empresa" active>
                    <h4 class="mt-4"> INFORMACION EMPRESA </h4>
                    <hr class="line">

                    <b-form @submit="addCompany" v-if="show">

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

                        <b-form-group label="Ubicacion:" >
                            <h5 id="coordinatesCompa" class="coordinates"><b-badge variant="primary"></b-badge></h5>
                            <div class="card shadow">
                                <div class="card-body">
                                    <div id="mapCompa" style="height: 250px;
                                width: 100%;"></div>
                                </div>
                            </div>

                        </b-form-group>

                        <b-button class="mr-2" type="submit" variant="primary">Aplicar</b-button>
                        <b-button variant="danger">Cancelar</b-button>
                    </b-form>
                </b-tab>

                <b-tab title="(+) Usuario a empresa">
                    <h4 class="mt-4"> INFORMACION USUARIO </h4>
                    <hr class="line">

                    <b-form @submit="addUser" v-if="show">
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

                         <b-form-group label="Empresa a la que pertenece:" label-for="inputUserCompany">
                            <b-form-select id="inputUserCompany" v-model="formUser.rncComp" :options="listAvailableCompanies" required></b-form-select>
                        </b-form-group>

                        <b-button class="mr-2" type="submit" variant="primary">Aplicar</b-button>
                        <b-button variant="danger">Cancelar</b-button>
                    </b-form>
                </b-tab>

                <b-tab title="(+) Basurero">
                    <h4 class="mt-4"> INFORMACION BASURERO </h4>
                    <hr class="line">

                    <b-form @submit="addBasurero" v-if="show">                       
                        
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
                                    <div id="map" style="height: 250px;
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

                        <b-form-group label="Descripcion:" label-for="inputBinDescrip">
                            <b-form-input id="inputBinDescrip" v-model="formBin.descrip" required placeholder="Ej.: Gomibako.SRL">
                            </b-form-input>
                        </b-form-group>

                        <b-button class="mr-2" type="submit" variant="primary">Aplicar</b-button>
                        <b-button variant="danger">Cancelar</b-button>

                    </b-form>

                </b-tab>
           
            </b-tabs>

        </b-container>



    </div>
</template>

<script>
import axios from 'axios';
import mapboxgl from "mapbox-gl";

export default {
    data() {
        return {
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
            listBinTypes: ['Tradicional - 1 contenedor','Reciclaje - 3 contenedores (plastico/metal/papel-carton)'],
            listAvailableCompanies: [],
            chk_materialbasura:[
                { text: 'Plastico', value: 'plastico' },
                { text: 'Metal', value: 'metal' },
                { text: 'Papel/Carton', value: 'papel/carton' },
                { text: 'Organico', value: 'organico' }
                ],
            show: true,
            accessToken: 'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw',
            geojsonLocationBin: null,
            geojsonLocationCompa: null,
        }
    },
    methods: {
        async addCompany() {
            try {
                 var res = await axios.post('http://localhost:5000/gomibako/internalapi/1.0/clientCompany',
                                            {
                                                "rnc":this.formCompany.rnc,
                                                "name":this.formCompany.name,
                                                "provincia": this.formCompany.provincia,
                                                "address": this.formCompany.address,
                                                "coordinates":this.geojsonLocationCompa
                                            });

                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
            
        },
        async addUser(evt) {
            try {
                evt.preventDefault()
                 var res = await axios.post('http://localhost:5000/gomibako/internalapi/1.0/user',
                                            {
                                                "firstname":this.formUser.firstname,
                                                "lastname":this.formUser.lastname,
                                                "email": this.formUser.email,
                                                "rncComp": this.formUser.rncComp.split("RNC:")[1]
                                            });

                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
            
        },
        async addBasurero(evt){
            try {
                evt.preventDefault()
                var res = await axios.post('http://localhost:5000/gomibako/internalapi/1.0/dustbin/0',
                                            {
                                                "deviceEui":this.formBin.deviceEui,
                                                "rncComp":this.formBin.rncComp.split("RNC:")[1],
                                                "type": this.formBin.type,
                                                "descrip": this.formBin.descrip,
                                                "mWaste": this.formBin.selectedMaterial,
                                                "coordinates":this.geojsonLocationBin
                                            });
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
        },
        onReset(evt) {
            evt.preventDefault()
            // Reset our form values
            this.form.email = ''
            this.form.name = ''
            this.form.food = null
            this.form.checked = []
            // Trick to reset/clear native browser form validation state
            this.show = false
            this.$nextTick(() => {
                this.show = true
            })
        },
        async loadAvailableCompanies(){
            try {
                var res = await axios.get('http://localhost:5000/gomibako/internalapi/1.0/clientCompany');

                for (var i = 0; i < res.data.length; i++) {
                    this.listAvailableCompanies.push("NOMBRE: " + res.data[i].name + " - RNC:" + res.data[i].rnc)        
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
                    zoom: 12,
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
                    'Longitude: ' + coords.lng + ' Latitude: ' + coords.lat;
                canvas.style.cursor = '';

                this.geojsonLocationBin = coords.lng + "," + coords.lat;
                console.log(this.geojsonLocationBin)

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
                    zoom: 12,
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
                    'Longitude: ' + coords.lng + ' Latitude: ' + coords.lat;
                canvas.style.cursor = '';

                this.geojsonLocationCompa = coords.lng + "," + coords.lat;
                console.log(this.geojsonLocationCompa)

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
        this.loadAvailableCompanies();
        this.create_map_point_dragdable_bin();
        this.create_map_point_dragdable_compa();
       
        

        

        
                        
    }
}
</script>

<style>

</style>
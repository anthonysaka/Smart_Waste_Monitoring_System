<template>
  <div class="routing">
      
    <b-container fluid>
      <b-jumbotron class="jumbotron pt-2">
          <h4 class="h4 text-gray-800 py-2"><strong> GENERACION DE RUTAS </strong></h4>
          <b-row>
              <b-col cols="7">
                <div class="card ">
                    <div class="card-body">
                        <div ref="mapContainer" id="map" style="height: 80vh; width: 100%;"></div>
                    </div>
                </div>
              </b-col>

              <b-col cols="5">
                   <b-tabs content-class="mt-3" justified>
                    <b-tab title="Basureros">
                        <div class="card ">
                            <div class="card-header">
                                <h5 class="h5 text-gray-800"><strong>Lista Basureros </strong></h5>
                            </div>   
                            <div class="card-body py-0 px-0">
                                <b-table responsive="md sm" borderless sticky-header striped hover :items="items" :fields="fields" head-variant="light" selectable select-mode="multi" @row-selected="onRowSelectedBin">

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
                        <b-button @click="getDirectionsSmartRoutes" variant="primary">Primary</b-button>
                    </b-tab>

                     <b-tab title="Camiones">
                         <div class="card ">
                            <div class="card-header">
                                <h5 class="h5 text-gray-800"><strong>Lista Basureros </strong></h5>
                            </div>   
                            <div class="card-body py-0 px-0">
                                <b-table responsive="md sm" borderless sticky-header striped hover :items="itemsTruck" :fields="fieldsTruck" head-variant="light" selectable
                                    select-mode="multi" @row-selected="onRowSelectedTruck">

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
                    </b-tab>

                   </b-tabs>
                  
              </b-col>
          </b-row>

      </b-jumbotron>

       <b-jumbotron class="jumbotron pt-4">
           <h4 class="h4 text-gray-800 py-2"><strong> INFORMACION </strong></h4>
           <div class="card ">
                <div class="card-header">
                    <h5 class="h5 text-gray-800"><strong>Lista Rutas</strong></h5>
                </div>   
                <div class="card-body">
                </div>
            </div>

       </b-jumbotron>

    </b-container>

  </div>
</template>

<script>
import axios from 'axios';
const mapboxgl = require ('mapbox-gl')
const mapboxMatrixClient = require('@mapbox/mapbox-sdk/services/matrix');
const mpbxMatrixClient = mapboxMatrixClient({accessToken:'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw'});
const mapboxDirectionClient = require('@mapbox/mapbox-sdk/services/directions');
const mpbxDirectionClient = mapboxDirectionClient({accessToken:'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw'});

const API_URL = process.env.API_URL;
mapboxgl.accessToken = 'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw'


export default {
    data(){
        return{
            userlogged: JSON.parse(localStorage.getItem('userdata')),
            accessToken: 'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw',
            geoJson: null,

            fields: [
                {
                    key: 'selected',
                    label: '[*]',
                    sortable: true
                }, 
                {
                    key: 'name',
                    label: 'NOMBRE',
                    sortable: true
                },
                {
                    key: 'level',
                    label: '%',
                    sortable: true,
                },
                {
                    key: 'volumen',
                    label: 'VOL.',
                    sortable: true,
                },
                {
                    key: 'location',
                    label: 'UBICACION',
                    sortable: true,
                },



            ],
            items: [ ],
            selectedTable: null,

            fieldsTruck: [
                {
                    key: 'selected',
                    label: '[*]',
                    sortable: true
                }, 
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
                    key: 'capVol',
                    label: 'CAPACIDAD VOLUMENTRICA',
                    sortable: true,
                },
            ],
            itemsTruck:[],
            selectedTableTruck: null,

            coordinatesToRoutes: [],
            coordinatesInitPoint:'',
            cantTruck: 0,
            capacitiesTruck: [],
            distanceMatrix: [],
            
            map: null,
        }
    },
    methods:{
        async getNecessaryTruck(){
            var volumenOnDemand = 0;
            var camionesregistrados = [];
            var listnecessaryTrucks = [];
            var auxSumTruckCapacity = 0;

            for (let i = 0; i < this.selectedTableBin.length; i++) {
                volumenOnDemand += this.selectedTableBin[i].volumen;   
            }

            camionesregistrados = await this.loadAvailableTrucks();
            
            for (let i = 0; i < camionesregistrados.length; i++) {
                if ((auxSumTruckCapacity + camionesregistrados[i].cap_carga_vol) >= volumenOnDemand) {
                    listnecessaryTrucks.push(camionesregistrados[i])
                    break;
                } else {
                    listnecessaryTrucks.push(camionesregistrados[i]);
                    auxSumTruckCapacity += camionesregistrados[i].cap_carga_vol;
                }     
            }

            return listnecessaryTrucks;

        },
        getArrayVolumenOnDemand_modeManual(){
            var volumenOnDemand = [0]

            for (let i = 0; i < this.selectedTableBin.length; i++) {
                volumenOnDemand.push(this.selectedTableBin[i].volumen);   
            }
            
            return volumenOnDemand;

        },
        async getMapboxDistanceMatrix(){ //poner mode
            var res1 = await axios.get(`${API_URL}/clientCompany/1`,{
                params: {
                rncComp: this.userlogged.rnc_compa
                }
            });
            var i = res1.data[0].coordinates.split(",")
            var auxPoints = [{coordinates:[parseFloat(i[1]),parseFloat(i[0])]}];

           // if (mode == 1) { //mode manual: el operador seleccionar los basurero que desea recolectar
                for (let i = 0; i < this.selectedTableBin.length; i++) {
                   auxPoints.push({coordinates:[parseFloat(this.selectedTableBin[i].location.split(",")[0]),parseFloat(this.selectedTableBin[i].location.split(",")[1])]})
                }
                console.log(auxPoints)
           // } 
            //else { //modo auto: se buscan los basurero cuyo nivel de llenado sea mayor a 80%
                
            //}
        
            try {
                var r = await mpbxMatrixClient.getMatrix({
                points: auxPoints,
                profile: 'driving',
                annotations: ['distance']
            })
                .send()
            return r.body
            } catch (error) {
                console.log(error)
                
            }
             
        },
        async getSmartRoutes(){  //Capacited Vehicles Routing Problem (CVRP) call OR TOOL on server
            try {
                var aux = await this.getMapboxDistanceMatrix();
                var matrix =  aux;
                var listvoldemand = JSON.stringify(this.getArrayVolumenOnDemand_modeManual());
                var listruck = await this.getNecessaryTruck()
                var cant_Truck = listruck.length
                var listtruckcapacity = []

                for (let i = 0; i < listruck.length; i++) {
                    listtruckcapacity.push(listruck[i].cap_carga_vol)    
                }
                var res = null;
                res = await axios.get(`${API_URL}/smartroutes`, {
                    params: {
                        distanceMatrix: matrix,
                        volDemands: listvoldemand,
                        truckCapacities: JSON.stringify(listtruckcapacity),
                        cantTruck: cant_Truck,
                    }
                });

               // Despues obtener la respuesta del servidor
                var auxRoutesByTruck = res.data.solution.rutas.split(";")
                var smart_routes_solution = {rutas:[],totalDistance:res.data.solution.total_distance,totalVolumen:res.data.solution.total_volumen}
                var x = 0
                for (x = 0; x < auxRoutesByTruck.length; x++) {
                   smart_routes_solution.rutas.push(auxRoutesByTruck[x].split(":")) 
                }
                               
               
                var res1 = await axios.get(`${API_URL}/clientCompany/1`,{
                    params: {
                    rncComp: this.userlogged.rnc_compa }
                    });

                var i = res1.data[0].coordinates.split(",")
                var aux_Points = [{coordinates:[parseFloat(i[1]),parseFloat(i[0])]}];
                
                for (let i = 0; i < this.selectedTableBin.length; i++) {
                    aux_Points.push({coordinates:[parseFloat(this.selectedTableBin[i].location.split(",")[0]),parseFloat(this.selectedTableBin[i].location.split(",")[1])]})
                }
                console.log(aux_Points)
                         
                var y = 0;
                var j = 1;
                for (y = 0; y < smart_routes_solution.rutas.length-1; y++) {
                    for ( j = 1; j < smart_routes_solution.rutas[y].length-2; j++) {  
                        if(j == smart_routes_solution.rutas[y].length-3){
                            smart_routes_solution.rutas[y][j] = aux_Points[0].coordinates[0]+","+aux_Points[0].coordinates[1]
                        } else {
                            smart_routes_solution.rutas[y][j] = aux_Points[parseInt(smart_routes_solution.rutas[y][j])].coordinates[0]+","+aux_Points[parseInt(smart_routes_solution.rutas[y][j])].coordinates[1]
                        }
                        
                    }  
                }
                console.log(smart_routes_solution)
                return smart_routes_solution;    
            } catch (error) {
                console.log(error)
            }
        
        },
        async getDirectionsSmartRoutes(){
            this.removeRoute();

            var listCoordRoutes = await this.getSmartRoutes();
            var auxCoordRoutes = []
            var i = 0;
            var j = 1;
            console.log(listCoordRoutes)

            for (i = 0; i < listCoordRoutes.rutas.length - 1 ; i++) {
                auxCoordRoutes.push([])
                for (j = 1; j < listCoordRoutes.rutas[i].length-2; j++){
                    auxCoordRoutes[i].push({coordinates:[parseFloat(listCoordRoutes.rutas[i][j].split(",")[0]),parseFloat(listCoordRoutes.rutas[i][j].split(",")[1])],approach:'curb'})
                } 
            }
            console.log(auxCoordRoutes)

            try {
                //console.log(response)
                var routeid = 0;
                for (let x = 0; x < auxCoordRoutes.length; x++) {

                    var response = await mpbxDirectionClient.getDirections({
                        profile:'driving',
                        waypoints: auxCoordRoutes[x],
                        //steps: true,
                        geometries: "geojson",
                    }).send()
                    
                    this.drawSmartRoutes(response.body.routes[0].geometry,('R'+routeid))  
                    routeid++;  
                    
                }
                
                
            } catch (error) {
                console.log(error)
            }
            
        },
        async drawSmartRoutes(coords,name){
            function getRandomColor() {
                var letters = '0123456789ABCDEF';
                var color = '#';
                for (var i = 0; i < 6; i++) {
                    color += letters[Math.floor(Math.random() * 16)];
                }
                return color;
            }

            console.log(name)
            
            // check if the route is already loaded
            /* if (this.map.getSource('route')) {
                this.map.removeLayer('route')
                this.map.removeSource('route')
            } else{ */
                this.map.addLayer({
                "id": name,
                "type": "line",
                "source": {
                    "type": "geojson",
                    "data": {
                    "type": "Feature",
                    "properties": {},
                    "geometry": coords
                    }
                },
                "layout": {
                    "line-join": "round",
                    "line-cap": "round"
                },
                "paint": {
                    "line-color": getRandomColor(),
                    "line-width": 8,
                    "line-opacity": 0.8
                }
                });
            //};
        },
        removeRoute(){
            if (this.map.getSource('route')) {
                this.map.removeLayer('route');
                this.map.removeSource('route');
                
            } else  {
                return;
            }
        },
        async loadAvailableBinsOnMap(map) {
            try {
                var res = null;
                res = await axios.get(`${API_URL}/dustbin/1`, {
                    params: {
                    rncComp: this.userlogged.rnc_compa
                    }
                });
                var res1 = await axios.get(`${API_URL}/clientCompany/1`,{
                    params: {
                    rncComp: this.userlogged.rnc_compa
                    }
                });

                var auxFeatures = [];

                var auxCoor = res1.data[0].coordinates.split(",")
                auxFeatures.push({
                type: 'Feature',
                geometry: {
                    type: 'Point',
                    coordinates: [auxCoor[1], auxCoor[0]]
                },
                properties: {
                    title: res1.data[0].name,
                    description: 'Localidad de la empresa'
                }
                })

                for (var i = 0; i < res.data.length; i++) {
                    let auxCoor1 = res.data[i].coordinates.split(",")
                    auxFeatures.push({
                    type: 'Feature',
                    geometry: {
                        type: 'Point',
                        coordinates: [auxCoor1[0], auxCoor1[1]]
                    },
                    properties: {
                        title: res.data[i].name,
                        description: res.data[i].description
                    }
                    })
                }

                this.geoJson = {
                    type: 'FeatureCollection',
                    features: auxFeatures,
                }


                if (res != null) {
                    // add markers to map
                    var i = 0;
                this.geoJson.features.forEach(function (marker) {
                    
                    // create a HTML element for each feature
                    var el = document.createElement('div');
                    if(i == 0){
                        el.className = 'marker1';
                    } else{
                        el.className = 'marker';
                    }
                    i++;
                    // make a marker for each feature and add to the map
                    new mapboxgl.Marker(el)
                    .setLngLat(marker.geometry.coordinates)
                    .setPopup(new mapboxgl.Popup({
                        offset: 25
                        }) // add popups
                        .setHTML('<h5>' + marker.properties.title + '</h5><strong>' + marker.properties.description + '</strong>'))
                    .addTo(map);
                });        
            }
            } catch (error) {
                console.log(error)
                //this.initmap()
            }
        },
        async loadAvailableBins(){
            try {
                console.log(this.userlogged.rnc_compa)
                var res = await axios.get(`${API_URL}/dustbin/1`,{ params: {rncComp: this.userlogged.rnc_compa}});
               
                for (var i = 0; i < res.data.length; i++) { 
                    var res1 = await axios.get(`${API_URL}/bindata/0`,{ params: {namebin: res.data[i].name }});    
                    if(res.data[i].type == 'Tradicional - 1 contenedor'){
                        let row = {name:res.data[i].name,level:res1.data.data_sensor.lvlsingle,volumen:res1.data.data_sensor.volumen,location:res.data[i].coordinates}
                        this.items.push(row);
                    }else{
                        //falta agregar el volumen, pensar como hacerlo.
                        let lvl = ((res1.data.data_sensor.lvlPlastic + res1.data.data_sensor.lvlPaper + res1.data.data_sensor.lvlMedal)/3);
                        let row = {name:res.data[i].name,level:lvl,location:res.data[i].coordinates}
                        this.items.push(row);
                    }
                    
                   
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
        },
        async loadAvailableTrucks(){
            try {
                var res = await axios.get(`${API_URL}/truck`,{ params: {rncComp: this.userlogged.rnc_compa}});

               /* for (var i = 0; i < res.data.length; i++) {      
                    let row = {code:res.data[i].code,placa:res.data[i].placa,capVol:res.data[i].cap_carga_vol}
                    this.itemsTruck.push(row);
                }*/
                console.log(res.status)
                return res.data;
            } catch (error) {
                console.log(error)
            }
            
        },
        onRowSelectedBin(items) {
            this.selectedTableBin = items;
            console.log(this.selectedTableBin);
        },
        onRowSelectedTruck(items) {
            this.selectedTableTruck = items;
        },
        initmap(){
            const mapContainer = this.$refs.mapContainer;
            var m = this.map = new mapboxgl.Map({
                                                    container: mapContainer,
                                                    style: "mapbox://styles/mapbox/streets-v11",
                                                    center: [-70.703692, 19.415888],
                                                    zoom: 12,
                                                });
            this.loadAvailableBinsOnMap(m);
        }
    },
    mounted(){     
        
        this.initmap();
        
        this.loadAvailableBins();
        this.loadAvailableTrucks();

      //  this.prueba();
        
        //this.getMapboxDistanceMatrix();
    } 
}
</script>

<style>

</style>
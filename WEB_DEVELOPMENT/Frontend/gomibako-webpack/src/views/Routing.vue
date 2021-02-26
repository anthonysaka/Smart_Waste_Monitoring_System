<template>
  <div class="routing">
      
    <b-container fluid>
      <b-jumbotron class="jumbotron pt-2">
          <h4 class="h4 text-gray-800 py-2"><strong> GENERACION DE RUTAS </strong></h4>
          <b-row>
              <b-col cols="6">
                <div class="card ">
                    <div class="card-body">
                        <div ref="mapContainer" id="map" style="height: 80vh; width: 100%;"></div>
                    </div>
                </div>
              </b-col>

              <b-col cols="6" class="mr-n4">
                        <div class="card ml-n2 mr-n4">
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
                        <b-button class="mt-4" @click="getDirectionsSmartRoutes(1)" variant="primary">Modo Manual</b-button>
                        <b-button class="mt-4" @click="getDirectionsSmartRoutes(0)" variant="primary">Modo Auto</b-button>
                
                  
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
import Swal from 'sweetalert2';
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
                    key: 'mWaste',
                    label: 'MATERIAL',
                    sortable: true,
                },
                {
                    key: 'location',
                    label: 'UBICACION',
                    sortable: true,
                },
            ],
            items: [ ],
            selectedTableBin: null,

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
            routeid: 0,
            auxrouteid:0,
        }
    },
    methods:{
        async getNecessaryTruck(listVolumen){
            var volumenDemand = 0;
            var camionesregistrados = [];
            var listnecessaryTrucks = [];
            var auxSumTruckCapacity = 0;

            for (let x = 0; x < listVolumen.length; x++) {
                volumenDemand += listVolumen[x];
                
            }
            console.log(volumenDemand)

            camionesregistrados = await this.loadAvailableTrucks();
            
            for (let i = 0; i < camionesregistrados.length; i++) {
                
                if ((auxSumTruckCapacity + camionesregistrados[i].cap_carga_vol) >= volumenDemand) {
                    listnecessaryTrucks.push(camionesregistrados[i])
                    return listnecessaryTrucks;
                } else {
                    listnecessaryTrucks.push(camionesregistrados[i]);
                    auxSumTruckCapacity += camionesregistrados[i].cap_carga_vol;
                }     
            }

            Swal.fire(
                    'No cuenta con suficiente capacidad volumentrica en los camiones registrado para sastifacer la demanda de recogida actual. Por favor registre mas camiones o utilice le modo manual!',
                    '',
                    'error'
                )
            return null;   
        },
        getArrayVolumenOnDemand(mode){
            var volumenOnDemand = [0]

            if (mode == 1) {
                for (let i = 0; i < this.selectedTableBin.length; i++) {
                    volumenOnDemand.push(parseFloat(this.selectedTableBin[i].volumen));   
                }
            } else {
                
                for (let i = 0; i < this.items.length; i++) {
                    if(this.items[i].mWaste == "plastico/metal/papel-carton"){
                        console.log("entre volumen")
                        let aux = this.items[i].level.split("-")
                        if(parseInt(aux[0])>= 80) {
                            volumenOnDemand.push(parseFloat(this.items[i].volumen));
                        } else if (parseInt(aux[1]) >= 80) {
                            volumenOnDemand.push(parseFloat(this.items[i].volumen));
                        } else if (parseInt(aux[2]) >= 80){
                            volumenOnDemand.push(parseFloat(this.items[i].volumen));
                        }
                    } else {
                        if(this.items[i].level >= 80) {
                            volumenOnDemand.push(parseFloat(this.items[i].volumen));     
                        }
                            
                    }
                    
                }

                if (volumenOnDemand.length <= 1) {
                    Swal.fire(
                        'No hay basureros con mas del 80% de llenado!',
                        '',
                        'error'
                    )
                    return null;
                    
                }
            }   
            
            console.log(volumenOnDemand)
            
            return volumenOnDemand;
        },
        async getMapboxDistanceMatrix(mode){ //poner mode
            var res1 = await axios.get(`${API_URL}/clientCompany/1`,{
                params: {
                rncComp: this.userlogged.rnc_compa
                }
            });
            var i = res1.data[0].coordinates.split(",")
            var auxPoints = [{coordinates:[parseFloat(i[1]),parseFloat(i[0])]}];

            if (mode == 1) { //mode manual: el operador seleccionar los basurero que desea recolectar
                for (let i = 0; i < this.selectedTableBin.length; i++) {
                   auxPoints.push({coordinates:[parseFloat(this.selectedTableBin[i].location.split(",")[0]),parseFloat(this.selectedTableBin[i].location.split(",")[1])]})
                }
                console.log(auxPoints)
            } 
            else { //modo auto: se buscan los basurero cuyo nivel de llenado sea mayor a 80%
                var res = await axios.get(`${API_URL}/dustbin/1`,{ params: {rncComp: this.userlogged.rnc_compa}});
                
                for (let i = 0; i < res.data.length; i++) {
                    if(res.data[i].status == 1 || res.data[i].status == 2) { // SI esta full o Overload, considerarlo para la ruta
                       auxPoints.push({coordinates:[parseFloat(res.data[i].coordinates.split(",")[0]),parseFloat(res.data[i].coordinates.split(",")[1])]})
                    }
                    
                }
                console.log(auxPoints)
            }
        
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
        async getSmartRoutes(mode){  //Capacited Vehicles Routing Problem (CVRP) call OR TOOL on server
            try {
                console.log(mode)
                var listvoldemand = this.getArrayVolumenOnDemand(mode);
                if (listvoldemand == null) {
                    return null;
                }
                var listruck = await this.getNecessaryTruck(listvoldemand);
                if (listruck == null) {
                    return null;
                }
                var cant_Truck = listruck.length
                var listtruckcapacity = []

                var aux = await this.getMapboxDistanceMatrix(mode);
                var matrix =  aux;

                for (let i = 0; i < listruck.length; i++) {
                    listtruckcapacity.push(listruck[i].cap_carga_vol)    
                }
                console.log(matrix)
                console.log(listvoldemand)
                console.log(listtruckcapacity)
                console.log(cant_Truck)
                var res = null;

                await Swal.fire({
                    title: 'Presione para generar las rutas!',
                    showLoaderOnConfirm: true,
                    preConfirm: async (login) => {
                        Swal.update({
                            text:'Generando rutas...',
                        })
                        Swal.showLoading();
                        try {
                            res = await axios.get(`${API_URL}/smartroutes`, {
                                params: {
                                    distanceMatrix: matrix,
                                    volDemands: JSON.stringify(listvoldemand),
                                    truckCapacities: JSON.stringify(listtruckcapacity),
                                    cantTruck: cant_Truck,
                                }
                             })
                            
                        } catch (error) {
                            Swal.showValidationMessage(
                            `Request failed: ${error}`
                            )
                        }
                    },
                    allowOutsideClick: () => !Swal.isLoading()
                    })

                if (res.data.solution != null) {
                    Swal.fire(
                                'Rutas creadas con exito!',
                                '',
                                'success'
                            )
                } else {
                    Swal.fire(
                                'El sistema no puede encontrar una solucion!',
                                '',
                                'error'
                            )
                    
                }

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
                
                if (mode == 1) { //mode manual: el operador seleccionar los basurero que desea recolectar
                    for (let i = 0; i < this.selectedTableBin.length; i++) {
                    aux_Points.push({coordinates:[parseFloat(this.selectedTableBin[i].location.split(",")[0]),parseFloat(this.selectedTableBin[i].location.split(",")[1])]})
                    }
                    console.log(aux_Points)
                    } 
                else { //modo auto: se buscan los basurero cuyo nivel de llenado sea mayor a 80%
                    var res = await axios.get(`${API_URL}/dustbin/1`,{ params: {rncComp: this.userlogged.rnc_compa}});
                    
                    for (let i = 0; i < res.data.length; i++) {
                        if(res.data[i].status == 1 || res.data[i].status == 2) { // SI esta full o Overload, considerarlo par ala ruta
                        aux_Points.push({coordinates:[parseFloat(res.data[i].coordinates.split(",")[0]),parseFloat(res.data[i].coordinates.split(",")[1])]})
                        }
                        
                    }
                    console.log(aux_Points)
                }
                         
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
        async getDirectionsSmartRoutes(mode){
            
            if(mode == 1 && this.selectedTableBin == null){
                Swal.fire(
                    'Seleccione uno o mas basureros!',
                    '',
                    'error'
                )
            }
            else {
                this.removeRoute();
                var listCoordRoutes = await this.getSmartRoutes(mode);
                var auxCoordRoutes = []
                var i = 0;
                var j = 1;
                console.log(listCoordRoutes)

                if (listCoordRoutes != null) {

                    for (i = 0; i < listCoordRoutes.rutas.length - 1 ; i++) {
                        auxCoordRoutes.push([])
                        for (j = 1; j < listCoordRoutes.rutas[i].length-2; j++){
                            auxCoordRoutes[i].push({coordinates:[parseFloat(listCoordRoutes.rutas[i][j].split(",")[0]),parseFloat(listCoordRoutes.rutas[i][j].split(",")[1])],approach:'curb'})
                        } 
                    }
                    console.log(auxCoordRoutes)

                    try {
                        //console.log(response)
                        for (let x = 0; x < auxCoordRoutes.length; x++) {

                            var response = await mpbxDirectionClient.getDirections({
                                profile:'driving',
                                waypoints: auxCoordRoutes[x],
                                //steps: true,
                                geometries: "geojson",
                            }).send()
                            
                            this.drawSmartRoutes(response.body.routes[0].geometry,(this.routeid))  
                            this.routeid++;  
                            
                        }

                    } catch (error) {
                        console.log(error)
                    } 
                }  
            }      
        },
        async drawSmartRoutes(coords,name){
            function getRandomColor() {
                var letters = '0123456789ABCDEF';
                var color = '#'+name;
                for (var i = 0; i < 5; i++) {
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
                    id: "R"+name,
                    type: "line",
                    source: {
                        type: "geojson",
                        data: {
                            type: "Feature",
                            properties: {},
                            geometry: coords
                        }
                    },
                    layout: {
                        "line-join": "round",
                        "line-cap": "round",
                    },
                    paint: {
                        "line-color": getRandomColor(),
                        "line-width": 5,
                        "line-opacity": 0.8
                    }
                },'waterway-label');

                this.map.addLayer({
                    id: "S"+name+1,
                    type: "symbol",
                    source: {
                        "type": "geojson",
                        "data": {
                            "type": "Feature",
                            "properties": {},
                            "geometry": coords
                        }
                    },
                    layout: {
                        'symbol-placement': 'line',
                        'text-field': '▶',
                        'text-size': [
                            "interpolate",
                            ["linear"],
                            ["zoom"],
                            12, 24,
                            22, 60
                        ],
                        'symbol-spacing': [
                            "interpolate",
                            ["linear"],
                            ["zoom"],
                            12, 30,
                            22, 160
                        ],
                        'text-keep-upright': false
                    },
                    paint: {
                        "text-color": '#3887be',
                        "text-halo-color": 'hsl(55, 11%, 96%)',
                        "text-halo-width": 3
                    }
                },'waterway-label');
        },
        removeRoute(){
            if(this.routeid > 0){
                console.log("entre")
                for (let x = this.auxrouteid; x < this.routeid; x++) {
                    this.map.removeLayer("R"+x);
                    this.map.removeLayer("S"+x+1);
                    this.auxrouteid++;
                }
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
                        let row = {name:res.data[i].name,level:res1.data.data_sensor.lvlsingle,volumen:res1.data.data_sensor.volumen,mWaste:res.data[i].material_waste,location:res.data[i].coordinates}
                        this.items.push(row);
                    }else{      
            
                        let lvl = (String(res1.data.data_sensor.lvlPlastic) + "-" + String(res1.data.data_sensor.lvlMedal) + "-" + String(res1.data.data_sensor.lvlPaper));
                        let row = {name:res.data[i].name,level:lvl,volumen:res1.data.data_sensor.volumen,mWaste:res.data[i].material_waste,location:res.data[i].coordinates}
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

               for (var i = 0; i < res.data.length; i++) {      
                    let row = {code:res.data[i].code,placa:res.data[i].placa,capVol:res.data[i].cap_carga_vol}
                    this.itemsTruck.push(row);
                }
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
        this.$emit('childToParent', this.userlogged)
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
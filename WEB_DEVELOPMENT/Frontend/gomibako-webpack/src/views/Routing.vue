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

                        <div class="d-flex justify-content-around">
                            <b-button class="mt-4" @click="getDirectionsSmartRoutes(1)" variant="primary">Modo Manual</b-button>
                            <b-button class="mt-4" @click="getDirectionsSmartRoutes(0)" variant="primary">Modo Auto</b-button>
                            <b-button class="mt-4" @click="saveRoutes()" variant="primary" v-if="flagSave">Guardar</b-button>
                        </div>
                     
                      
                
                  
              </b-col>
          </b-row>

      </b-jumbotron>

       <b-jumbotron class="jumbotron pt-4">
           <div class="card mb-4">
                <div class="card-body">
                <h5 class="h5 text-gray-800 my-0"><strong> LISTADO DE RUTAS SIN ASIGNAR </strong></h5>
                </div>
            </div>

            <b-container style="display: flex;justify-content: center;">
                <b-input-group size="md" class="mb-4 w-50">
                <b-form-input v-model="filter" type="search" id="filterInput" placeholder="Escribe para buscar"></b-form-input>
                </b-input-group>
            </b-container>
         

            <b-col cols="12">
                <div class="card ">  
                    <div class="card-body">
                        <b-table responsive="sm" borderless hover :items="itemsR" :fields="fieldsR" head-variant="light" selectable
                        select-mode="single" @row-selected="onRowSelectedRoute" :filter="filter"
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

                        <template #cell(routeInfo)="row">
                            <b-button size="sm" @click="info(row.item, row.index, $event.target)" class="mr-1">Info Ruta</b-button>
                        </template>

                        <template #cell(asignar)="row">
                            <b-button size="sm" @click="asignar(row.item, row.index, $event.target)" class="mr-1">Asignar</b-button>
                        </template>

                    </b-table>

                    <!-- Info modal -->
                        <b-modal :id="infoModal.id" :title="infoModal.title" ok-only size="lg" @hide="resetInfoModal">
                            <h3 style="color: black;"><strong> Detalles de Ruta </strong></h3>

                            <h5 style="color: black;"><strong>[-] Listado de basureros:</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.bins}}</p>

                            <h5 style="color: black;"><strong>[-] Listado de coordenadas:</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.coords}}</p>

                            <h5 style="color: black;"><strong>[-] Camion correspondiente:</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.truck}}</p>

                            <h5 style="color: black;"><strong>[-] Total distancia (metros):</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.total_dist}}</p>

                            <h5 style="color: black;"><strong>[-] Total volumen (pies^3):</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.total_volumen}}</p>
                            
                        </b-modal>

                        <!-- Asignar modal -->
                        <b-modal :id="asignarModal.id" :title="asignarModal.title" ok-only size="lg" @hide="resetAsignarModal">
                            <h3 style="color: black;"><strong> Asignacion de Ruta </strong></h3>
                            <hr>

                            <h4 style="color: black;"><strong> Detalles de Ruta </strong></h4>

                            <h5 style="color: black;"><strong>[-] ID:</strong></h5>
                            <p style="color: black;">{{this.asignarModal.idRoute}}</p>

                            <h5 style="color: black;"><strong>[-] Listado de basureros:</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.bins}}</p>

                            <h5 style="color: black;"><strong>[-] Listado de coordenadas:</strong></h5>
                            <p style="color: black;">{{this.asignarModal.content.coords}}</p>

                            <h5 style="color: black;"><strong>[-] Camion correspondiente:</strong></h5>
                            <p style="color: black;">{{this.asignarModal.content.truck}}</p>

                            <h5 style="color: black;"><strong>[-] Total distancia (metros):</strong></h5>
                            <p style="color: black;">{{this.asignarModal.content.total_dist}}</p>

                            <h5 style="color: black;"><strong>[-] Total volumen (pies^3):</strong></h5>
                            <p style="color: black;">{{this.asignarModal.content.total_volumen}}</p>

                            <h5 style="color: black;"><strong>[-] Elegir chofer: </strong></h5>
                            <div class="d-flex justify-content- mb-4">
                                <b-form-select searchable="Search here.." v-model="selected" :options="listDriver" class="mb- mr-4"
                                        value-field="item" text-field="name" disabled-field="notEnabled"></b-form-select>
                            </div> 
                          

                             <b-button class="mt-4" @click="setRouteToDriver()" variant="primary">Asignar</b-button>

                            
                        </b-modal>
                    </div>
                </div>
            </b-col>

       </b-jumbotron>

        <b-jumbotron class="jumbotron pt-4">
           <div class="card mb-4">
                <div class="card-body">
                <h5 class="h5 text-gray-800 my-0"><strong> LISTADO DE RUTAS ASIGNADAS/COMPLETADAS </strong></h5>
                </div>
            </div>

            <b-container style="display: flex;justify-content: center;">
                <b-input-group size="md" class="mb-4 w-50">
                <b-form-input v-model="filterR" type="search" id="filterInput" placeholder="Escribe para buscar"></b-form-input>
                </b-input-group>
            </b-container>
         

            <b-col cols="12">
                <div class="card ">  
                    <div class="card-body">
                        <b-table responsive="sm" borderless hover :items="itemsRC" :fields="fieldsRC" head-variant="light" selectable
                            select-mode="single" :filter="filterR"
                            :filter-included-fields="filterOnR">

                            <template #cell(routeInfoC)="row">
                                <b-button size="sm" @click="info(row.item, row.index, $event.target)" class="mr-1">Info Ruta</b-button>
                            </template>
                        </b-table>

                    <!-- Info modal -->
                        <b-modal :id="infoModal.id+'C'" :title="infoModal.title" ok-only size="lg" @hide="resetInfoModal">
                            <h3 style="color: black;"><strong> Detalles de Ruta </strong></h3>

                            <h5 style="color: black;"><strong>[-] Listado de basureros:</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.bins}}</p>

                            <h5 style="color: black;"><strong>[-] Listado de coordenadas:</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.coords}}</p>

                            <h5 style="color: black;"><strong>[-] Camion correspondiente:</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.truck}}</p>

                            <h5 style="color: black;"><strong>[-] Total distancia (metros):</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.total_dist}}</p>

                            <h5 style="color: black;"><strong>[-] Total volumen (pies^3):</strong></h5>
                            <p style="color: black;">{{this.infoModal.content.total_volumen}}</p>
                            
                        </b-modal>
                    </div>
                </div>
            </b-col>

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
            userlogged: JSON.parse(sessionStorage.getItem('userdata')),
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
            selectedTableRoute: null,

            coordinatesToRoutes: [],
            coordinatesInitPoint:'',
            cantTruck: 0,
            capacitiesTruck: [],
            distanceMatrix: [],
            
            map: null,
            routeid: 0,
            auxrouteid:0,

            flagSave: false,

            auxSolutionRoutes: {},
            auxListTrucks: [],

            fieldsR: [
                {
                    key: 'id',
                    label: 'ID',
                    sortable: true
                },
                {
                    key: 'routeInfo',
                    label: 'DETALLES RUTA',
                },
                {
                    key: 'dateCreated',
                    label: 'FECHA CREADA',
                    sortable: true,
                },
                {
                    key: 'status',
                    label: 'STATUS',
                    sortable: true,
                },
                {
                    key: 'asignar',
                    label: 'ACCION',
                },
            ],
            itemsR: [ ],

            fieldsRC: [
                {
                    key: 'id',
                    label: 'ID',
                    sortable: true
                },
                {
                    key: 'routeInfoC',
                    label: 'DETALLES RUTA',
                },
                {
                    key: 'dateCreated',
                    label: 'FECHA CREADA',
                    sortable: true,
                },
                {
                    key: 'status',
                    label: 'STATUS',
                    sortable: true,
                },
                {
                    key: 'driver',
                    label: 'CHOFER',
                    sortable: true,
                },
                {
                    key: 'completed_date',
                    label: 'FECHA Compl.',
                    sortable: true,
                },
            ],
               
            itemsRC: [ ],

            infoModal: {
                id: 'info-modal',
                title: '',
                content: ''
            },
            asignarModal: {
                id: 'asignar-modal',
                title: '',
                content: '',
                idRoute:''
            },

            filter: null,
            filterOn:[],
            filterR: null,
            filterOnR:[],
            auxRouteInfo: [],
            listDriver: [],
            selected: null,
            idR: '',
            auxNameBins: [],
            auxlistNameBinSol: [],
            auxListCoordDraw:[]
        }
    },
    methods:{
        async loadDriver(){
            try {
                var res = await axios.get(`${API_URL}/driver`,{ params: {rncComp: this.userlogged.rnc_compa}});

                for (var i = 0; i < res.data.length; i++) {   
                    this.listDriver.push(res.data[i].id + '-' + res.data[i].username)   
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
           
        },
        async setRouteToDriver(){
            let idRoute = this.idR
            let user = this.selected.split('-')[1]
            try {
                var res = await axios.put(`${API_URL}/routes`,{ id: idRoute, username_driver: user, status: 'Asignada'});
                console.log(res.status)
            } catch (error) {
                 console.log(error)
            }


        },
        info(item, index, button) {
            console.log(this.auxRouteInfo[0])
            this.infoModal.title = `Row index: ${index}`
            this.infoModal.content = this.auxRouteInfo[index].info_route
            this.$root.$emit('bv::show::modal', this.infoModal.id, button)
        },
        resetInfoModal() {
            this.infoModal.title = ''
            this.infoModal.content = ''
        },
        asignar(item, index, button) {
            this.idR = this.auxRouteInfo[index].id
            this.asignarModal.title = `Row index: ${index}`
            this.asignarModal.idRoute = this.auxRouteInfo[index].id
            this.asignarModal.content = this.auxRouteInfo[index].info_route
            this.$root.$emit('bv::show::modal', this.asignarModal.id, button)
        },
        resetAsignarModal() {
            this.asignarModal.title = ''
            this.asignarModal.content = ''
            this.asignarModal.idRoute = ''
            this.idR = ''
        },
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
                    this.auxNameBins.push(this.selectedTableBin[i].name);
                }
            } else {
                
                for (let i = 0; i < this.items.length; i++) {
                    if(this.items[i].mWaste == "plastico/metal/papel-carton"){
                        let aux = this.items[i].level.split("-")
                        if(parseInt(aux[0])>= 80) {
                            volumenOnDemand.push(parseFloat(this.items[i].volumen));
                            this.auxNameBins.push(this.items[i].name);
                        } else if (parseInt(aux[1]) >= 80) {
                            volumenOnDemand.push(parseFloat(this.items[i].volumen));
                             this.auxNameBins.push(this.items[i].name);
                        } else if (parseInt(aux[2]) >= 80){
                            volumenOnDemand.push(parseFloat(this.items[i].volumen));
                             this.auxNameBins.push(this.items[i].name);
                        }
                    } else {
                        if(this.items[i].level >= 80) {
                            volumenOnDemand.push(parseFloat(this.items[i].volumen));    
                             this.auxNameBins.push(this.items[i].name); 
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
                this.auxListTrucks = listruck;
                console.log("TRUCKS")
                console.log(listruck)
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
                    return null;
                }

                // Despues obtener la respuesta del servidor
                var auxRoutesByTruck = res.data.solution.rutas.split(";")
                console.log("auxRoutesByTruck")
                console.log(auxRoutesByTruck)
                console.log(auxRoutesByTruck.length)

                
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
                var namesol = []
                var auxname = []
                var y = 0;
                var j = 1;
                for (y = 0; y < smart_routes_solution.rutas.length-1; y++) {
                    for ( j = 1; j < smart_routes_solution.rutas[y].length-2; j++) {
                        if(parseInt(smart_routes_solution.rutas[y][j]) != 0){
                            auxname.push(this.auxNameBins[parseInt(smart_routes_solution.rutas[y][j])-1])
                        }
                        if(j == smart_routes_solution.rutas[y].length-3){
                            smart_routes_solution.rutas[y][j] = aux_Points[0].coordinates[0]+","+aux_Points[0].coordinates[1]
                        } else {
                            smart_routes_solution.rutas[y][j] = aux_Points[parseInt(smart_routes_solution.rutas[y][j])].coordinates[0]+","+aux_Points[parseInt(smart_routes_solution.rutas[y][j])].coordinates[1]
                        }
                        
                    }  
                    namesol.push(auxname)
                    auxname = []
                }

                console.log("SOLUCION")
                console.log(smart_routes_solution)
                console.log(namesol)
                this.auxSolutionRoutes = smart_routes_solution;
                this.auxlistNameBinSol = namesol;
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
                    console.log('RUTAS')
                    console.log(auxCoordRoutes)

                    try {
                        //console.log(response)
                        this.auxListCoordDraw = []
                        for (let x = 0; x < auxCoordRoutes.length; x++) {

                            var response = await mpbxDirectionClient.getDirections({
                                profile:'driving',
                                waypoints: auxCoordRoutes[x],
                                //steps: true,
                                geometries: "geojson",
                            }).send()
                            
                            console.log('ESTAS SON LAS DIRECCIONES')
                            console.log(response.body)
                            let aux = []
                            for (let i = 0; i < response.body.routes[0].geometry.coordinates.length; i++) {
                               aux.push({longitude:response.body.routes[0].geometry.coordinates[i][0],latitude:response.body.routes[0].geometry.coordinates[i][1]})
                                
                            }
                            this.auxListCoordDraw.push(aux)
                            console.log(this.auxListCoordDraw)

                            
                            this.drawSmartRoutes(response.body.routes[0].geometry,(this.routeid))  
                            this.routeid++;  
                            
                        }

                        this.flagSave = true;

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
                     status:res.data[i].status,
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

                    if(marker.status == 1){
                        el.className = 'marker_full';
                    } else if (marker.status == 2){
                        el.className = 'marker_overload';
                    } else {
                        el.className = 'marker'
                    }
                    
                     if(i == 0){
                        el.className = 'marker1';
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
        async loadRoutesSinAsignarTable(){
             try {
                var res = await axios.get(`${API_URL}/routes`,{ params: {rncComp: this.userlogged.rnc_compa}});

               for (var i = 0; i < res.data.length; i++) {  
                   if (res.data[i].status == 'Sin Asignar'){
                        let row = {id:res.data[i].id,dateCreated:res.data[i].created_date,status:res.data[i].status}
                        this.itemsR.push(row);
                        this.auxRouteInfo.push(res.data[i])
                   }
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
        },
        async loadRoutesTable(){
             try {
                var res = await axios.get(`${API_URL}/routes`,{ params: {rncComp: this.userlogged.rnc_compa}});

               for (var i = 0; i < res.data.length; i++) {  
                   if (res.data[i].status != 'Sin Asignar'){
                        let row = {id:res.data[i].id,dateCreated:res.data[i].created_date,status:res.data[i].status,driver:res.data[i].driver_username,completed_date:res.data[i].completed_date}
                        this.itemsRC.push(row);
                        this.auxRouteInfo.push(res.data[i])
                   }
                }
                console.log(res.status)
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
        onRowSelectedRoute(items) {
            this.selectedTableRoute = items;
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
        },
        async saveRoutes(){
            var aux1 = []
            var aux = []
            console.log("SALVANDO PRUEBA")
            console.log(this.auxSolutionRoutes)
            for (let i = 0; i < this.auxSolutionRoutes.rutas.length-1; i++) {
                aux1 = [];
                for (let j = 1; j < this.auxSolutionRoutes.rutas[i].length-2; j++){
                       aux1.push(this.auxSolutionRoutes.rutas[i][j])
                }
          
                let body = {"route_info":{bins:this.auxlistNameBinSol[i],coords:aux1,total_dist:this.auxSolutionRoutes.rutas[i][this.auxSolutionRoutes.rutas[i].length-2],
                                            total_volumen:this.auxSolutionRoutes.rutas[i][this.auxSolutionRoutes.rutas[i].length-1],truck:this.auxListTrucks[i].placa,
                                            polylineDraw: this.auxListCoordDraw[i]},
                            "rncCompa":this.userlogged.rnc_compa,
                            "status": 'Sin Asignar',
                            }
                console.log(body)
                var res = await axios.post(`${API_URL}/routes`, body);
                console.log(res.status)
            }
        }
    },
    mounted(){     
        this.$emit('childToParent', this.userlogged)
        this.initmap();
        this.loadAvailableBins();
        this.loadAvailableTrucks();
        this.loadRoutesSinAsignarTable();
        this.loadRoutesTable();
        this.loadDriver();

      //  this.prueba();
        
        //this.getMapboxDistanceMatrix();
    } 
}
</script>

<style>

</style>
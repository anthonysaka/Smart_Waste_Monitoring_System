<template>
  <div class="Dashboard">
    <b-container fluid>

      <b-jumbotron class="jumbotron pt-2">
         <div class="card mb-4">
            <div class="card-body">
              <h5 class="h5 text-gray-800 my-0"><strong> GRAFICOS </strong></h5>
            </div>
         </div>
         <b-row>
          <b-container>
            <div class="d-flex justify-content- mb-4">
              <b-form-select searchable="Search here.." v-model="selected" :options="listAvailableBins" class="mb- mr-4"
                     value-field="item" text-field="name" disabled-field="notEnabled"></b-form-select>
               <b-button @click="updateValuesPeriodically" variant="primary">Ok!</b-button>
            </div>      
          </b-container>
        </b-row>
        
        
        <b-row>
          <b-col cols="12" md="5" >
            <div class="card mt-2">
              <div class="card-body">
                <div class="chart-area pt-4">
                  <lineChart :width="200" :height="250" v-if="loadedLine" :chart-data="datacollectionLine[0]">
                  </lineChart>
                </div>
              </div>
            </div>

            <div class="card mt-2">
              <div class="card-body">
                <div class="chart-area pt-4">
                  <lineChart :width="200" :height="250" v-if="loadedLine" :chart-data="datacollectionLine[1]">
                  </lineChart>
                </div>
              </div>
            </div>



          </b-col>

            <!-- LIVE DATA -->
          <b-col cols="12" md="7" style="margin-top:3.8%;">
            <div class="card w-200" >
              <div class="d-flex px-2 pb-4">
                <h5 class="h5 mr-auto ml-2 mt-2 mb-n1 text-gray-800" style="color: RGB(79, 79, 79) !important;">Codigo:&nbsp;<strong>{{titlebin}}</strong></h5>
                <hr>
                <h5 class="h5 mt-2 mb-n1 mr-2  text-gray-800" style="color: RGB(79, 79, 79) !important;">Fecha correspondiente a:&nbsp;<strong>{{updatetime}}</strong></h5>
                <hr>
              </div>

              <div class="d-flex flex-column mb-4" style="background-color:transparent !important;">
                <b-row style="background-color:transparent !important;">
                  <b-col cols="12" md="3">
                    <div class="minicard  h-10 py-1 ml-2 mr-2">
                      <div class="card-body" style="height: 10vh;">
                        <div class="d-flex flex-column">
                          <div class="text-xs font-weight-bold text-center mt-n3 text-primary text-uppercase mb-1">
                            <strong>Temperatura (°C)</strong></div>
                        </div>
                        <b-row>
                          <b-col cols="6">
                            <div class="d-flex flex-column text-center">
                              <i class="fas fa-temperature-high fa-2x"></i>
                            </div>
                          </b-col>
                          <b-col cols="6">
                            <div class="h5 mb-0 text-center mt-2 px-0 font-weight-bold text-gray-800">
                              <b-badge variant="primary">{{tempValue}}</b-badge>
                            </div>
                          </b-col>

                        </b-row>
                      </div>
                    </div>
                  </b-col>

                  <b-col cols="12" md="3">
                    <div class="minicard  h-10 py-1 ml-2 mr-2">
                      <div class="card-body" style="height: 10vh;">
                        <div class="d-flex flex-column">
                          <div class="text-xs font-weight-bold text-center mt-n3 text-primary text-uppercase mb-1">
                            <strong>Humedad (%)</strong></div>
                        </div>
                        <b-row>
                          <b-col cols="6">
                            <div class="d-flex flex-column text-center">
                              <i class="fas fa-tint fa-2x"></i>
                            </div>
                          </b-col>
                          <b-col cols="6">
                            <div class="h5 mb-0 text-center mt-2 font-weight-bold text-gray-800">
                              <b-badge variant="primary">{{humValue}}</b-badge>
                            </div>
                          </b-col>

                        </b-row>
                      </div>
                    </div>
                  </b-col>

                  <b-col cols="12" md="3">
                    <div class="minicard  h-10 py-1 ml-2 mr-2">
                      <div class="card-body" style="height: 10vh;">
                        <div class="d-flex flex-column">
                          <div class="text-xs font-weight-bold text-center mt-n3 text-primary text-uppercase mb-1">
                            Bateria (%)</div>
                        </div>
                        <b-row>
                          <b-col cols="6">
                            <div class="d-flex flex-column text-center">
                              <i class="fas fa-battery-three-quarters fa-2x"></i>
                            </div>
                          </b-col>
                          <b-col cols="6">
                            <div class="h5 mb-0 text-center mt-2 font-weight-bold text-gray-800">
                             <b-badge variant="primary">{{batteryValue}}</b-badge></div>
                          </b-col>

                        </b-row>
                      </div>
                    </div>
                  </b-col>

                  <b-col cols="12" md="3">
                    <div class="minicard  h-10 py-1 ml-2 mr-2">
                      <div class="card-body" style="height: 10vh;">
                        <div class="d-flex flex-column">
                          <div class="text-xs font-weight-bold text-center mt-n3 text-primary text-uppercase mb-1">
                            ESTADO</div>
                        </div>
                        <b-row>
                          <b-col cols="6">
                            <div class="d-flex flex-column text-center">
                              <i class="fas fa-2x fa-info-circle"></i>
                            </div>
                          </b-col>
                          <b-col cols="6">
                            <div class="h6 ml-n4 mb-0 text-center mt-2 font-weight-bold text-gray-800"> 
                              <b-badge variant="primary">{{binStatus}}</b-badge></div>
                          </b-col>

                        </b-row>
                      </div>
                    </div>
                  </b-col>
                </b-row>
              </div>

              <div class="d-flex flex-column mb-4">
                <b-row>
                  <b-col cols="12" md="4">
                    <div class="minicard  mb-2 mt-2 ml-2 mr-0"  v-if="show_three">
                      <!-- Card Header -->
                      <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold text-primary"><strong>Plastico:</strong>
                          <b-badge pill variant="primary">{{ levelplastic }} %</b-badge>
                        </h6>
                      </div>
                      <!-- Card Body -->
                      <div class="card-body">
                        <div class="chart-pie pt-4">
                          <levelChart :width="150" :height="150" v-if="loadedDonut" :chart-data="datacollectionDonut[0]">
                          </levelChart>
                        </div>
                      </div>
                    </div>
                  </b-col>

                  <b-col cols="12" md="4">
                    <div class="minicard  mb-2 mt-2 ml-0 mr-0" v-if="show_three">
                      <!-- Card Header -->
                      <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold text-primary"><strong>Metal:</strong>
                          <b-badge pill variant="primary">{{ levelmetal }} %</b-badge>
                        </h6>
                      </div>
                      <!-- Card Body -->
                      <div class="card-body">
                        <div class="chart-pie pt-4">
                          <levelChart :width="150" :height="150" v-if="loadedDonut" :chart-data="datacollectionDonut[1]">
                          </levelChart>
                        </div>
                      </div>
                    </div>

                    <div class="minicard  mb-2 mt-2 ml-0 mr-0" v-if="show_one">
                      <!-- Card Header -->
                      <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold text-primary"><strong>{{typeM}}:</strong>
                          <b-badge pill variant="primary">{{ levelSingle }} %</b-badge>
                        </h6>
                      </div>
                      <!-- Card Body -->
                      <div class="card-body">
                        <div class="chart-pie pt-4">
                          <levelChart :width="150" :height="150" v-if="loadedDonut" :chart-data="datacollectionDonut[3]">
                          </levelChart>
                        </div>
                      </div>
                    </div>
                  </b-col>

                  <b-col cols="12" md="4">
                    <div class="minicard  mb-2 mt-2 ml-0 mr-2"  v-if="show_three">
                      <!-- Card Header -->
                      <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold text-primary"><strong>Papel/Carton:</strong>
                          <b-badge pill variant="primary">{{ levelpaper}} %</b-badge>
                        </h6>
                      </div>
                      <!-- Card Body -->
                      <div class="card-body">
                        <div class="chart-pie pt-4">
                          <levelChart :width="150" :height="150" v-if="loadedDonut" :chart-data="datacollectionDonut[2]">
                          </levelChart>
                        </div>
                      </div>
                    </div>
                  </b-col>




                </b-row>
              </div>
            </div>
          </b-col>
        </b-row>

      </b-jumbotron>

<!-- SECOND SECTION -->
      <b-jumbotron class="jumbotron">
        <div class="card mb-4">
            <div class="card-body">
              <h5 class="h5 text-gray-800 my-0"><strong> LISTADO DE BASUREROS</strong></h5>
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
                  <b-table responsive="sm" borderless hover :items="items" :fields="fields" head-variant="light" selectable
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

      <!-- THIRD SECTION -->
      <b-jumbotron class="jumbotron">
        <div class="card mb-4">
          <b-row>
            <b-col cols="9" class="card-body">
              <h5 class="h5 ml-2 text-gray-800 my-0"><strong> DATOS BASUREROS</strong></h5>
            </b-col>
            <b-col cols="3">
                <h5 class="h5 mt-4 text-gray-800" style="color: RGB(79, 79, 79) !important;">Actualizado:&nbsp;<strong>{{timestamp}}</strong></h5>
            </b-col>

          </b-row>
         </div>
    
        
        <b-container style="display: flex;justify-content: center;">
            <b-input-group size="md" class="mb-4 w-50">
              <b-form-input v-model="filterD" type="search" id="filterInputD" placeholder="Escribe para buscar"></b-form-input>
            </b-input-group>
            <b-col cols="2">
               <b-button  @click="loadDataBinTable()" variant="primary">Actualizar Datos</b-button>
            </b-col>

        </b-container>
          

        <b-col cols="12">
          <div class="card">
              <div class="card-body">
                  <b-table id="tableDataBin" responsive="sm" borderless hover :items="itemsD" :fields="fieldsD" head-variant="light" selectable
                    select-mode="single" @row-selected="onRowSelected" :filter="filterD"
                    :filter-included-fields="filterOnD" :current-page="currentPage" :per-page="perPage">

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
              <b-pagination class="px-4 mx-4"
                v-model="currentPage"
                :total-rows="rows"
                :per-page="perPage"
                align="fill"
                size="sm"
                aria-controls="tableDataBin">
               
              </b-pagination>
          </div>
        </b-col>
      </b-jumbotron>


    </b-container>
  </div>

</template>

<script>
import levelChart from '../components/donutChart';
import lineChart from '../components/lineChart';
import axios from 'axios';
import mapboxgl from "mapbox-gl";
import Swal from 'sweetalert2';
const API_URL = process.env.API_URL;

import io from 'socket.io-client';
var socket = io.connect("http://localhost:5000");

export default {
    components:{
        levelChart,
        lineChart,
    },
    data (){
        return {
            perPage: 20,
            currentPage: 1,
            timestamp: null,
            userlogged: JSON.parse(sessionStorage.getItem('userdata')),
            datacollectionDonut: [],
            datacollectionLine: [],
            loadedDonut: false,
            loadedLine: false,
            tempValue: null,
            humValue: null,
            batteryValue: null,
            binStatus: null,
            levelplastic: null,
            levelmetal: null,
            levelpaper: null,
            levelSingle:null,
            selected: null,
            titlebin: null,
            updatetime:null,
            listAvailableBins: [{text: 'Please select an option'}],
            accessToken: 'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw',
            fields: [
                {
                    key: 'name',
                    label: 'NOMBRE',
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
                    key: 'description',
                    label: 'DESCRIPCION',
                    sortable: true,
                },
                {
                    key: 'date',
                    label: 'FECHA REGISTRO',
                    sortable: true,
                },

            ],
            items: [ ],
            fieldsD: [
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
                    key: 'temperature',
                    label: 'TEMP.',
                    sortable: true,
                },
                {
                  key: 'humidity',
                  label: 'HUM.',
                  sortable: true,
                },
                 {
                  key: 'nodedate',
                  label: 'FECHA Crec.',
                  sortable: true,
                },
                {
                  key: 'date',
                  label: 'FECHA Rec.',
                  sortable: true,
                },
                {
                    key: 'datatype',
                    label: 'DType.',
                    sortable: true,
                },

            ],
            itemsD: [ ],
            selectedTable: null,
            filter: null,
            filterOn:[],
            filterD: null,
            filterOnD:[],
            show_one: false,
            show_three: false,
            typeM: '',
            namebin: ''
        }
    },
    methods: {
        getNow(){
            const today = new Date();
            const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            const dateTime = date +' '+ time;
            this.timestamp = dateTime;
        },
        async getLastValues(){
            if(this.selected != null) {      
                var auxlvlPlast = 0;
                var auxlvlMetal = 0;
                var auxlvlPaper = 0;
                var auxlvlSingle = 0;

                try {           
                    this.titlebin = this.namebin.split(" ")[0]
                    var res = await axios.get(`${API_URL}/bindata/0`,{ params: {namebin: this.namebin.split(" ")[0]}});
                    var data = res.data;

                    
                        if (this.namebin.split(" - ")[1] == 'Tradicional'){
                          this.show_one = true;
                          this.show_three = false;
                          this.typeM = this.namebin.split(" - ")[3]
                          auxlvlSingle = data.data_sensor.lvlsingle;
                          this.levelSingle = data.data_sensor.lvlsingle;

                          if(data.data_sensor.codeStatus == 2){
                            this.binStatus = 'OVERLOAD'
                          }else if (data.data_sensor.codeStatus == 1){
                            this.binStatus = 'FULL'
                          }else{
                            this.binStatus = 'NORMAL'
                          }
                        } else { 
                          this.show_three = true;
                          this.show_one = false;
                          auxlvlPlast = data.data_sensor.lvlPlastic;
                          auxlvlMetal = data.data_sensor.lvlMedal;
                          auxlvlPaper = data.data_sensor.lvlPaper;
                          this.levelplastic = auxlvlPlast;
                          this.levelmetal = auxlvlMetal;
                          this.levelpaper = auxlvlPaper; 

                          if(data.data_sensor.codeStatusPlastic == 2 || data.data_sensor.codeStatusMetal == 2 || data.data_sensor.codeStatusPaper == 2){
                            this.binStatus = 'OVERLOAD'
                          }else if (data.data_sensor.codeStatus == 1 || data.data_sensor.codeStatusMetal == 1 || data.data_sensor.codeStatusPaper == 1){
                            this.binStatus = 'FULL'
                          }else{
                            this.binStatus = 'NORMAL'
                          }

                        }
                            this.datacollectionDonut = [{
                            labels: ['Nivel de llenado'],
                            
                            datasets: [{
                                label: 'Data One',
                                backgroundColor: ['#2e59d9', "#ffffff"],
                                hoverBackgroundColor: ['#2e59d9','#ffffff'],
                                borderColor:['#2e59d9', "#ffffff"],
                                hoverBorderColor: ["#070707","#070707"],
                                data: [auxlvlPlast, 100 - auxlvlPlast]
                        }],
                        },{
                            labels: ['Nivel de llenado'],
                            datasets: [{
                                label: 'Data One',
                                backgroundColor: ['#2e59d9', "#ffffff"],
                                hoverBackgroundColor: ['#2e59d9','#ffffff'],
                                borderColor:['#2e59d9', "#ffffff"],
                                hoverBorderColor: ["#070707","#070707"],
                                data: [auxlvlMetal, 100 - auxlvlMetal]
                        }],
                        },{
                            labels: ['Nivel de llenado'],
                            datasets: [{
                                label: 'Data One',
                                backgroundColor: ['#2e59d9', "#ffffff"],
                                hoverBackgroundColor: ['#2e59d9','#ffffff'],
                                borderColor:['#2e59d9', "#ffffff"],
                                hoverBorderColor: ["#070707","#070707"],
                                data: [auxlvlPaper, 100 - auxlvlPaper]
                        }],
                        },{
                            labels: ['Nivel de llenado'],
                            datasets: [{
                                label: 'Data One',
                                backgroundColor: ['#2e59d9', "#ffffff"],
                                hoverBackgroundColor: ['#2e59d9','#ffffff'],
                                borderColor:['#2e59d9', "#ffffff"],
                                hoverBorderColor: ["#070707","#070707"],
                                data: [auxlvlSingle, 100 - auxlvlSingle]
                        }],
                        }
                        ];
                        
                        this.updatetime = data.created_date;
                        this.tempValue = data.data_sensor.temperature;
                        this.humValue = data.data_sensor.humidity;
                        this.batteryValue = data.data_sensor.batteryLevel;
                        this.loadedDonut = true;

              } catch (error) {
                  console.error(error);
              }       

            }
            
        },
        async getBinGraphicValues(){
            if(this.selected != null) {
                try {           
                    var res = await axios.get(`${API_URL}/bindata/1`,{ params: {namebin: this.namebin.split(" ")[0] }});
                    var data = res.data;
                 
                    var labels = []

                    if (this.namebin.split(" - ")[1] == 'Tradicional') {
                      var datasetsSingle = {
                        label: this.namebin.split(" - ")[3],
                        data: [],
                        fill: true,
                        borderColor: '#2554FF',
                        backgroundColor: 'rgba(33, 76, 229, 0.5)',
                        borderWidth: 2
                      }
                      var datasetsSingleTem = {
                        label: 'Temperatura(C)',
                        data: [],
                        fill: true,
                        borderColor: '#2554FF',
                        backgroundColor: 'rgba(33, 76, 229, 0.5)',
                        borderWidth: 2
                      }
                      var datasetsSingleHum = {
                        label: 'Humedad(%)',
                        data: [],
                        fill: true,
                        borderColor: '#FFFFFF',
                        backgroundColor: 'rgba(100, 100, 100, 0.8)',
                        borderWidth: 2
                      }

                      for (var i = 0; i < data.length; i++) {
                        labels.push(data[i].created_date.split("GMT")[0])
                        datasetsSingle.data.push(data[i].data_sensor.lvlsingle)
                        datasetsSingleTem.data.push(data[i].data_sensor.temperature)
                        datasetsSingleHum.data.push(data[i].data_sensor.humidity)  
                      }
                    this.datacollectionLine = [{
                      labels: labels,
                      datasets: [datasetsSingle]
                    },{
                      labels: labels,
                      datasets: [datasetsSingleTem,datasetsSingleHum]
                    },
                    ];
                    } 
                    else {
                      var datasetsPlastic = {
                        label: 'Plastico',
                        data: [],
                        fill: true,
                        borderColor: '#2554FF',
                        backgroundColor: 'rgba(33, 76, 229, 0.5)',
                        borderWidth: 2
                      }
                      var datasetsMetal = {
                        label: 'Metal',
                        data: [],
                        fill: true,
                        borderColor: '#FF5425',
                        backgroundColor: 'rgba(229, 76, 33,0.5)',
                        borderWidth: 2
                      }
                      var datasetsPaper = {
                        label: 'Papel/Carton',
                        data: [],
                        fill: true,
                        borderColor: '#FFFFFF',
                        backgroundColor: 'rgba(100, 100, 100, 0.8)',
                        borderWidth: 2
                      }
                      var datasetsTem = {
                        label: 'Temperatura(C)',
                        data: [],
                        fill: true,
                        borderColor: '#2554FF',
                        backgroundColor: 'rgba(33, 76, 229, 0.5)',
                        borderWidth: 2
                      }
                      var datasetsHum = {
                        label: 'Humedad(%)',
                        data: [],
                        fill: true,
                        borderColor: '#FFFFFF',
                        backgroundColor: 'rgba(100, 100, 100, 0.8)',
                        borderWidth: 2
                      }

                      for (var i = 0; i < data.length; i++) {
                        labels.push(data[i].created_date.split("GMT")[0])
                        datasetsPlastic.data.push(data[i].data_sensor.lvlPlastic)
                        datasetsMetal.data.push(data[i].data_sensor.lvlMedal)
                        datasetsPaper.data.push(data[i].data_sensor.lvlPaper)
                        datasetsTem.data.push(data[i].data_sensor.temperature)
                        datasetsHum.data.push(data[i].data_sensor.humidity)
                      }

                    this.datacollectionLine = [{
                      labels: labels,
                      datasets: [datasetsPlastic, datasetsMetal, datasetsPaper]

                    },{
                      labels: labels,
                      datasets: [datasetsTem,datasetsHum]

                    }];

                    }
                    //console.log(labels)
                    this.loadedLine = true;
            } catch (error) {
                console.error(error);
            }       

            }
            
        },
        async updateValuesPeriodically(){
          var x,y;
          if(this.selected != null){
             
            try {
              var res = await axios.get(`${API_URL}/bindata/0`,{ params: {namebin: this.selected.split(" ")[0] }});

              if (res.status == 200) {
                //clearInterval(x);
                //clearInterval(y);
                this.namebin = this.selected
                this.getLastValues()
                this.getBinGraphicValues()
                //x = setInterval(this.getLastValues,5000)
               // y = setInterval(this.getBinGraphicValues,5000)   
              }        
            } catch (error) {
              Swal.fire(
                'No hay datos!',
                '',
                'error'
              )
              
            }
              
            } else { 

            }
        },
        async loadAvailableBins(){
            try {
                console.log(this.userlogged.rnc_compa)
                var res = await axios.get(`${API_URL}/dustbin/1`,{ params: {rncComp: this.userlogged.rnc_compa}});

                for (var i = 0; i < res.data.length; i++) {
                    this.listAvailableBins.push(res.data[i].name + " - " + res.data[i].type + " - " + res.data[i].material_waste)        
                    let row = {name:res.data[i].name,type:res.data[i].type,material:res.data[i].material_waste,location:res.data[i].coordinates,description:res.data[i].description,date:res.data[i].created_date}
                    this.items.push(row) 
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
        },
        async loadDataBinTable(){
          this.getNow();
          this.itemsD = []
            try {
                console.log(this.userlogged.rnc_compa)
                var res = await axios.get(`${API_URL}/dustbin/1`,{ params: {rncComp: this.userlogged.rnc_compa}});
               
                for (var i = 0; i < res.data.length; i++) { 
                    var res1 = await axios.get(`${API_URL}/bindata/2`,{ params: {namebin: res.data[i].name }}); 

                      for (var x = 0; x < res1.data.length; x++) { 
                         if(res.data[i].type == 'Tradicional - 1 contenedor'){
                              let row = {name:res.data[i].name,level:res1.data[x].data_sensor.lvlsingle,volumen:res1.data[x].data_sensor.volumen,temperature:res1.data[x].data_sensor.temperature,
                                        humidity:res1.data[x].data_sensor.humidity,nodedate:res1.data[x].data_sensor.nodeDate,date:res1.data[x].created_date,datatype:res1.data[x].data_sensor.datatype}
                              this.itemsD.push(row);
                          }else{          
                              let lvl = (String(res1.data[x].data_sensor.lvlPlastic) + "-" + String(res1.data[x].data_sensor.lvlMedal) + "-" + String(res1.data[x].data_sensor.lvlPaper));
                              let row = {name:res.data[i].name,level:lvl,volumen:res1.data[x].data_sensor.volumen,temperature:res1.data[x].data_sensor.temperature,
                                        humidity:res1.data[x].data_sensor.humidity,nodedate:res1.data[x].data_sensor.nodeDate,date:res1.data[x].created_date,datatype:res1.data[x].data_sensor.datatype}
                              this.itemsD.push(row);
                              //console.log(res1.data[x].created_date)
                          }
                      }
                }
  
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
        },
        onRowSelected(items) {
            this.selectedTable = items;
            //this.getBinGraphicValues();
        },
    },
    computed: {
      rows() {
        return this.itemsD.length
      }
    },
    created(){

       socket.on("mqtt_message", fetchedData => {
                if(this.namebin != null){
                   this.updateValuesPeriodically()
                   this.itemsD = []
                   this.loadDataBinTable()
                } 
            })

    },
    mounted(){
      this.$emit('childToParent', this.userlogged)
      this.loadAvailableBins()
      this.loadDataBinTable();
        // Set the initial number of items
      this.totalRows = this.itemsD.length
       

     
    }
}

</script>

<style>
    @import '../assets/styles/main.css';
</style>
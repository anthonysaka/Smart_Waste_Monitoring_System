<template>
    <div class="Dashboard">
        <b-container fluid>
            <b-row>
                <b-col cols="12" md="4">
                    <div class="card shadow">
                        <div class="card-body">
                             <div id="map" style="height: 80vh;
                                width: 100%;"></div>
                        </div>
                    </div>
            
                </b-col>

                <b-col cols="12" md="8">
                    <div class="card mb-4">
                        <b-form-select
                            v-model="selected"
                            :options="listAvailableBins"
                            class="mb-0"
                            value-field="item"
                            text-field="name"
                            disabled-field="notEnabled"
                            ></b-form-select>    
                    </div>
                    <div class="card w-200">
                        <div class="d-flex px-2 pb-4">
                            <h5 class="h5 mr-auto ml-2 mt-2 mb-n1 text-gray-800" style="color: RGB(79, 79, 79) !important;">Live Data of:<strong>{{titlebin}}</strong></h5>
                            <hr>
                            <h5 class="h5 mt-2 mb-n1 mr-2  text-gray-800" style="color: RGB(79, 79, 79) !important;">Last update at:<strong>{{updatetime}}</strong></h5>
                            <hr>
                        </div>
                       
                        <div class="d-flex flex-column mb-4">
                            <b-row>
                                <b-col cols="12" md="3">
                                    <div class="minicard shadow h-10 py-1 ml-2 mr-2">
                                        <div class="card-body" style="height: 10vh;">
                                            <div class="d-flex flex-column">
                                                <div
                                                    class="text-xs font-weight-bold text-center mt-n3 text-primary text-uppercase mb-1">
                                                    <strong>Temperatura (°C)</strong></div>
                                            </div>
                                            <b-row>
                                                <b-col cols="6">
                                                    <div class="d-flex flex-column text-center">
                                                        <i class="fas fa-temperature-high fa-2x"></i>
                                                    </div>
                                                </b-col>
                                                <b-col cols="6">
                                                    <div
                                                        class="h5 mb-0 text-center mt-2 px-0 font-weight-bold text-gray-800">
                                                        <b-badge  variant="primary">{{tempValue}}</b-badge></div>
                                                </b-col>

                                            </b-row>
                                        </div>
                                    </div>
                                </b-col>

                                <b-col cols="12" md="3">
                                    <div class="minicard shadow h-10 py-1 ml-2 mr-2">
                                        <div class="card-body" style="height: 10vh;">
                                            <div class="d-flex flex-column">
                                                <div
                                                    class="text-xs font-weight-bold text-center mt-n3 text-primary text-uppercase mb-1">
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
                                                         <b-badge pill variant="primary">{{humValue}}</b-badge></div>
                                                </b-col>

                                            </b-row>
                                        </div>
                                    </div>
                                </b-col>

                                <b-col cols="12" md="3">
                                    <div class="minicard shadow h-10 py-1 ml-2 mr-2">
                                        <div class="card-body" style="height: 10vh;">
                                            <div class="d-flex flex-column">
                                                <div
                                                    class="text-xs font-weight-bold text-center mt-n3 text-primary text-uppercase mb-1">
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
                                                        N/A</div>
                                                </b-col>

                                            </b-row>
                                        </div>
                                    </div>
                                </b-col>

                                <b-col cols="12" md="3">
                                    <div class="minicard shadow h-10 py-1 ml-2 mr-2">
                                        <div class="card-body" style="height: 10vh;">
                                            <div class="d-flex flex-column">
                                                <div
                                                    class="text-xs font-weight-bold text-center mt-n3 text-primary text-uppercase mb-1">
                                                    ESTADO</div>
                                            </div>
                                            <b-row>
                                                <b-col cols="6">
                                                    <div class="d-flex flex-column text-center">
                                                        <i class="fas fa-tint fa-2x"></i>
                                                    </div>
                                                </b-col>
                                                <b-col cols="6">
                                                    <div class="h5 mb-0 text-center mt-2 font-weight-bold text-gray-800">
                                                        N/A</div>
                                                </b-col>

                                            </b-row>
                                        </div>
                                    </div>
                                </b-col>
                            </b-row>
                        </div>

                        <div class="d-flex flex-column mb-4" >
                            <b-row>
                                <b-col cols="12" md="4">
                                    <div class="minicard shadow mb-2 mt-2 ml-2 mr-0">
                                        <!-- Card Header -->
                                        <div class="card-header py-3">
                                            <h6 class="m-0 font-weight-bold text-primary"><strong>Plastico - Nivel de
                                                Llenado:  </strong>  <b-badge pill variant="primary">{{ levelplastic }} %</b-badge>
                                            </h6>
                                        </div>
                                        <!-- Card Body -->
                                        <div class="card-body">
                                            <div class="chart-pie pt-4">
                                                <levelChart :width="250" :height="250" v-if="loaded"
                                                            :chart-data="datacollection[0]">
                                                </levelChart>
                                            </div>
                                        </div>
                                    </div>
                                </b-col>

                                <b-col cols="12" md="4">
                                    <div class="minicard shadow mb-2 mt-2 ml-0 mr-0">
                                        <!-- Card Header -->
                                        <div class="card-header py-3">
                                            <h6 class="m-0 font-weight-bold text-primary">Metal - Nivel de
                                                Llenado:  <b-badge pill variant="primary">{{ levelmetal }} %</b-badge>
                                            </h6>
                                        </div>
                                        <!-- Card Body -->
                                        <div class="card-body">
                                            <div class="chart-pie pt-4">
                                                <levelChart :width="250" :height="250" v-if="loaded"
                                                            :chart-data="datacollection[1]">
                                                </levelChart>
                                            </div>
                                        </div>
                                    </div>
                                </b-col>

                                <b-col cols="12" md="4">
                                    <div class="minicard shadow mb-2 mt-2 ml-0 mr-2">
                                        <!-- Card Header -->
                                        <div class="card-header py-3">
                                            <h6 class="m-0 font-weight-bold text-primary">Papel/Carton - Nivel de
                                                Llenado:  <b-badge pill variant="primary">{{ levelpaper}} %</b-badge>
                                            </h6>
                                        </div>
                                        <!-- Card Body -->
                                        <div class="card-body">
                                            <div class="chart-pie pt-4">
                                                <levelChart :width="250" :height="250" v-if="loaded"
                                                            :chart-data="datacollection[2]">
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
        </b-container>
    </div>

</template>

<script>
import levelChart from '../components/donutChart';
import axios from 'axios';
import mapboxgl from "mapbox-gl";

export default {
    components:{
        levelChart
    },
    data (){
        return {
            userlogged: JSON.parse(localStorage.getItem('userdata')),
            datacollection: [],
            loaded: false,
            tempValue: null,
            humValue: null,
            levelplastic: null,
            levelmetal: null,
            levelpaper: null,
            selected: null,
            titlebin: null,
            updatetime:null,
            listAvailableBins: [ ],
            accessToken: 'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw',
        }
    },
    methods: {
        async getLastValues(){
            if(this.selected != null) {
                try {
               
                
                this.titlebin = this.selected.split(" ")[0]
                var res = await axios.get('http://localhost:5000/gomibako/internalapi/1.0/bindata',{ params: {namebin: this.selected.split(" ")[0] }});
                var data = res.data;
                this.updatetime = data.created_date;
                this.levelplastic = data.data_sensor.lvlPlastic;
                this.levelmetal = data.data_sensor.lvlMedal;
                this.levelpaper = data.data_sensor.lvlPaper;
                console.log(data.data_sensor.lvlPlastic);
                 console.log(data.data_sensor.lvlMedal);
                  console.log(data.data_sensor.lvlPaper);
                this.datacollection = [{
                    labels: ['Nivel de llenado'],
                    
                    datasets: [{
                        label: 'Data One',
                        backgroundColor: ['#2e59d9', "#ffffff"],
                        hoverBackgroundColor: ['#2e59d9','#ffffff'],
                        borderColor:['#2e59d9', "#ffffff"],
                        hoverBorderColor: ["#070707","#070707"],
                        data: [data.data_sensor.lvlPlastic, 100 - data.data_sensor.lvlPlastic]
                }],
                },{
                    labels: ['Nivel de llenado'],
                    datasets: [{
                        label: 'Data One',
                        backgroundColor: ['#2e59d9', "#ffffff"],
                        hoverBackgroundColor: ['#2e59d9','#ffffff'],
                        borderColor:['#2e59d9', "#ffffff"],
                        hoverBorderColor: ["#070707","#070707"],
                        data: [data.data_sensor.lvlMedal, 100 - data.data_sensor.lvlMedal]
                }],
                },{
                    labels: ['Nivel de llenado'],
                    datasets: [{
                        label: 'Data One',
                        backgroundColor: ['#2e59d9', "#ffffff"],
                        hoverBackgroundColor: ['#2e59d9','#ffffff'],
                        borderColor:['#2e59d9', "#ffffff"],
                        hoverBorderColor: ["#070707","#070707"],
                        data: [data.data_sensor.lvlPaper, 100 - data.data_sensor.lvlPaper]
                }],
                }
                ];
                this.tempValue = data.data_sensor.temperature;
                this.humValue = data.data_sensor.humidity;
               
                
                this.loaded = true;
            } catch (error) {
                console.error(error);
            }       

            }
            
        },
        async loadAvailableBins(){
            try {
                console.log(this.userlogged.rnc_org)
                var res = await axios.get('http://localhost:5000/gomibako/internalapi/1.0/dustbin/1',{ params: {rncComp: this.userlogged.rnc_org }});

                for (var i = 0; i < res.data.length; i++) {
                    this.listAvailableBins.push(res.data[i].name + " - " + res.data[i].type)        
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
        }
    },
    mounted(){
        this.getLastValues()
        setInterval(this.getLastValues, 5000)

        this.loadAvailableBins()

        mapboxgl.accessToken = this.accessToken;

           var map = new mapboxgl.Map({
                container: "map",
                style: "mapbox://styles/mapbox/streets-v11",
                center: [-70.703692, 19.415888],
                zoom: 12,
            });
    }
}

</script>

<style>
    @import '../assets/styles/main.css';
</style>
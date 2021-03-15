<template>
  <div class="home">

    <b-row class="mb-4">

      <b-col cols="12" md="3">
        <h5 class="h5 text-gray-800 py-2 " style="display: flex;justify-content: center;"><strong>ESTADO DE LOS BASUREROS </strong></h5>

        <b-row class="mt-2 px-4" >
          <b-col cols="12" style="display: flex;justify-content: center;">
            <div class="card  shadow" style="height: 6rem; width: 80%">
            <div class="minicard  h-10 py-1 ml-2 mr-2">
              <div class="card-body" style="height: 10vh;">
                <div class="d-flex flex-column">
                  <div class="text-s font-weight-bold text-center mt-n3 text-primary text-uppercase mb-1">
                    <strong>NORMAL [< 80]</strong></div>
                </div>
                <b-row>
                  <b-col cols="6">
                    <div class="d-flex flex-column text-center">
                      <i class="fas fa-trash-alt fa-2x text-primary"></i>
                    </div>
                  </b-col>
                  <b-col cols="6">
                    <div class="h4 mb-0 text-center mt-2 font-weight-bold text-gray-800">
                      <b-badge variant="primary">{{amountNormal}}</b-badge>
                    </div>
                  </b-col>

                </b-row>
              </div>
            </div>
            </div>
          </b-col>
        </b-row>

        <b-row class="mt-2 px-4">
          <b-col cols="12" style="display: flex;justify-content: center;">
            <div class="card  shadow" style="height: 6rem; width: 80%">
            <div class="minicard  h-10 py-1 ml-2 mr-2">
              <div class="card-body" style="height: 10vh;">
                <div class="d-flex flex-column">
                  <div class="text-s font-weight-bold text-center mt-n3 text-warning text-uppercase mb-1">
                    <strong>FULL [80-95]</strong></div>
                </div>
                <b-row>
                  <b-col cols="6">
                    <div class="d-flex flex-column text-center">
                      <i class="fas fa-trash-alt fa-2x text-warning"></i>
                    </div>
                  </b-col>
                  <b-col cols="6">
                    <div class="h4 mb-0 text-center mt-2 font-weight-bold text-gray-800">
                      <b-badge variant="warning">{{amountFull}}</b-badge>
                    </div>
                  </b-col>

                </b-row>
              </div>
            </div>
            </div>
          </b-col>
        </b-row>

        <b-row class="mt-2 px-4">
          <b-col cols="12" style="display: flex;justify-content: center;">
            <div class="card  shadow" style="height: 6rem; width: 80%">
            <div class="minicard  h-10 py-1 ml-2 mr-2">
              <div class="card-body" style="height: 10vh;">
                <div class="d-flex flex-column">
                  <div class="text-s font-weight-bold text-center mt-n3 text-danger text-uppercase mb-1">
                    <strong>OVERLOAD [> 95]</strong></div>
                </div>
                <b-row>
                  <b-col cols="6">
                    <div class="d-flex flex-column text-center">
                      <i class="fas fa-trash-alt fa-2x text-danger"></i>
                    </div>
                  </b-col>
                  <b-col cols="6">
                    <div class="h4 mb-0 text-center mt-2 font-weight-bold text-gray-800">
                      <b-badge variant="danger">{{amountOverload}}</b-badge>
                    </div>
                  </b-col>

                </b-row>
              </div>
            </div>
            </div>
          </b-col>
        </b-row>

        <b-row class="mt-2 px-4 pt-4">
          <b-col cols="12" style="display: flex;justify-content: center;">
            <div class="card  shadow" style="width: 80%">
              <div class="minicard  h-10 py-1 ml-2 mr-2">
                 <div class="card-header" style="display: flex;justify-content: center;">
                        <h6 class="m-0 font-weight-bold"><strong>Estado Sensores</strong>
                      
                        </h6>
                  </div>
                <div class="card-body">
                  <div class="chart-pie pt-2">
                    <levelChart :width="150" :height="150" v-if="loadedDonut" :chart-data="datacollectionDonut[0]">
                    </levelChart>
                  </div>
                </div>
              </div>
            </div>
          </b-col>
        </b-row>
         

        

      </b-col>
      

      <b-col cols="12" md="9">
        <div class="card shadow">
          <div class="card-body">
            <div id="map" style="height: 80vh;
                                width: 100%;"></div>
          </div>
        </div>
      </b-col>


    </b-row>
    <!--     ****************  -->



  </div>
</template>

<script>
  import mapboxgl from "mapbox-gl";
  import Swal from 'sweetalert2';
  import axios from 'axios';
  const API_URL = process.env.API_URL;
  import levelChart from '../components/donutChart';
  import Vue from 'vue';
  import VueToast from 'vue-toast-notification';
  import 'vue-toast-notification/dist/theme-sugar.css';
  Vue.use(VueToast);
  const map = null;


  export default {
    name: "Home",
    components:{
        levelChart,
    },
    data() {
      return {
        accessToken: 'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw',
        userlogged: JSON.parse(localStorage.getItem('userdata')),
        geoJson: null,
        amountNormal: 0, 
        amountFull: 0, 
        amountOverload: 0,
        datacollectionDonut: [],
        loadedDonut: false,
       
      };
    },
    methods: {
      async loadAvailableBinsOnMap() {
        try {
          console.log(this.userlogged.rnc_compa)
          var res = null;
          res = await axios.get(`${API_URL}/dustbin/1`, {
            params: {
              rncComp: this.userlogged.rnc_compa
            }
          });
          var auxFeatures = [];

          for (var i = 0; i < res.data.length; i++) {
            let auxCoor = res.data[i].coordinates.split(",")
            auxFeatures.push({
              type: 'Feature',
              status:res.data[i].status,
              geometry: {
                type: 'Point',
                coordinates: [auxCoor[0], auxCoor[1]]
              },
              properties: {
                title: res.data[i].name,
                description: res.data[i].description,
              }
            })
          }

          this.geoJson = {
            type: 'FeatureCollection',
            features: auxFeatures,
          }

          mapboxgl.accessToken = this.accessToken;
          map = new mapboxgl.Map({
            container: "map",
            style: "mapbox://styles/mapbox/streets-v11",
            center: [-70.703692, 19.415888],
            zoom: 12,
          });

          if (res != null) {
            setInterval(async()=>{
              var res = null;
          res = await axios.get(`${API_URL}/dustbin/1`, {
            params: {
              rncComp: this.userlogged.rnc_compa
            }
          });
          var auxFeatures = [];

          for (var i = 0; i < res.data.length; i++) {
            let auxCoor = res.data[i].coordinates.split(",")
            auxFeatures.push({
              type: 'Feature',
              status:res.data[i].status,
              geometry: {
                type: 'Point',
                coordinates: [auxCoor[0], auxCoor[1]]
              },
              properties: {
                title: res.data[i].name,
                description: res.data[i].description,
              }
            })
          }

          this.geoJson = {
            type: 'FeatureCollection',
            features: auxFeatures,
          }
              // add markers to map
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
            

            // make a marker for each feature and add to the map
            new mapboxgl.Marker(el)
              .setLngLat(marker.geometry.coordinates)
              .setPopup(new mapboxgl.Popup({
                  offset: 25
                }) // add popups
                .setHTML('<h5>' + marker.properties.title + '</h5><strong>' + marker.properties.description + '</strong>'))
              .addTo(map);
          });        
              

            },5000)
          }
            

          
          // Add zoom and rotation controls to the map.
          map.addControl(new mapboxgl.NavigationControl());
          

        } catch (error) {
          console.log(error)
           mapboxgl.accessToken = this.accessToken;
          var map = new mapboxgl.Map({
            container: "map",
            style: "mapbox://styles/mapbox/streets-v11",
            center: [-70.703692, 19.415888],
            zoom: 12,
          });
        }
      },
      async loadDataResumeCardsDashboard(){
            try {
                console.log(this.userlogged.rnc_compa)
                var res = await axios.get(`${API_URL}/dustbin/1`,{ params: {rncComp: this.userlogged.rnc_compa}});

                for (var i = 0; i < res.data.length; i++) {
                   if (res.data[i].status == 0) {
                     this.amountNormal++;
                   } else if (res.data[i].status == 1) {
                     this.amountFull++;
                   } else{
                     this.amountOverload++;
                   }

                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
        },
      async updateLastSeenDevices(){
        try {
          var res = null;
          res = await axios.get(`${API_URL}/dustbin/1`, {
                                                          params: {
                                                            rncComp: this.userlogged.rnc_compa
                                                          }
                                                        });
          var auxNumActive = 0;
          var auxNumInactive = 0;
          const today = new Date();
          const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
          const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
          const dateTime1 = date +' '+ time;
          let dateTime = new Date(dateTime1);

          for (var i = 0; i < res.data.length; i++) {
              let auxDateTime = res.data[i].active.split("G")[0];
              let aux = new Date(auxDateTime);
              let dif = (dateTime.getTime() - aux.getTime())/1000;
              if(dif<30){
                auxNumActive++;
              } else {
                auxNumInactive++;
                //send alert
                Vue.$toast.open({
                  message: "Sensor Inactivo!\n\n"+res.data[i].name,
                  type: "warning",
                  position:"top-right",
                  duration: 5000,
                  dismissible: true
                })
          
              }
          }

        this.datacollectionDonut = [{
                            labels: ['Activo','Inactivo'],
                            
                            datasets: [{
                                label: 'Data One',
                                backgroundColor: ['#2e59d9', "#ffffff"],
                                hoverBackgroundColor: ['#2e59d9','#ffffff'],
                                borderColor:['#2e59d9', "#ffffff"],
                                hoverBorderColor: ["#070707","#070707"],
                                data: [auxNumActive,auxNumInactive]
                        }],
          }];
        this.loadedDonut = true;
        } catch (error) {
          
        }

              
            
        },
      },
      mounted() {
        this.$emit('childToParent', this.userlogged)
        this.loadAvailableBinsOnMap();
        this.loadDataResumeCardsDashboard();
        this.userlogged = JSON.parse(localStorage.getItem('userdata'));
        
        this.updateLastSeenDevices(); //poner esto ciclico y mover a app.vue
       // setInterval(this.updateLastSeenDevices,10000)
        

        if (this.userlogged.default_credentials == true) {
          Swal.mixin({
            confirmButtonText: 'Next &rarr;',
            progressSteps: ['1', '2', '3', '4'],
            allowOutsideClick: false

          }).queue([{
              title: 'Hey, hemos detectado que aun no has cambiado tus credenciales por defecto, por favor continuar para cambiarlas (Es muy recomendado).',
              showCancelButton: true,
            },
            {
              input: 'text',
              title: 'Cambiar el nombre de usuario por defecto',
              text: 'Por favor introducir un nuevo nombre de usuario',
              showCancelButton: false,
              inputValidator: (value) => {
                if (!value) {
                  return 'You need to write something!'
                }
              }
            },
            {
              input: 'password',
              title: 'Cambiar contrasena por defecto',
              text: 'Por favor introducir una nueva contrasena',
              showCancelButton: false,
              inputValidator: (value) => {
                if (!value) {
                  return 'You need to write something!'
                }
              }
            },
          ]).then(async (result) => {
            if (result.value) {
              try {
                const res = await axios.put(`${API_URL}/changecredentials`, {
                "id": this.userlogged.id,
                "newusername": result.value[1],
                "newpassword": result.value[2]
              })
                
              } catch (error) {
                Swal.fire(
                  "usuario ya existe",
                  "",
                  "error"
                )
              }
                const username = result.value[1]
                const password = result.value[2]
                const res1 = await axios.post(`${API_URL}/login`, {
                    username,
                    password
                  })
                localStorage.setItem('userdata', JSON.stringify(res1.data.user[0]))
                this.userlogged = JSON.parse(localStorage.getItem('userdata'))
              
            
              
            }
          })
        }


      }
      };
</script>

<style>
  @import '../assets/styles/main.css';
</style>

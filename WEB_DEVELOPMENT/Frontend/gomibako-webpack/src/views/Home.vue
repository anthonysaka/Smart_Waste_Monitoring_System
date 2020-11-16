<template>
  <div class="home">

    <b-row class="mb-4">

      <b-col cols="12" md="3">

        <b-row>
          <b-col cols="12">
            <div class="card  shadow" style="height: 6rem; width: 80%">
                <div class="card-body">
                  <div class="row no-gutters align-items-center">
                    <div class="col mr-1">
                      <div class="d-flex flex-column">
                        <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Activos</div>
                      </div>
                      <div class="d-flex flex-column">
                        <div class="h5 mb-0 font-weight-bold text-gray-800">DATO</div>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-trash fa-2x text-success"></i>
                    </div>
                  </div>
                </div>
              </div>
          </b-col>
        </b-row>

        <b-row>
          <b-col cols="12">
            <div class="card  shadow" style="height: 6rem; width: 80%">
                <div class="card-body">
                  <div class="row no-gutters align-items-center">
                    <div class="col mr-1">
                      <div class="d-flex flex-column">
                        <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Activos</div>
                      </div>
                      <div class="d-flex flex-column">
                        <div class="h5 mb-0 font-weight-bold text-gray-800">DATO</div>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-trash fa-2x text-success"></i>
                    </div>
                  </div>
                </div>
              </div>
          </b-col>
        </b-row>

        <b-row>
          <b-col cols="12">
            <div class="card  shadow" style="height: 6rem; width: 80%">
                <div class="card-body">
                  <div class="row no-gutters align-items-center">
                    <div class="col mr-1">
                      <div class="d-flex flex-column">
                        <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Activos</div>
                      </div>
                      <div class="d-flex flex-column">
                        <div class="h5 mb-0 font-weight-bold text-gray-800">DATO</div>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-trash fa-2x text-success"></i>
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

  export default {
    name: "Home",
    data() {
      return {
        accessToken: 'pk.eyJ1IjoiYW50aG9ueXNha2EiLCJhIjoiY2tnbjBrZWR4MGkwNDJ0cGczb2UxNTE4YiJ9.WsEmhirejFVApuNz9Ivtlw',
        userlogged: JSON.parse(localStorage.getItem('userdata')),
      };
    },
    mounted() {
      this.$emit('childToParent',this.userlogged)
      mapboxgl.accessToken = this.accessToken;
      var map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v11",
        center: [-70.703692, 19.415888],
        zoom: 12,
      });

      var geojson = { type: 'FeatureCollection',
                      features: [{
                        type: 'Feature',
                        geometry: {
                          type: 'Point',
                          coordinates: [-70.702859,19.416531]
                        },
                        properties: {
                          title: 'Mapbox',
                          description: 'Washington, D.C.'
                        }
                      },
                      ]
                    };
      // add markers to map
      geojson.features.forEach(function(marker) {

        // create a HTML element for each feature
        var el = document.createElement('div');
        el.className = 'marker';

        // make a marker for each feature and add to the map
        new mapboxgl.Marker(el)
          .setLngLat(marker.geometry.coordinates)
            .setPopup( new mapboxgl.Popup({ offset: 25}) // add popups
          .setHTML('<h3>' + marker.properties.title + '</h3><p>' + marker.properties.description + '</p>'))
          .addTo(map);
      });
      


      this.userlogged = JSON.parse(localStorage.getItem('userdata'));
      if (this.userlogged.default_credentials == true) {
        Swal.mixin({
                      confirmButtonText: 'Next &rarr;',
                      progressSteps: ['1', '2', '3','4'],
                      allowOutsideClick: false
                      
                    }).queue([
                      {
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
                    ]).then(async(result) => {
                      if (result.value) {
                        const res = await axios.put('http://localhost:5000/gomibako/internalapi/1.0/changecredentials',
                                            {
                                                "id":this.userlogged.id,
                                                "newusername":result.value[1],
                                                "newpassword":result.value[2]
                                            }) 
                        const username = result.value[1] 
                        const password = result.value[2]       
                        const res1 = await axios.post('http://localhost:5000/gomibako/internalapi/1.0/login', {username,password})
                        localStorage.setItem('userdata', JSON.stringify(res1.data.user[0]))
                        this.userlogged = JSON.parse(localStorage.getItem('userdata')),
                        console.log(res);    
                      }
                    })
      }


    }
  };
</script>

<style>
  @import '../assets/styles/main.css';
</style>

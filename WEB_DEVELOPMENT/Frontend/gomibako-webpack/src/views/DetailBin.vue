<template>
  <div class="detailbin">

    <div class="d-flex flex-column mb-4">
      <b-row>

        <b-col cols="12" md="4">
          <div class="card shadow">
            <div class="card-body">
              <div class="chart-area pt-4">
                <lineChart :width="200" :height="200" v-if="loaded" 
                    :chart-data="datacollection[0]">
                </lineChart>
              </div>
            </div>
          </div>
        </b-col>

        <b-col cols="12" md="8">
            <b-table    responsive="sm" 
                        striped hover 
                        :items="items" 
                        :fields="fields" 
                        head-variant="light"
                        selectable
                        select-mode="single"
                        @row-selected="onRowSelected">
                    
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
        </b-col>


      </b-row>
    </div>
      
   <div class="d-flex flex-column mt-2">
     <b-row>
       <b-col cols="6" md="4">
         <!-- <div class="card shadow">
           <div class="card-body">
             <div class="chart-area pt-4">
               <lineChart :width="200" :height="200" v-if="loaded" :chart-data="datacollection[0]">
               </lineChart>
             </div>
           </div>
         </div> -->
       </b-col>

     </b-row>
   </div>
     
      
  </div>
</template>

<script>
import lineChart from '../components/lineChart';
import axios from 'axios';
const API_URL = process.env.API_URL
export default {
    components:{
        lineChart,
    },
    data() {
        return {
            datacollection: [],
            loaded: false,
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
                    key: 'deviceEUI',
                    label: 'DEVICE EUI',
                    sortable: true
                }, 
                {
                    key: 'type',
                    label: 'TIPO',
                    sortable: true,
                },
                {
                    key: 'material',
                    label: 'MATERIAL CONTENIDO',
                    sortable: true,
                },
                {
                    key: 'location',
                    label: 'Ubicacion',
                    sortable: true,
                },
                {
                    key: 'description',
                    label: 'Descripcion',
                    sortable: true,
                },

            ],
            items: [ ],
            selected:null,
            userlogged: JSON.parse(localStorage.getItem('userdata')),
        }
    },
    methods: {
        async getBinValues(){
            if(this.selected != null) {
                try {           
                    var res = await axios.get(`${API_URL}/bindata/1`,{ params: {namebin: this.selected.name }});
                    var data = res.data;
                 
                    var labels = []
                    var datasetsPlastic = [
                                {
                                label: 'Line Chart',
                                data: [],
                                fill: false,
                                borderColor: '#2554FF',
                                backgroundColor: '#2554FF',
                                borderWidth: 2
                                }
                            ]
                    var datasetsMetal = [
                                {
                                label: 'Line Chart',
                                data: [],
                                fill: false,
                                borderColor: '#FF5425',
                                backgroundColor: '#FF5425',
                                borderWidth: 2
                                }
                            ]
                    var datasetsPaper = [
                                {
                                label: 'Line Chart',
                                data: [],
                                fill: false,
                                borderColor: '#FFFFFF',
                                backgroundColor: '#FFFFFF',
                                borderWidth: 2
                                }
                            ]

                    for (var i = 0; i < data.length; i++) {
                       labels.push(data[i].created_date)
                       datasetsPlastic.data.push(data[i].data_sensor.lvlPlastic)
                       datasetsMetal.data.push(data[i].data_sensor.lvlMedal)
                       datasetsPaper.data.push(data[i].data_sensor.lvlPaper)
                    }
                    
                    this.datacollection = [{
                        labels: labels,
                        datasets: [datasetsPlastic,datasetsMetal,datasetsPaper]

                    }];
                this.loaded = true;
                
            } catch (error) {
                console.error(error);
            }       

            }
            
        },
        async loadAvailableBins(){
            try {
                console.log(this.userlogged.rnc_org)
                var res = await axios.get(`${API_URL}/dustbin/1`,{ params: {rncComp: this.userlogged.rnc_org }});
                console.log(res.data)
                for (var i = 0; i < res.data.length; i++) {
                    let row = {name:res.data[i].name,deviceEUI:res.data[i].deviceeui,type:res.data[i].type,material:res.data[i].material_waste,location:res.data[i].coordinates,description:res.data[i].description}
                    this.items.push(row)        
                }
                console.log(res.status)
            } catch (error) {
                console.log(error)
            }
        },
        onRowSelected(items) {
            this.selected = items;
            this.getBinValues();
        },
    },
    mounted(){

        this.loadAvailableBins();
    }
}
</script>

<style>

</style>
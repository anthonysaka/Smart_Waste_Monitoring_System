
<script>
import { Doughnut, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins;
export default {
  extends: Doughnut,
  mixins: [reactiveProp],
  data(){
      return{
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                tooltips: {
                    display: false
                },
                cutoutPercentage: 80,
                animation:{
                    animateRotate: true,
                    duration: 1000
                },
                
            }
      }      
  },
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}
</script>


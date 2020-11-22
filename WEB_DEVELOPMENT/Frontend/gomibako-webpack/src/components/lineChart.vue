
<script>
import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins;
export default {
  extends: Line,
  mixins: [reactiveProp],
  data(){
      return{
        options: {
            maintainAspectRatio: false,
            responsive: true,
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 0,
                    bottom: 0
                }
            },
            scales: {
                xAxes: [{
                    display: true,
                    time: {
                        unit: 'date'
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                }],
                yAxes: [{
                    display: true,
                    ticks: {
                        beginAtZero: true,
                        max:100,
                        suggestedMax: 100,
                        min:0,
                        suggestedMin:0,
                        stepSize: 10,
                        maxTicksLimit: 11,
                    },
                }],
            },
            legend: {
                display: true,
            },
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                titleMarginBottom: 10,
                titleFontColor: '#6e707e',
                titleFontSize: 14,
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                intersect: false,
                mode: 'index',
                caretPadding: 10,
            }
        }      
    }      
  },
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}
</script>


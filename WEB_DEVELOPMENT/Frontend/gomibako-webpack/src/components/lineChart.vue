
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
                    left: 5,
                    right: 5,
                    top: 0,
                    bottom: 0
                }
            },
            scales: {
                xAxes: [{
                    time: {
                        unit: 'date'
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                }],
                yAxes: [{
                    stacked: true,
                    ticks: {
                        maxTicksLimit: 10,
                        beginAtZero: true,
                    },
                    gridLines: {
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                }],
            },
            legend: {
                display: false
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


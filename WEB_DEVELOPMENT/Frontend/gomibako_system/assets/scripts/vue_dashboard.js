Vue.component('fill-level-chart', {
    extends: VueChartJs.Doughnut,
    props: {
        id: Number
    },
    data() {
        return {
            chartdata: {
                labels: ['Nivel de llenado'],
                datasets: [{
                    label: 'Data One',
                    backgroundColor: ['#2e59d9', "rgba(234, 236, 244, 1)"],
                    hoverBackgroundColor: ['#2e59d9'],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                    data: [80, 100 - 80]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                legend: {
                  display: false
                },
                tooltips: {
                    display: false
                },
                cutoutPercentage: 80,

                animation:{
                    animateRotate: true,
                    duration: 2000
                },
                title: {
                    display: true,
                    text: 'Custom Chart Title',
                    padding: 0
                }
            }
        }
    },
    mounted() {
        this.renderChart(this.chartdata, this.options)
    }

})

const app = new Vue({
    el: '#vue_app'
})
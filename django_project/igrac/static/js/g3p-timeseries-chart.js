let url = '/api/G3P_data/';
const chartColors = [
    "rgb(75, 192, 192)",
    "rgb(255, 99, 132)",
    "rgb(54, 162, 235)",
    "rgb(153, 102, 255)",
    "rgb(255, 205, 86)",
    "rgb(255, 159, 64)",
    "rgb(201, 203, 207)"
]

let convertTimeseriesData = (input) => {
    let data = {};
    input.map(function (row) {
        let parameter = row.par;
        let unit = row.u;
        let value = row.v;
        let unit_to = 'm';
        // value = unitConvert(unit, unit_to, value);
        // let's we save it
        if (value != null) {
            if (!data[parameter]) {
                data[parameter] = []
            }
            data[parameter].unshift(
                [row.dt * 1000, value]
            );
        }
    })
    return data;
}

function renderTimeseriesChart(identifier, id, chart, data, xLabel, yLabel, onChartClicked) {
    let title = identifier.replaceAll('_', ' ');
    if (!data) {
        data = []
    }
    const options = {
        chart: {
            zoomType: 'x',
            events: {
                click: function (event) {
                    onChartClicked(new Date(event.xAxis[0].value))
                }
            }
        },
        title: {
            text: title
        },
        yAxis: {
            title: {
                text: yLabel
            },
        },
        xAxis: {
            type: 'datetime',
            title: {
                text: xLabel
            }
        },
        legend: {
            enabled: true
        },
        rangeSelector: {
            buttons: [{
                type: 'day',
                count: 3,
                text: '3d'
            }, {
                type: 'week',
                count: 1,
                text: '1w'
            }, {
                type: 'month',
                count: 1,
                text: '1m'
            }, {
                type: 'month',
                count: 6,
                text: '6m'
            }, {
                type: 'year',
                count: 1,
                text: '1y'
            }, {
                type: 'all',
                text: 'All'
            }]
        },
        plotOptions: {
            series: {
                showInLegend: true,
                dataGrouping: { 
                    groupPixelWidth: 50, 
                    units: [['hour', [4]], ['day', [1]], ['week', [1, 2]], ['month', [1]]] }
            }
        },
        series: [
            {
                id: 'value',
                name: identifier.replaceAll('_', ' '),
                data: data,
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 2,
                states: {
                    hover: {
                        lineWidth: 2
                    }
                },
                color: '#24619d',
                tooltip: {
                    valueDecimals: 3
                },
                visible: true
            },
        ]
    }
    if (!chart) {
        chart = Highcharts.stockChart(`g3p-${id}-chart`, options);
    } else {
        chart.update(options);
    }
    return chart;
}
let TimeseriesChartObj = function (id, identifier, $loading, xlabel = "", ylabel = "") {
    this.identifier = identifier;
    this.id = id;
    this.$loading = $loading;
    this.url = url + `?id=${id}&name=${identifier}`;
    this.parameter = 'Groundwater Storage';

    const that = this;

    this.asyncRenderChart = function () {
        return new Promise(resolve => {
            that.$loading.show();
            setTimeout(() => {
                that._renderChart();
            }, 200);
        });
    }

    this.renderChart = async function () {
        await this.asyncRenderChart();
    };

    this._renderChart = function () {
        const data = that.data;
        if (!data) {
            return;
        }
        const cleanData = convertTimeseriesData(data.data);
        const chartData = cleanData[this.parameter];
        this.chart = null;
        if (!chartData || chartData.length === 0) {
            that.$loading.hide();
            $(`#g3p-${this.id}-chart`).html(
                '<div style="text-align: center; color: red">No data found</div>');
            return
        }
        if (xlabel === "") {
            xlabel = "Time"
        }
        if (ylabel === "") {
            ylabel = "Groundwater storage anomaly (mm)"
        }
        this.chart = renderTimeseriesChart(
            this.identifier,
            this.id, 
            this.chart,
            chartData,
            xlabel, 
            ylabel,
            function (date) {
                // when chart is clicked
                console.log('clicked');
            })
        this.$loading.hide();
    }

    /** Fetch the data */
    this.fetchData = function () {
        this.$loading.show();
        if (this.url) {
            const that = this;
            $.ajax({
                url: this.url,
                dataType: 'json',
                success: function (data, textStatus, request) {
                    if (!that.data) {
                        that.data = {
                            data: [],
                        }
                    }
                    that.data.data = that.data.data.concat(data.data);
                    that.data.end = data.end;
                    that.renderChart();
                },
                error: function (error, textStatus, request) {
                    that.$loading.hide();
                    $(`#g3p-${this.id}-chart`).html(
                        '<div style="text-align: center; color: red">No data found</div>')
                }
            })
        }
    }
    this.fetchData();
}

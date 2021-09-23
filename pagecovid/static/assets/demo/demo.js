if (document.getElementById('myCanvas')) {
    var data = JSON.parse(document.getElementById('generate-data1').textContent);
    var data2 = JSON.parse(document.getElementById('generate-data2').textContent);
    var lables_data = JSON.parse(document.getElementById('lables').textContent);

    var totalDuration = 5000;
    var delayBetweenPoints = totalDuration / data.length;
    var previousY = (ctx) => ctx.index === 0 ? ctx.chart.scales.y.getPixelForValue(10) : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y;
    var animation = {
        x: {
            type: 'number',
            easing: 'linear',
            duration: delayBetweenPoints,
            from: NaN,
            delay(ctx) {
                if (ctx.type !== 'data' || ctx.xStarted) {
                    return 0;
                }
                ctx.xStarted = true;
                return ctx.index * delayBetweenPoints;
            }
        },
        y: {
            type: 'number',
            easing: 'linear',
            duration: delayBetweenPoints,
            from: previousY,
            delay(ctx) {
                if (ctx.type !== 'data' || ctx.yStarted) {
                    return 0;
                }
                ctx.yStarted = true;
                return ctx.index * delayBetweenPoints;
            }
        }
    };

    Chart.defaults.font.size = 13;

    var ctx = document.getElementById('myCanvas').getContext("2d");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: lables_data,
            datasets: [{
                label: "Статистика минздрава",
                borderColor: 'red',
                borderWidth: 2,
                radius: 1,
                data: data,
            },
            {
                label: "Прогнозируемая статистика",
                borderColor: 'blue',
                borderWidth: 2,
                radius: 1,
                data: data2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation,
            interaction: {
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Рекорд смертей зарегистрирован ' + String(lables_data[find_max_value()]) + ' (' + String(data[find_max_value()]['y']) + ' человек)',
                    color: 'black',
                    font: {
                        size: 20
                    }
                }
            },
        },
    })
}

if (document.getElementById('dead-canvas')) {
    const dData1 = JSON.parse(document.getElementById('dead-data1').textContent);
    const dData2 = JSON.parse(document.getElementById('dead-data2').textContent);
    const dLables_data = JSON.parse(document.getElementById('dead-lables').textContent);
    const dtotalDuration = 5000;
    const ddelayBetweenPoints = dtotalDuration / dData1.length;
    const dpreviousY = (ctx) => ctx.index === 0 ? ctx.chart.scales.y.getPixelForValue(10) : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y;

    const dAnimation = {
        x: {
            type: 'number',
            easing: 'linear',
            duration: ddelayBetweenPoints,
            from: NaN,
            delay(ctx) {
                if (ctx.type !== 'data' || ctx.xStarted) {
                    return 0;
                }
                ctx.xStarted = true;
                return ctx.index * ddelayBetweenPoints;
            }
        },
        y: {
            type: 'number',
            easing: 'linear',
            duration: ddelayBetweenPoints,
            from: dpreviousY,
            delay(ctx) {
                if (ctx.type !== 'data' || ctx.yStarted) {
                    return 0;
                }
                ctx.yStarted = true;
                return ctx.index * ddelayBetweenPoints;
            }
        }
    };

    Chart.defaults.font.size = 13;

    var ctx = document.getElementById('dead-canvas').getContext("2d");
    var deadChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dLables_data,
            datasets: [{
                label: "Статистика минздрава",
                borderColor: 'red',
                borderWidth: 2,
                radius: 1,
                data: dData1,
            },
            {
                label: "Прогнозируемая статистика",
                borderColor: 'blue',
                borderWidth: 2,
                radius: 1,
                data: dData2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            dAnimation,
            interaction: {
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Летальные исходы',
                    color: 'black',
                    font: {
                        size: 20
                    }
                },
                legend: {
                    font: {
                        size: 20
                    }
                }
            },
        },

    })
}


// find max value
function find_max_value() {
    var ind = 0, val = 0;
    for (var i = 0; i < data.length; i++) {
        if (Number(data[i]['y']) > val) {
            val = Number(data[i]['y']);
            ind = i;
        }
    }
    return ind
}

function parseString(str) {
    var newStr = ""

    for(var i = 0; i < str.length; i++) {
        if ((str[i] >= '0') && (str[i] <= '9')) {
            console.log(str[i])
            newStr += str[i]
        }

    }

    return Number(newStr)
}

// pie-chart

if (document.getElementById('pie-chart')) {

    var data_vaccination = JSON.parse(document.getElementById('vaccination').textContent);
    console.log(parseString(data_vaccination['population']))
    var pie_chart = new Chart(document.getElementById("pie-chart"), {
        type: 'pie',
        data: {
            labels: ["Получили обе дозы","Получили ни одной дозы"],
            datasets: [{
                label: "Population (millions)",
                backgroundColor: ["red", "#0046de"],
                data: [parseString(data_vaccination['fully_vaccinated']), parseString(data_vaccination['population']) * 1000]
            }]
        },
    });
}
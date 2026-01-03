const weather_condition = {
	"thunderstorm": '11d',
	"drizzle": '09d',
	"snow": '13d',
	"atmosphere": '50d',
};

const groups = {
	500: '10d',
	501: '10d',
	502: '10d',
	503: '10d',
	504: '10d',
	511: '13d',
	520: '09d',
	521: '09d',
	522: '09d',
	531: '09d',
	800: '01d',
	801: '02d',
	802: '03d',
	803: '04d',
	804: '03d',
};

let weather = {};
let gif = document.getElementById("weatherIcon");
let desc = document.getElementById("weatherDesc");
let temp = document.getElementById("weatherTemp");

async function request(){
	await axios({
		method: 'get',
		url: 'http://localhost:8080/weather-condition',
		header: {
			'Content-type': 'application/json',
		}
	})
	.then(function (weather) {
		const resp = JSON.parse(weather.request.response);
		temp.innerHTML = resp['temp'] + '&#176;C';
		if ( weather_condition[resp['description']]){
			gif.src = `https://openweathermap.org/img/wn/${weather_condition[resp['description']]}@2x.png`;
		}else{
			gif.src = `https://openweathermap.org/img/wn/${groups[resp['id']]}@2x.png`;
		}
		desc.innerHTML = resp['description'];
	})
	.catch(function (error) {
		console.log(error);
	});
};

request();
// Mapping of room names to their respective IDs
const roomMapping = {
    'Room 209': '8',
    'Room 109': '10',
    'Room 307': '11',
    'Room 129': '18',
    'Room 126': '19',
    'Room 229': '20',
    'Room 226': '21',
    'Room 326': '22'
};

// Function to fetch data from the API and get the latest temperature value
async function fetchDataAndPrintTemperature(roomName, roomId) {
    try {
        const currentTime = new Date().toISOString();

        const apiUrl = `https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id=${roomId}&startTime=2023-02-01T00:00:00Z&endTime=${currentTime}&fields=temperature`;

        const response = await fetch(apiUrl, {
            headers: {
                'x-api-key': 'II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay'
            },
            method: 'GET',
            mode: 'cors',
            cache: 'no-cache'
        });

        if (!response.ok) {
            throw new Error('Failed to fetch temperature data');
        }

        const data = await response.json();
        const valuesArray = data.results[0].series[0].values;
        valuesArray.sort((a, b) => a[0] - b[0]);
        const latestData = valuesArray[valuesArray.length - 1];
        const latestTemperature = latestData[1];

        // Update the content of the div element with the appropriate id
        const temperatureElement = document.getElementById(`temperature${roomId}`);
        temperatureElement.textContent = `Temperature: ${latestTemperature} °C`;


    } catch (error) {
        console.error(`Error for ${roomName}:`, error);
    }
}


async function fetchDataAndPrintCo2(roomName, roomId) {
    try {
        const currentTime = new Date().toISOString();

        const apiUrl = `https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id=${roomId}&startTime=2023-02-01T00:00:00Z&endTime=${currentTime}&fields=Co2`;

        const response = await fetch(apiUrl, {
            headers: {
                'x-api-key': 'II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay'
            },
            method: 'GET',
            mode: 'cors',
            cache: 'no-cache'
        });

        if (!response.ok) {
            throw new Error('Failed to fetch Co2 data');
        }

        const data = await response.json();
        const valuesArray = data.results[0].series[0].values;
        valuesArray.sort((a, b) => a[0] - b[0]);
        const latestData = valuesArray[valuesArray.length - 1];
        const latestCo2 = latestData[1];

        // Update the content of the humidity div element
        const Co2Element = document.getElementById(`Co2_${roomId}`);
        Co2Element.textContent = `Co2: ${latestCo2} ppm`;
    } catch (error) {
        console.error(`Error fetching Co2 for ${roomName}:`, error);
    }
}


async function fetchDataAndPrintHumidity(roomName, roomId) {
    try {
        const currentTime = new Date().toISOString();

        const apiUrl = `https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id=${roomId}&startTime=2023-02-01T00:00:00Z&endTime=${currentTime}&fields=humidity`;

        const response = await fetch(apiUrl, {
            headers: {
                'x-api-key': 'II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay'
            },
            method: 'GET',
            mode: 'cors',
            cache: 'no-cache'
        });

        if (!response.ok) {
            throw new Error('Failed to fetch humidity data');
        }

        const data = await response.json();
        const valuesArray = data.results[0].series[0].values;
        valuesArray.sort((a, b) => a[0] - b[0]);
        const latestData = valuesArray[valuesArray.length - 1];
        const latestHumidity = latestData[1];

        // Update the content of the humidity div element
        const humidityElement = document.getElementById(`humidity${roomId}`);
        humidityElement.textContent = `Humidity: ${latestHumidity}%`;
    } catch (error) {
        console.error(`Error fetching humidity for ${roomName}:`, error);
    }
}


// Call both functions to fetch and print temperature and humidity for each room when the page loads
window.addEventListener('load', () => {
    for (const roomName in roomMapping) {
        fetchDataAndPrintTemperature(roomName, roomMapping[roomName]);
        fetchDataAndPrintHumidity(roomName, roomMapping[roomName]);
        fetchDataAndPrintCo2(roomName, roomMapping[roomName]);
    }
});
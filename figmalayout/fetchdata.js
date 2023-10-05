// Mapping of room names to their respective IDs
const roomMapping = {
    'Room 209': '8',
    'Room 109': '10',
    'Room 307': '11',
    'Room 129': '18',
    'Room 126': '19',
    'Room 229': '20',
    'Room 226': '21',
    'Room 326': '22',
    'Restaurant Hall': '9',
    'Lower restaurant': '12',
    'Upper restaurant': '16',
    'Lower lobby cloakroom': '14',
    'Lower lobby': '7',
    '2.nd floor lobby space': '15',
    'Vuolle 1 meeting room': '13',
    'Linno 1 ja 2 neuvottelutila': '17',
    'Linno 1 ja 2 neuvottelutila': '23'
};

// Function to fetch data from the API and get the latest temperature value
async function fetchDataAndPrintTemperature(roomName, roomId) {
    try {
            const endTime = new Date();
            const startTime = new Date(endTime.getTime() - 2 * 60 * 60 * 1000); // Last 6 hours
            const startTimeStr = startTime.toISOString();
            const endTimeStr = endTime.toISOString();

        const apiUrl = `https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id=${roomId}&startTime=${startTimeStr}&endTime=${endTimeStr}&fields=temperature`;

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


// Function to display a loading indicator
function showLoadingIndicator(roomId) {
    const temperatureElement = document.getElementById(`temperature${roomId}`);
    const humidityElement = document.getElementById(`humidity${roomId}`);
    const Co2Element = document.getElementById(`Co2_${roomId}`);

    temperatureElement.textContent = 'Loading...';
    humidityElement.textContent = 'Loading...';
    Co2Element.textContent = 'Loading...';
}

// Function to update data for a room
async function updateRoomData(roomName, roomId) {
    try {
        // Display a loading indicator while fetching data
        showLoadingIndicator(roomId);

        // Fetch and update temperature, humidity, and CO2 data for the room
        await fetchDataAndPrintTemperature(roomName, roomId);
        await fetchDataAndPrintHumidity(roomName, roomId);
        await fetchDataAndPrintCo2(roomName, roomId);
    } catch (error) {
        console.error(`Error updating data for ${roomName}:`, error);
    }
}

// Function to periodically update data for a room
function startPeriodicUpdates(roomName, roomId) {
    setInterval(() => {
        updateRoomData(roomName, roomId);
    }, 300000); // Update every 5 minutes (300,000 milliseconds)
}

// Call updateRoomData for each room when the page loads to fetch initial data
window.addEventListener('load', () => {
    for (const roomName in roomMapping) {
        updateRoomData(roomName, roomMapping[roomName]);
        // Start periodic updates after the initial data is fetched
        startPeriodicUpdates(roomName, roomMapping[roomName]);
    }
});
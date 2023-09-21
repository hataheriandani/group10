// Add event listeners when the DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("fetchDataButton").addEventListener("click", fetchData);
    document.getElementById("exportButton").addEventListener("click", exportToExcel);
});

let tableData; // Store table data for export

async function fetchData() {
    try {
        const apiKey = "II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay"; // Replace with your actual API key
        const roomId = document.getElementById("roomId").value; // Get the room ID from the input
        const startTime = document.getElementById("startTime").value; // Get the start time from the input
        const endTime = document.getElementById("endTime").value; // Get the end time from the input

        // Create the API URL with the start and end times
        const apiUrl = `https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id=${roomId}&startTime=${startTime}:00Z&endTime=${endTime}:00Z&fields=temperature,humidity,co2,light,motion,vdd`; // Use the room ID in the API endpoint

        // Create headers with the x-api-key header containing your API key
        const headers = new Headers({
            "x-api-key": apiKey,
            "Content-Type": "application/json",
        });

        // Create a request object with the desired method, headers, and other options
        const request = new Request(apiUrl, {
            method: "GET",
            headers: headers,
        });

        // Make the API request
        const response = await fetch(request);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Store the data for export
        tableData = data.results[0]?.series[0]; // Use optional chaining to handle undefined data

        // Call a function to create and display the table with borders
        displayDataInTable(tableData);
        // Enable the export button when data is available
        document.getElementById("exportButton").disabled = false;

        // Calculate and update pie charts
        const co2Values = tableData.values.map((row) => row[tableData.columns.indexOf("co2")]);
        const humidityValues = tableData.values.map((row) => row[tableData.columns.indexOf("humidity")]);
        const temperatureValues = tableData.values.map((row) => row[tableData.columns.indexOf("temperature")]);

        const averageCO2 = calculateAverage(co2Values);
        const averageHumidity = calculateAverage(humidityValues);
        const averageTemperature = calculateAverage(temperatureValues);

        updatePieChart("co2Chart", "CO2", averageCO2);
        updatePieChart("humidityChart", "Humidity", averageHumidity);
        updatePieChart("temperatureChart", "Temperature", averageTemperature);
    } catch (error) {
        console.error("Fetch error:", error);
    }
}

function displayDataInTable(data) {
    const table = document.createElement("table");
    table.classList.add("data-table"); // Add the class to your table

    // Apply border styles to the table element
    table.style.borderCollapse = "collapse";
    table.style.width = "100%";
    table.style.border = "1px solid #ddd";

    const headerRow = table.createTHead().insertRow();
    const dataRow = table.insertRow();

    // Example: Create header cells with borders
    for (const column of tableData.columns) {
        const headerCell = headerRow.insertCell();
        headerCell.textContent = column;
        headerCell.style.border = "1px solid #ddd"; // Add border style to header cells
        headerCell.style.background = "#f2f2f2";
        headerCell.style.padding = "8px";
        headerCell.style.textAlign = "left";
    }

    // Example: Create data cells with borders
    for (const values of tableData.values) {
        const dataRow = table.insertRow(); // Create a new row for data
    
        for (const value of values) {
            const cell = dataRow.insertCell(); // Use dataRow to create cells
            cell.textContent = value === null ? "null" : value;
            cell.style.border = "1px solid #ddd"; // Add border style to data cells
            cell.style.padding = "8px";
            cell.style.textAlign = "left";
        }
    }

    // Get the container where you want to append the table
    const container = document.getElementById("table-container");

    // Remove any existing table
    container.innerHTML = "";

    // Append the table to the container
    container.appendChild(table);
}

function calculateAverage(values) {
    const sum = values.reduce((acc, value) => acc + parseFloat(value), 0);
    return (sum / values.length).toFixed(2);
}

function updatePieChart(chartId, label, value) {
    const ctx = document.getElementById(chartId).getContext("2d");

    const data = {
        labels: [label, "Others"],
        datasets: [{
            data: [value, 100 - value], // Assuming the total is 100%
            backgroundColor: ["#FF5733", "#EAEAEA"],
        }],
    };

    const options = {
        title: {
            display: true,
            text: `${label} Average`,
            fontSize: 16,
        },
    };

    const chart = new Chart(ctx, {
        type: "pie",
        data: data,
        options: options,
    });
}
// Inside the fetchData() function after updating pie charts
// Update live data
updateLiveData(tableData);

// Update Pie Charts
updatePieChart("co2PieChart", "CO2", averageCO2);
updatePieChart("temperaturePieChart", "Temperature", averageTemperature);
updatePieChart("humidityPieChart", "Humidity", averageHumidity);
function updateLiveData(data) {
    const liveDataContainer = document.getElementById("liveData");

    // Create a table to display live data
    const liveDataTable = document.createElement("table");
    liveDataTable.classList.add("data-table");

    // Create header row
    const headerRow = liveDataTable.createTHead().insertRow();
    for (const column of data.columns) {
        const headerCell = headerRow.insertCell();
        headerCell.textContent = column;
    }

    // Create data row with the latest data
    const dataRow = liveDataTable.insertRow();
    const latestData = data.values[data.values.length - 1];
    for (const value of latestData) {
        const cell = dataRow.insertCell();
        cell.textContent = value === null ? "null" : value;
    }

    // Clear previous data and append the updated live data table
    liveDataContainer.innerHTML = "";
    liveDataContainer.appendChild(liveDataTable);
}
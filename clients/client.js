// fetch data from flask server
async function fetchData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/request_data');
        const data = await response.json();
        // console.log(data);  // Logging the entire dictionary
        return data;
    } catch (error) {
        console.error('Error fetching game info:', error);
        return 'inactive'; // Default to 'inactive' on error
    }
}

let map;
let mapLayersGroup;
let markersClusterGroup;
let typeChartInstance;
let trendChartInstance;

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Initialize Leaflet Map Base
    const mapElement = document.getElementById('crimeMap');
    if (mapElement) {
        map = L.map('crimeMap').setView([20.5937, 78.9629], 5);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);
        mapLayersGroup = L.layerGroup().addTo(map);
    }
    
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Inter';

    window.refreshChartsAndMap();
});

window.refreshChartsAndMap = async () => {
    // Get filter values
    const dateRange = document.getElementById('dateRange')?.value || '';
    const type = document.getElementById('filterType')?.value || '';
    const area = document.getElementById('filterArea')?.value || '';
    
    let queryStr = `?type=${encodeURIComponent(type)}&area=${encodeURIComponent(area)}`;
    if (dateRange && dateRange.includes('to')) {
        const dates = dateRange.split(' to ');
        queryStr += `&start=${dates[0]}&end=${dates[1]}`;
    }

    if (map && mapLayersGroup) {
        mapLayersGroup.clearLayers();
        if (markersClusterGroup) {
            map.removeLayer(markersClusterGroup);
        }
        
        try {
            const response = await fetch('/api/incidents' + queryStr, {
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('auth_token') }
            });
            const incidents = await response.json();
            
            // Heatmap
            const heatData = incidents.map(inc => [inc.lat, inc.lng, inc.severity === 'High' ? 1.0 : 0.5]);
            L.heatLayer(heatData, {radius: 25, blur: 15, maxZoom: 10, minOpacity: 0.4}).addTo(mapLayersGroup);
            
            // Marker Cluster
            markersClusterGroup = L.markerClusterGroup({
                chunkedLoading: true,
                maxClusterRadius: 50
            });
            incidents.forEach(inc => {
                const color = inc.severity === 'High' ? 'red' : 'orange';
                const markerHtml = `<div style="background-color: ${color}; width: 15px; height: 15px; border-radius: 50%; border: 2px solid white;"></div>`;
                const customIcon = L.divIcon({ html: markerHtml, className: '', iconSize: [15, 15] });
                
                const marker = L.marker([inc.lat, inc.lng], {icon: customIcon})
                    .bindPopup(`<b>${inc.type}</b><br>Area: ${inc.area}<br>Severity: ${inc.severity}<br>${new Date(inc.timestamp).toLocaleString()}`);
                markersClusterGroup.addLayer(marker);
            });
            map.addLayer(markersClusterGroup);
            
            // Fetch and plot Patrol Units
            const patrolRes = await fetch('/api/patrols', {
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('auth_token') }
            });
            const patrols = await patrolRes.json();
            
            patrols.forEach(p => {
                const iconColor = p.status === 'Dispatched' ? '#ff2a2a' : '#00f3ff';
                const patrolHtml = `<div style="color: ${iconColor}; font-size: 20px; text-shadow: 0 0 5px ${iconColor};"><i class="fa-solid fa-car-on"></i></div>`;
                const customIcon = L.divIcon({ html: patrolHtml, className: '', iconSize: [20, 20], iconAnchor: [10, 10] });
                
                L.marker([p.lat, p.lng], {icon: customIcon})
                    .bindPopup(`<b>${p.name}</b><br>Status: <span style="color:${iconColor}">${p.status}</span>`)
                    .addTo(mapLayersGroup);
            });
            
        } catch (e) {
            console.error("Error fetching map data:", e);
        }
    }

    // 2. Initialize Charts (Chart.js)
    
    // Set global theme config
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Inter';

    const typeCtx = document.getElementById('typeChart');
    if (typeCtx) {
        try {
            const resp = await fetch('/api/charts/type' + queryStr, {
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('auth_token') }
            });
            const typeData = await resp.json();
            
            if (typeChartInstance) typeChartInstance.destroy();
            typeChartInstance = new Chart(typeCtx, {
                type: 'doughnut',
                data: {
                    labels: typeData.labels,
                    datasets: [{
                        data: typeData.data,
                        backgroundColor: ['#00f3ff', '#ff2a2a', '#0077ff', '#ffffff'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'right' } },
                    cutout: '70%'
                }
            });
        } catch (e) {
            console.error("Error fetching type chart data:", e);
        }
    }

    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        try {
            const resp = await fetch('/api/charts/trend' + queryStr, {
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('auth_token') }
            });
            const trendData = await resp.json();
            
            if (trendChartInstance) trendChartInstance.destroy();
            trendChartInstance = new Chart(trendCtx, {
                type: 'line',
                data: {
                    labels: trendData.labels,
                    datasets: [
                        {
                            label: 'Reported Incidents',
                            data: trendData.reported,
                            borderColor: '#00f3ff',
                            backgroundColor: 'rgba(0, 243, 255, 0.1)',
                            borderWidth: 2,
                            tension: 0.4, // smooth curves
                            fill: true,
                            pointBackgroundColor: trendData.anomalies.map(a => a === -1 ? '#ff2a2a' : '#070913'),
                            pointBorderColor: trendData.anomalies.map(a => a === -1 ? '#ff2a2a' : '#00f3ff'),
                            pointBorderWidth: 2,
                            pointRadius: trendData.anomalies.map(a => a === -1 ? 6 : 3)
                        },
                        {
                            label: 'Upper Bound (95% CI)',
                            data: trendData.upper_bound,
                            borderColor: 'transparent',
                            backgroundColor: 'transparent',
                            pointRadius: 0,
                            fill: false,
                            tension: 0.4
                        },
                        {
                            label: 'Lower Bound (95% CI)',
                            data: trendData.lower_bound,
                            borderColor: 'transparent',
                            backgroundColor: 'rgba(255, 42, 42, 0.15)',
                            pointRadius: 0,
                            fill: '-1', // Fill to previous dataset (Upper Bound)
                            tension: 0.4
                        },
                        {
                            label: 'AI Predicted Trend',
                            data: trendData.predicted,
                            borderColor: '#ff2a2a',
                            borderDash: [5, 5],
                            borderWidth: 2,
                            tension: 0.4,
                            fill: false,
                            pointRadius: 3,
                            pointBackgroundColor: '#ff2a2a'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'top' }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255, 255, 255, 0.05)' }
                        },
                        x: {
                            grid: { color: 'rgba(255, 255, 255, 0.05)' }
                        }
                    }
                }
            });
        } catch (e) {
            console.error("Error fetching trend chart data:", e);
        }
    }
};

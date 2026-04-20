/* Project: Environmental Audit GIS
  Module: assets/www/map_logic.js
  #NEW_FEATURE: 處理地圖圖層切換、JS 端方位角計算、動畫播放迴圈與 Python 橋接
*/

// --- 1. 地圖與圖層初始化 ---
const map = L.map('map').setView([23.5, 121], 7); // 預設中心為台灣

// 豐富圖層定義
const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 });
const googleHybrid = L.tileLayer('http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', { maxZoom: 20 });
const googleSatellite = L.tileLayer('http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}', { maxZoom: 20 });

googleHybrid.addTo(map); // 預設使用混合圖層(含路網與空拍)

// 加入圖層控制面板
L.control.layers({
    "Google 混合圖層": googleHybrid,
    "Google 空拍圖": googleSatellite,
    "OpenStreetMap": osmLayer
}).addTo(map);

// 全域變數宣告
let trackData = [];
let stoppointData = [];
let currentIndex = 0;
let isPlaying = false;
let explorationMode = true;
let playInterval = null;

let trackPolyline = null;
let currentPathPolyline = null;
let vehicleMarker = null;
let heatLayer = null;
let stoppointMarkers = [];

// --- 2. 接收來自 Python 的資料 ---
window.receiveGISData = function(data) {
    trackData = data.tracks || [];
    stoppointData = data.stoppoints || [];
    currentIndex = 0;
    
    clearMap();

    if (trackData.length === 0) return;

    // 繪製完整的底色軌跡線 (淺色)
    const latlngs = trackData.map(pt => [pt.lat, pt.lng]);
    trackPolyline = L.polyline(latlngs, {color: 'gray', weight: 3, opacity: 0.5}).addTo(map);
    
    // 繪製已走過的軌跡線 (紅色)
    currentPathPolyline = L.polyline([], {color: 'red', weight: 5, opacity: 0.8}).addTo(map);

    // 繪製停頓點熱區 (Heatmap)
    if (stoppointData.length > 0) {
        const heatPoints = stoppointData.map(pt => [pt.lat, pt.lng, pt.duration * 0.5]);
        heatLayer = L.heatLayer(heatPoints, {radius: 35, blur: 20, maxZoom: 17, gradient: {0.4: 'blue', 0.6: 'cyan', 0.7: 'lime', 0.8: 'yellow', 1.0: 'red'}}).addTo(map);
        
        // 標記隱形停頓點 (用於探索模式計算距離)
        stoppointData.forEach(pt => {
            const circle = L.circleMarker([pt.lat, pt.lng], {radius: 5, color: 'purple'}).addTo(map);
            circle.bindPopup(`<b>${pt.name}</b><br>停留: ${pt.duration} 分鐘`);
            stoppointMarkers.push({ marker: circle, data: pt });
        });
    }

    // 建立 3D 車輛圖示 (使用動態 SVG 與 CSS 旋轉)
    const carIcon = L.divIcon({
        html: `<div style="font-size: 32px; text-align: center;">🚓</div>`,
        className: 'vehicle-marker',
        iconSize: [40, 40],
        iconAnchor: [20, 20]
    });
    
    vehicleMarker = L.marker([trackData[0].lat, trackData[0].lng], {icon: carIcon}).addTo(map);
    map.fitBounds(trackPolyline.getBounds());
    
    updateFrame();
};

// --- 3. 處理 Python 傳來的動作指令 ---
window.triggerAction = function(action, payload) {
    if (action === 'toggle_play') {
        isPlaying = payload.is_playing;
        if (isPlaying) {
            playInterval = setInterval(() => {
                if (currentIndex < trackData.length - 1) {
                    currentIndex++;
                    updateFrame();
                } else {
                    clearInterval(playInterval);
                    window.triggerAction('toggle_play', {is_playing: false}); // 播完自動停止
                }
            }, 300); // 動畫速度，可從 Python 傳遞參數調整
        } else {
            clearInterval(playInterval);
        }
    } else if (action === 'step_forward') {
        if (currentIndex < trackData.length - 1) currentIndex++;
        updateFrame();
    } else if (action === 'step_backward') {
        if (currentIndex > 0) currentIndex--;
        updateFrame();
    } else if (action === 'show_all') {
        currentIndex = trackData.length - 1;
        updateFrame();
    } else if (action === 'set_exploration_mode') {
        explorationMode = payload.enabled;
        if(!explorationMode) document.getElementById('info-card').classList.remove('show');
    }
};

// --- 4. 動畫影格更新與方位角計算 ---
function updateFrame() {
    if (trackData.length === 0) return;
    
    const pt = trackData[currentIndex];
    
    // 更新走過的軌跡線
    const currentLatLngs = trackData.slice(0, currentIndex + 1).map(p => [p.lat, p.lng]);
    currentPathPolyline.setLatLngs(currentLatLngs);
    
    // 計算車頭方位角 (Bearing)
    let bearing = 0;
    if (currentIndex < trackData.length - 1) {
        const nextPt = trackData[currentIndex + 1];
        bearing = calculateBearing(pt.lat, pt.lng, nextPt.lat, nextPt.lng);
    } else if (currentIndex > 0) {
        const prevPt = trackData[currentIndex - 1];
        bearing = calculateBearing(prevPt.lat, prevPt.lng, pt.lat, pt.lng);
    }
    
    // 更新車輛位置與轉向
    vehicleMarker.setLatLng([pt.lat, pt.lng]);
    const iconElement = vehicleMarker._icon;
    if (iconElement) {
        // 利用 CSS 轉換讓車頭朝向行駛方向
        iconElement.style.transform = `${iconElement.style.transform.replace(/rotate\([^\)]+\)/g, '')} rotate(${bearing}deg)`;
    }
    
    // 鏡頭跟隨
    map.panTo([pt.lat, pt.lng], {animate: true, duration: 0.3});

    // 探索模式邏輯：檢查是否靠近停頓點
    if (explorationMode) {
        checkNearbyStoppoints(pt.lat, pt.lng);
    }
}

// --- 5. 輔助運算與 UI 邏輯 ---
function calculateBearing(lat1, lng1, lat2, lng2) {
    const toRad = Math.PI / 180;
    const toDeg = 180 / Math.PI;
    const dLng = (lng2 - lng1) * toRad;
    const y = Math.sin(dLng) * Math.cos(lat2 * toRad);
    const x = Math.cos(lat1 * toRad) * Math.sin(lat2 * toRad) - Math.sin(lat1 * toRad) * Math.cos(lat2 * toRad) * Math.cos(dLng);
    return (Math.atan2(y, x) * toDeg + 360) % 360;
}

let activeStoppoint = null;
function checkNearbyStoppoints(lat, lng) {
    const threshold = 100; // 距離閾值(公尺)
    let found = false;
    
    for (let sp of stoppointMarkers) {
        const dist = map.distance([lat, lng], [sp.data.lat, sp.data.lng]);
        if (dist < threshold) {
            found = true;
            if (activeStoppoint !== sp.data.name) {
                activeStoppoint = sp.data.name;
                showInfoCard(sp.data);
                
                // 模擬系統介入：自動暫停讓稽查員查看
                if (isPlaying) {
                    window.triggerAction('toggle_play', {is_playing: false});
                    // 通知 Python 更新按鈕 UI (此處需依賴實務雙向綁定，目前為前端暫停)
                }
            }
            break;
        }
    }
    
    if (!found) {
        activeStoppoint = null;
        document.getElementById('info-card').classList.remove('show');
    }
}

function showInfoCard(data) {
    document.getElementById('ic-time').innerText = data.start_time;
    document.getElementById('ic-duration').innerText = data.duration;
    document.getElementById('ic-poi').innerText = data.name;
    document.getElementById('info-card').classList.add('show');
}

window.openStreetView = function() {
    if (trackData.length > 0 && currentIndex >= 0) {
        const pt = trackData[currentIndex];
        // 開啟 Google 街景 URL (可由 Android 預設瀏覽器或 Google Maps App 接手)
        const url = `https://www.google.com/maps?layer=c&cbll=${pt.lat},${pt.lng}`;
        window.open(url, '_blank');
    }
};

function clearMap() {
    if (trackPolyline) map.removeLayer(trackPolyline);
    if (currentPathPolyline) map.removeLayer(currentPathPolyline);
    if (vehicleMarker) map.removeLayer(vehicleMarker);
    if (heatLayer) map.removeLayer(heatLayer);
    stoppointMarkers.forEach(sp => map.removeLayer(sp.marker));
    stoppointMarkers = [];
    document.getElementById('info-card').classList.remove('show');
}
document.addEventListener('DOMContentLoaded', () => {

    window.addEventListener("map:init", e => {
        const map = e.detail.map;
        
        // map.setView([38.7, 9.13], 12);

        map.addEventListener("click", e => {
            L.marker(e.latlng).addTo(map);
        });

    }, false);


});
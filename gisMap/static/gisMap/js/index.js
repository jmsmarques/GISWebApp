document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#my_map").addEventListener('mousedown', e => {
        e.target.style.cursor = 'grabbing';
    });

    document.querySelector("#my_map").addEventListener('mouseup', e => {
        e.target.style.cursor = 'pointer';
    });
});
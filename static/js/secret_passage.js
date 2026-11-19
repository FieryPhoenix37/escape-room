let clickCount = 0
function countClicks() {
    clickCount++;
    if(clickCount == 3) {
        window.location.href = '/escape';
    }
}
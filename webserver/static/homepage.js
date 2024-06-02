
let url = "http://" + host_ip + ":5000/select_player.html";
console.log("QR URL: " + url);

function generateQRCode() {
    console.log("Generating QR code for " + url);
    new QRCode(document.getElementById("qrcode"), url);
}

window.onload = generateQRCode();
function expanddiv() {
    var expandDiv = document.getElementById('expenddiv');

    expandDiv.style.transition="transform"
    expandDiv.style.transitionDuration="2s"
    expandDiv.style.zIndex=1
    expandDiv.style.transformOrigin="right"
    expandDiv.style.transform="scaleX(2)"

    var innerElements = expandDiv.querySelectorAll('h1, button');
    innerElements.forEach(function (element) {
        element.style.transform="translateX(25)"
        element.style.transition = "transform 2s";
        element.style.transformOrigin = "left"; // Adjust the transform origin as needed
        element.style.transform = "scaleX(0.5)";
    });

    // Wait for the animation to complete (0.5s) before redirecting to the Django register URL
    setTimeout(function () {
        fetch("{% url 'home.html' %}", {
            method: 'GET', // You can adjust the HTTP method as needed
        })
            .then(function (response) {
                // Handle the response here (e.g., redirect to a new page)
                console.log(response.url);
                window.location.href ="http://127.0.0.1:8000/home";
            })
            .catch(function (error) {
                console.error('Error:', error);
            });
    }, 2000); // 2000 milliseconds = 2 seconds (matching the transition duration)
}


function edit(){
    var editButton = document.getElementById('toggleedit');
    var saveButton = document.getElementById('togglesave');
    var fnameInput = document.getElementById('fname');
    var lnameInput = document.getElementById('lname');
    var address = document.getElementById('address');

    editButton.classList.add('displaynone');
    saveButton.classList.remove('displaynone');

    fnameInput.disabled = false;
    fnameInput.readOnly = false;

    lnameInput.disabled = false;
    lnameInput.readOnly = false;

    address.disabled = false;
    address.readOnly = false;
    

}

document.addEventListener("DOMContentLoaded", function () {
    share(); // Call the share function when the page is ready
});


function share() {
    const shareButton = document.getElementById("share-btn");
    const popup = document.getElementById("popup");
    const closeBtn = document.getElementById("close-btn");
    const copyLink = document.getElementById("video-link");
    const copyBtn = document.getElementById("copy-btn");
    const link = document.getElementById("link1").value;
    console.log(link);

    shareButton.addEventListener("click", function () {
        popup.style.display = "flex";
        copyLink.value = link; // Replace with your video link
    });

    closeBtn.addEventListener("click", function () {
        popup.style.display = "none";
    });

    copyBtn.addEventListener("click", function () {
        copyLink.select();
        document.execCommand("copy");
    });

    // Handle click events for each share option (e.g., Facebook, Twitter, LinkedIn)
    const shareFacebook = document.getElementById("facebook");
    shareFacebook.addEventListener("click", function () {
        // Handle the Facebook sharing logic here
    });

    const shareTwitter = document.getElementById("twitter");
    shareTwitter.addEventListener("click", function () {
        // Handle the Twitter sharing logic here

    });

    const shareLinkedIn = document.getElementById("linkedin");
    shareLinkedIn.addEventListener("click", function () {
        // Handle the LinkedIn sharing logic here

    });
}




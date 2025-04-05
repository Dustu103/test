document.addEventListener("DOMContentLoaded", function () {
    const authButton = document.getElementById("auth-btn");
    if (authButton) {
        authButton.addEventListener("click", function () {
            chrome.identity.launchWebAuthFlow(
                {
                    url: "http://localhost:5000/login",
                    interactive: true
                },
                (redirectUrl) => {
                    if (chrome.runtime.lastError) {
                        console.error(chrome.runtime.lastError);
                        return;
                    }
                    console.log("Authenticated:", redirectUrl);
                }
            );
        });
    } else {
        console.error("auth-btn not found in popup.html");
    }
});

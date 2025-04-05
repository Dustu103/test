chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension Installed");
  });
  
  function authenticate() {
    chrome.identity.launchWebAuthFlow(
      { url: "http://localhost:5000/login", interactive: true },
      (redirectUrl) => {
        if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError);
            return;
        }
        console.log("Authenticated:", redirectUrl);
      }
    );
  }
  
  chrome.action.onClicked.addListener(authenticate);
  